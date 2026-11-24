"""Generate an importable native KNIME fixture from a particular release."""
import argparse
from copy import deepcopy
from io import BytesIO
from pathlib import Path
import struct
import subprocess
import sys
from zipfile import ZipFile, ZIP_DEFLATED
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "validation/T10"))
from prepare_boundary import NS, array, entry, key

ARCHIVE = "workflows/oral-b-italy.knwf"
BASE = "c23610a63fbd9934cb2c29cbddb8ee329d5d06af"
REVIEWED = "96fcb4a"
SCORES = {
    "eleven_twentieths": struct.unpack("f", struct.pack("f", 11 / 20))[0],
    "six_tenths": struct.unpack("f", struct.pack("f", 6 / 10))[0],
    "thirteen_twentieths": struct.unpack("f", struct.pack("f", 13 / 20))[0],
    "below": .5999999, "above": .6000001, "decimal_tie": .6,
}


def generate(mode, trained=False):
    title = f"Issue31-{'trained-' if trained else ''}{mode}"
    dest = HERE / "local" / title
    dest.mkdir(parents=True, exist_ok=True)
    rev = BASE if mode == "red" else REVIEWED if trained else None
    source = (subprocess.check_output(["git", "show", rev + ":" + ARCHIVE], cwd=ROOT)
              if rev else (ROOT / ARCHIVE).read_bytes())
    with ZipFile(BytesIO(source)) as release, ZipFile(dest.with_suffix(".knwf"), "w", ZIP_DEFLATED) as out:
        wf = ET.fromstring(release.read("oral-b-italy/workflow.knime"))
        nodes, edges = key(wf, "nodes"), key(wf, "connections")
        template = deepcopy(nodes[0])
        nodes[:] = []
        edges[:] = []
        wf.remove(key(wf, "annotations"))

        def write(path, root):
            key(root, "state").set("value", "CONFIGURED")
            ET.indent(root, "    ")
            out.writestr(title + "/" + path, ET.tostring(root, encoding="utf-8", xml_declaration=True))

        def add(i, x, y, original=None):
            member, = [n for n in release.namelist() if n.endswith(f"(#{original or i})/settings.xml")]
            r = ET.fromstring(release.read(member))
            m = key(r, "model")
            if i == 52 or original == 52:
                cols = [("case", "String"), ("P (target=success)", "Double"),
                        ("raw_probability", "Double"), ("scenario", "String"), ("success", "Int")]
                rows = [(case, p, p, s, 1) for case, p in SCORES.items() for s in ("lower","base","upper")]
                if trained:
                    cols = [(name, "Double") for name in
                            ("population", "income", "household_size", "hygienists", "dentist_distance")]
                    if i == 52:
                        cols.append(("target", "String"))
                        rows = [(100 if j < 10 else 200, 30, 2, 1, 5,
                                 "success" if j < 6 else "failure") for j in range(20)]
                    else:
                        cols.append(("case", "String"))
                        rows = [(101, 30, 2, 1, 5, "held_out")]
                        key(m, "rowIdPrefix").set("value", "Test")
                props = key(m, "columnProperties")
                prop = deepcopy(props[0])
                props[:] = []
                for j, (name, typ) in enumerate(cols):
                    c = deepcopy(prop)
                    c.set("key", str(j))
                    key(c, "ColumnName").set("value",name)
                    key(key(c,"ColumnClass"),"cell_class").set("value",f"org.knime.core.data.def.{typ}Cell")
                    props.append(c)
                cells = [(idx, j, v) for idx, row in enumerate(rows) for j,v in enumerate(row)]
                for j,(name,typ) in enumerate([("rowIndices","xint"),("columnIndices","xint"),("values","xstring")]):
                    array(key(m,name),[c[j] for c in cells],typ)
            if i == 120:
                # Connect the single validation-tree policy to the downstream column schema.
                key(key(m,"renamings")[0],"newName").set("value","probability")
            if original == 189:
                key(r,"variables")[:] = []
                p = key(key(key(m,"settings"),"file_chooser_settings"),"path")
                key(p,"path").set("value",str(dest / {901:"validation.csv",902:"base.csv",903:"stress.csv",904:"raw.csv"}[i]))
            node = deepcopy(template)
            path = f"{key(r,'node-name').get('value')} (#{i})/settings.xml"
            node.set("key",f"node_{i}")
            key(node,"id").set("value",str(i))
            key(node,"node_settings_file").set("value",path)
            bounds = key(key(node,"ui_settings"),"extrainfo.node.bounds")
            for j,v in enumerate([x,y,-1,-1]):
                key(bounds,str(j)).set("value",str(v))
            nodes.append(node)
            write(path,r)

        def link(a,b,port=1,source_port=1):
            c=ET.SubElement(edges,NS+"config",key=f"connection_{len(edges)}")
            for name,v in zip(("sourceID","sourcePort","destID","destPort"),(a,source_port,b,port)):
                entry(c,name,v,"xint")

        add(52,80,200)
        add(23,80,40)
        policy_input = 52
        chains = []
        if trained:
            add(900,80,420,52)
            add(322,260,200)
            add(327,440,420)
            add(904,620,620,189)
            link(52,322)
            link(322,327,1,3)
            link(900,327,2)
            link(327,904)
            policy_input = 327
        else:
            chains.append((200,[52] + ([601] if mode=="green" else []) + [120,143,144,159,163,167,901]))
        chains.append((420,[policy_input] + ([602] if mode=="green" else []) + [330,336,337,902]))
        for y, chain in chains:
            for j,(a,b) in enumerate(zip(chain,chain[1:])):
                add(b,(660 if trained else 300)+j*180,y,189 if b>=900 else None)
                link(a,b)
        if not trained:
            for j,(a,b) in enumerate(zip([330,348,349,350],[348,349,350,903])):
                add(b,660+j*180,610,189 if b==903 else None)
                link(a,b)
            for b in (143,349):
                link(23,b,0)
        link(23,336,0)
        write("workflow.knime",wf)
    print(dest.with_suffix(".knwf"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode",choices=["red","green"])
    parser.add_argument("--trained", action="store_true", help="fit the release tree on labeled training rows")
    args = parser.parse_args()
    generate(args.mode, args.trained)
