"""Exercise the candidate's vote rounding and Decision B rule in KNIME, with supplied scores."""
from copy import deepcopy
from pathlib import Path
import sys
from xml.etree import ElementTree as ET
from zipfile import ZipFile

from build_folds import idle, put, xml
from native_folds import ROOT, execute, key, rows, value

CASES = [
    ("new59", "refit_unseen", "?", .5899999737739563, 0),
    ("new60", "refit_unseen", "?", .6000000238418579, 0),
    ("new61", "refit_unseen", "?", .6100000143051147, 1),
    ("prior-success", "held_out_2026", "success", .52, 1),
    ("prior-failure", "held_out_2026", "failure", .98, 0),
]


def create(scratch):
    wf = scratch / "boundary"
    wf.mkdir(parents=True)
    with ZipFile(ROOT / "workflows/oral-b-italy-final.knwf") as z, ZipFile(
            ROOT / "workflows/oral-b-italy.knwf") as rc3:
        flow = ET.fromstring(z.read("oral-b-italy-final/workflow.knime"))
        ns, cs = key(flow,"nodes"), key(flow,"connections")
        nodes = {int(value(n,"id")): n for n in ns}
        edge = deepcopy(cs[0])
        ns[:], cs[:] = [], []
        for i in (800,142,94,102):
            node = deepcopy(nodes[142 if i==800 else i])
            path = value(node,"node_settings_file")
            if i == 800:
                src = next(f for f in rc3.namelist() if f.endswith("Table Creator (#52)/settings.xml"))
                st = ET.fromstring(rc3.read(src))
                path = "Table Creator (#800)/settings.xml"
                m = key(st,"model")
                props = key(m,"columnProperties")
                prop = deepcopy(props[0])
                props[:] = []
                for j,col in enumerate(("case","score_source","target","P (target=success)")):
                    p = deepcopy(prop)
                    p.set("key",str(j))
                    put(p,"ColumnName",col)
                    typ = "Double" if j==3 else "String"
                    put(key(p,"ColumnClass"),"cell_class",f"org.knime.core.data.def.{typ}Cell")
                    props.append(p)
                for field,k in enumerate(("rowIndices","columnIndices","values")):
                    group = key(m,k)
                    proto = deepcopy(group[1])
                    group[:] = [group[0]]
                    put(group,"array-size",4*len(CASES))
                    for r,case in enumerate(CASES):
                        for c,v in enumerate(case[:4]):
                            e = deepcopy(proto)
                            e.set("key",str(4*r+c))
                            e.set("value",str((r,c,v)[field]))
                            group.append(e)
            else:
                st = ET.fromstring(z.read("oral-b-italy-final/"+path))
            if i==102:
                st.remove(key(st,"variables"))
                key(st,"model").find(".//*[@key='path'][@value]").set("value",str(scratch/"result.csv"))
            node.set("key",f"node_{i}")
            put(node,"id",i)
            put(node,"node_settings_file",path)
            ns.append(node)
            idle(st)
            (wf/path).parent.mkdir()
            (wf/path).write_bytes(xml(st))
        for j,(a,b) in enumerate(((800,142),(142,94),(94,102))):
            c = deepcopy(edge)
            c.set("key",f"connection_{j}")
            for k,v in zip(("sourceID","destID","sourcePort","destPort"),(a,b,1,1)):
                put(c,k,v)
            cs.append(c)
        idle(flow)
        (wf/"workflow.knime").write_bytes(xml(flow))
    return wf


if __name__ == "__main__":
    scratch = Path(sys.argv[1]).resolve()
    scratch.mkdir(exist_ok=False)
    execute(create(scratch),scratch)
    actual = [(r["case"],float(r["P (target=success)"]),int(r["recommend_activate"]))
              for r in rows(scratch/"result.csv")]
    if actual != [(name,round(p,2),flag) for name,_,_,p,flag in CASES]:
        raise ValueError(f"unexpected native decisions: {actual}")
    print(actual)
