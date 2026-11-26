"""Migrate the class archive to protocol folds using the native RC3 node templates.

Usage: python3 build_folds.py CLASS.knwf RC3.knwf NEW.knwf
The output is an unexecuted candidate; cached tables, models and exports are not evidence.
"""
import copy
from pathlib import Path
import sys
from xml.etree import ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile

from native_folds import key, value


def put(el, k, v):
    key(el, k).set("value", str(v))


def xml(el):
    return ET.tostring(el, encoding="utf-8", xml_declaration=True)


def idle(el):
    put(el, "state", "IDLE")
    if key(el, "hasContent") is not None:
        put(el, "hasContent", "false")
    for bucket in ("ports", "filestores", "internalObjects"):
        group = key(el, bucket)
        if group is not None:
            for entry in group.iter():
                if entry.get("key") in ("port_dir_location", "file_store_location", "file_store_id"):
                    entry.set("value", "")
                    entry.set("isnull", "true")


def migrate(src, rc3, dst):
    root = "oral-b-italy-final/"
    tpl = "oral-b-italy/03  Assign fixed folds (#205)/"
    with ZipFile(src) as old, ZipFile(rc3) as templates, ZipFile(dst, "x", ZIP_DEFLATED) as out:
        wf = ET.fromstring(old.read(root + "workflow.knime"))
        ns, cs = key(wf, "nodes"), key(wf, "connections")
        proto = ET.fromstring(templates.read(tpl + "workflow.knime"))
        for n in key(proto, "nodes"):
            t = int(value(n, "id"))
            if not 40 <= t <= 49:
                continue
            i = t + 110
            path = value(n, "node_settings_file")
            s = ET.fromstring(templates.read(tpl + path))
            m = key(s, "model")
            if t == 40:
                put(m, "expression", "return String.valueOf($Pdv Code$);")
                put(m, "append_column", "false")  # legacy settings: false means append
            if t == 48:
                put(m, "create_new_rowids", "false")
                put(m, "fail_on_duplicates", "true")
            if t == 49:
                criteria = key(m, "sortingCriteria")
                second = copy.deepcopy(criteria[0])
                second.set("key", "1")
                criteria.append(second)
                put(key(criteria[0], "columnV2"), "regularChoice", "fold")
            path = path.replace(f"(#{t})", f"(#{i})")
            put(n, "id", i)
            put(n, "node_settings_file", path)
            n.set("key", f"node_{i}")
            bounds = key(key(n, "ui_settings"), "extrainfo.node.bounds")
            put(bounds, "1", int(value(bounds, "1")) + 2500)
            ns.append(n)
            idle(s)
            out.writestr(root + path, xml(s))
        for c in cs:
            if (value(c, "sourceID"), value(c, "destID")) == ("44", "45"):
                put(c, "sourceID", 159)
        for j, (a, b, port) in enumerate([
            (44,150,1), (150,151,1), (151,152,1), (152,153,1), (153,154,1),
            (151,155,1), (155,156,1), (156,157,1), (154,158,1), (157,158,2),
            (158,159,1),
        ], 1000):
            c = copy.deepcopy(cs[0])
            c.set("key", f"connection_{j}")
            for k, v in zip(("sourceID", "destID", "sourcePort", "destPort"), (a,b,1,port)):
                put(c, k, v)
            cs.append(c)
        idle(wf)
        out.writestr(root + "workflow.knime", xml(wf))
        for f in old.namelist():
            if f.endswith("/settings.xml"):
                s = ET.fromstring(old.read(f))
                idle(s)
                if any(f"(#{i})/" in f for i in (46,54,64)):
                    put(key(s, "model"), "stratifiedSampling", "false")
                out.writestr(f, xml(s))
            elif f.startswith(root + "data/inputs/") or Path(f).name in ("workflowset.meta", "workflow-metadata.xml"):
                out.writestr(f, old.read(f))
        out.writestr(root + "data/outputs/", "")


if __name__ == "__main__":
    migrate(*sys.argv[1:])
