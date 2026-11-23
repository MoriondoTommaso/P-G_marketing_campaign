"""Prepare an isolated KNIME boundary fixture using the release node settings."""
from copy import deepcopy
from pathlib import Path
import xml.etree.ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[2]
LOCAL = Path(__file__).resolve().parent / "local" / "boundary"
NS = "{http://www.knime.org/2008/09/XMLConfig}"
ET.register_namespace("", NS[1:-1])
ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")


def key(element, name):
    return next(child for child in element if child.get("key") == name)


def entry(parent, name, value, type_="xstring"):
    ET.SubElement(parent, NS + "entry", key=name, type=type_, value=str(value))


def array(element, values, type_):
    element[:] = []
    entry(element, "array-size", len(values), "xint")
    for i, value in enumerate(values):
        entry(element, str(i), value, type_)


def prepare():
    dest = LOCAL / "Funding-boundary.knwf"
    result = LOCAL / "boundary.csv"
    if dest.exists() or result.exists():
        raise FileExistsError(f"Existing fixture or results in {LOCAL}")
    LOCAL.mkdir(exist_ok=True, parents=True)
    with ZipFile(ROOT / "workflows/oral-b-italy.knwf") as release, ZipFile(dest, "x", ZIP_DEFLATED) as fixture:
        def write(name, element):
            ET.indent(element, "    ")
            fixture.writestr("Funding-boundary/" + name, ET.tostring(element, encoding="utf-8", xml_declaration=True))

        wf = ET.fromstring(release.read("oral-b-italy/workflow.knime"))
        template = deepcopy(key(wf, "nodes")[0])  # root settings node, not a metanode
        key(wf, "nodes")[:] = []
        key(wf, "connections")[:] = []
        wf.remove(key(wf, "annotations"))
        for i, x, y in [(52,80,250),(23,80,60),(143,300,250),(144,520,250),
                        (159,740,250),(163,960,250),(167,1180,250),(189,1400,250)]:
            member, = [n for n in release.namelist() if n.endswith(f"(#{i})/settings.xml")]
            r = ET.fromstring(release.read(member))
            m = key(r, "model")
            if i == 52:
                array(key(m,"rowIndices"),[0,0,1,1,2,2],"xint")
                array(key(m,"columnIndices"),[0,1,0,1,0,1],"xint")
                array(key(m,"values"),["0.5999999","1","0.6","1","0.6000001","0"],"xstring")
                props = key(m,"columnProperties")
                second = deepcopy(props[0])
                second.set("key","1")
                key(second,"ColumnName").set("value","success")
                props.append(second)
                key(props[0],"ColumnName").set("value","probability")
                key(key(props[0],"ColumnClass"),"cell_class").set("value","org.knime.core.data.def.DoubleCell")
                key(key(r,"nodeAnnotation"),"text").set("value","Synthetic inputs just below, at and above break-even.")
            if i == 189:
                key(r,"variables")[:] = []
                fp=key(key(key(m,"settings"),"file_chooser_settings"),"path")
                key(fp,"path").set("value",str(result))
                key(key(r,"nodeAnnotation"),"text").set("value","Write the three boundary cases for independent checking.")
            n = deepcopy(template)
            n.set("key",f"node_{i}")
            key(n,"id").set("value",str(i))
            filename = "/".join(member.split("/")[-2:])
            key(n,"node_settings_file").set("value",filename)
            b=key(key(n,"ui_settings"),"extrainfo.node.bounds")
            for j,v in enumerate((x,y,-1,-1)):
                key(b,str(j)).set("value",str(v))
            key(wf,"nodes").append(n)
            write(filename,r)
        edges=[(52,1,143,1),(23,1,143,0),(143,1,144,1),(144,1,159,1),
               (159,1,163,1),(163,1,167,1),(167,1,189,1)]
        for j,edge in enumerate(edges):
            c=ET.SubElement(key(wf,"connections"),NS+"config",key=f"connection_{j}")
            for k,v in zip(("sourceID","sourcePort","destID","destPort"),edge):
                entry(c,k,v,"xint")
        write("workflow.knime",wf)
    print(dest)


if __name__ == "__main__":
    prepare()
