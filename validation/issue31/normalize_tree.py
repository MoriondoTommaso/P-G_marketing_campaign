"""Insert a native Rule Engine immediately after each tree score column filter."""
from copy import deepcopy
from pathlib import Path
from struct import pack, unpack
from xml.etree import ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED
import sys


def child(parent, key):
    return parent.find(f"./*[@key='{key}']")


def setvalue(parent, key, value):
    child(parent, key).set("value", str(value))


def insert(files, src, dst, number):
    old = next(p for p in files if p.endswith(f"(#{dst})/settings.xml"))
    folder = old.rsplit("/", 2)[0]
    flow = folder + "/workflow.knime"
    wf = ET.fromstring(files[flow])
    node = deepcopy(child(child(wf, "nodes"), f"node_{dst}"))
    node.set("key", f"node_{number}")
    setvalue(node, "id", number)
    name = f"Rule Engine (#{number})/settings.xml"
    setvalue(node, "node_settings_file", name)
    bounds = child(child(node, "ui_settings"), "extrainfo.node.bounds")
    setvalue(bounds, "1", int(child(bounds, "1").get("value")) + 130)
    child(wf, "nodes").append(node)
    connections = child(wf, "connections")
    wire, = [c for c in connections if child(c, "sourceID").get("value") == str(src)
             and child(c, "destID").get("value") == str(dst)]
    new = deepcopy(wire)
    setvalue(wire, "destID", number)
    setvalue(new, "sourceID", number)
    new.set("key", "connection_" + str(1 + max(int(c.get("key").split("_")[1]) for c in connections)))
    connections.append(new)
    settings = ET.fromstring(files[next(p for p in files if p.endswith("(#159)/settings.xml"))])
    model = child(settings, "model")
    column = "P (target=success)"
    setvalue(model, "append-column", "false")
    for k in ("replace-column-name", "new-column-name"):
        setvalue(model, k, column)
    rules = child(model, "rules")
    elem = deepcopy(child(rules, "0"))
    rules.remove(child(rules, "0"))
    rules.remove(child(rules, "1"))
    statements = []
    for boundary in (.55, .60, .65):
        binary32, = unpack("f", pack("f", boundary))
        statements.append(f"${column}$ = {binary32} => {boundary}")
    statements.append(f"TRUE => ${column}$")
    setvalue(rules, "array-size", len(statements))
    for i, statement in enumerate(statements):
        row = deepcopy(elem)
        row.attrib.update(key=str(i), value=statement)
        rules.append(row)
    setvalue(child(settings, "nodeAnnotation"), "text",
             "Restore exact 55%, 60%, 65% tree leaf ties before funding and stress decisions.")
    for path, xml in ((flow, wf), (folder + "/" + name, settings)):
        files[path] = ET.tostring(xml, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    ET.register_namespace("", "http://www.knime.org/2008/09/XMLConfig")
    ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
    src, dst = map(Path, sys.argv[1:])
    with ZipFile(src) as z:
        files = {n: z.read(n) for n in z.namelist()}
    insert(files, 119, 120, 601)
    insert(files, 329, 330, 602)
    with ZipFile(dst, "w", ZIP_DEFLATED) as z:
        for path, data in files.items():
            z.writestr(path, data)
