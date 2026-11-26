"""Build the class candidate from the pre-T52 class archive (d067910).

Usage: python3 build_folds.py CLASS.knwf RC3.knwf NEW.knwf
RC3 supplies only the standard Table Creator template. Its two-column lookup is
the published protocol map for these 170 stores, not code run inside KNIME.
"""
import copy
import csv
from pathlib import Path
import sys
from xml.etree import ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile

from native_folds import ROOT, key, value


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
    with ZipFile(src) as old, ZipFile(rc3) as templates, ZipFile(dst, "x", ZIP_DEFLATED) as out:
        wf = ET.fromstring(old.read(root + "workflow.knime"))
        ns, cs = key(wf, "nodes"), key(wf, "connections")
        layout = copy.deepcopy(ns[0])
        tree = copy.deepcopy(next(n for n in ns if value(n, "id") == "48"))
        predictor = ET.fromstring(old.read(root + value(tree, "node_settings_file")))
        put(key(predictor, "nodeAnnotation"), "text", "Benchmark: the tree trained on all 170 labeled stores scores the 310 new stores.")
        idle(predictor)
        tree.set("key", "node_163")
        put(tree, "id", 163)
        path = "Decision Tree Predictor (#163)/settings.xml"
        put(tree, "node_settings_file", path)
        bounds = key(key(tree, "ui_settings"), "extrainfo.node.bounds")
        put(bounds, "0", 3200)
        put(bounds, "1", 2450)
        ns.append(tree)
        out.writestr(root + path, xml(predictor))
        table_path = next(f for f in templates.namelist() if f.endswith("Table Creator (#52)/settings.xml"))
        for i, archive, source, x, y in [
            (150, templates, table_path, 100, 2450),
            (151, old, root + "Joiner (#108)/settings.xml", 300, 2450),
            (159, old, root + "Sorter (#98)/settings.xml", 500, 2450),
            (162, old, root + "Sorter (#98)/settings.xml", 100, 2260),
        ]:
            s = ET.fromstring(archive.read(source))
            put(key(s, "nodeAnnotation"), "text", {
                150: "Fixed cross-validation groups: store ID and fold (1–5) for the 170 labeled stores.",
                151: "Match each labeled store to its fold by store ID.",
                159: "Order by fold, then store ID, for five test groups of 34.",
                162: "Sort the 480 stores by store ID before deriving the target.",
            }[i])
            m = key(s, "model")
            if i == 150:
                with (ROOT / "outputs/folds.csv").open() as stream:
                    records = list(csv.DictReader(stream))
                props = key(m, "columnProperties")
                id_col = copy.deepcopy(props[0])
                put(id_col, "ColumnName", "fold_store")
                put(key(id_col, "ColumnClass"), "cell_class", "org.knime.core.data.def.StringCell")
                props[0].set("key", "1")
                put(props[0], "ColumnName", "fold")
                props.insert(0, id_col)
                cells = [(row, col, r[k]) for row,r in enumerate(records)
                         for col,k in enumerate(("store_id", "fold"))]
                for j,k in enumerate(("rowIndices", "columnIndices", "values")):
                    group = key(m, k)
                    item = group[1]
                    group[:] = [group[0]]
                    put(group, "array-size", len(cells))
                    for ncell, cell in enumerate(cells):
                        e = copy.deepcopy(item)
                        e.set("key", str(ncell))
                        e.set("value", str(cell[j]))
                        group.append(e)
            elif i == 151:
                crit = key(m, "matchingCriteria")[0]
                put(key(crit, "rightTableColumnV2"), "regularChoice", "fold_store")
                put(m, "dataCellComparisonMode", "STRING")
                put(m, "rowKeyFactory", "SEQUENTIAL")
                right = key(key(key(m, "rightColumnSelectionConfigV2"), "manualFilter"), "manuallySelected")
                right[:] = right[:3]
                put(right, "array-size", 2)
                put(right, "0", "fold_store")
                put(right, "1", "fold")
            else:
                criteria = key(m, "sortingCriteria")
                put(key(criteria[0], "columnV2"), "regularChoice", "fold" if i == 159 else "Pdv Code")
                if i == 159:
                    second = copy.deepcopy(criteria[0])
                    second.set("key", "1")
                    put(key(second, "columnV2"), "regularChoice", "fold_store")
                    criteria.append(second)
            dirname = Path(source).parent.name.rsplit(" (#", 1)[0]
            path = f"{dirname} (#{i})/settings.xml"
            n = copy.deepcopy(layout)
            n.set("key", f"node_{i}")
            put(n, "id", i)
            put(n, "node_settings_file", path)
            bounds = key(key(n, "ui_settings"), "extrainfo.node.bounds")
            put(bounds, "0", x)
            put(bounds, "1", y)
            ns.append(n)
            idle(s)
            out.writestr(root + path, xml(s))
        for c in cs:
            if (value(c, "sourceID"), value(c, "destID")) == ("44", "45"):
                put(c, "sourceID", 159)
            if (value(c, "sourceID"), value(c, "destID")) == ("18", "31"):
                put(c, "sourceID", 162)
            if (value(c, "sourceID"), value(c, "destID")) == ("31", "44"):
                put(c, "sourceID", 151)
        for j, (a, b, port) in enumerate([
            (18,162,1), (31,151,1), (150,151,2), (44,159,1), (77,163,1), (76,163,2),
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
