"""Install issue #31 pre-publication guards into a reset release workflow."""
import argparse
from copy import deepcopy
from pathlib import Path
import re
import xml.etree.ElementTree as E
from zipfile import ZipFile, ZIP_DEFLATED

Q = "{http://www.knime.org/2008/09/XMLConfig}"
E.register_namespace("", Q[1:-1])
E.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")


def key(el, k):
    return next(c for c in el if c.get("key") == k)


def put(el, k, v):
    key(el, k).set("value", str(v))


def value(el, k):
    return key(el, k).get("value")


def config(el, k):
    return E.SubElement(el, Q+"config", key=k)


def entry(el, k, v, t="xstring"):
    return E.SubElement(el, Q+"entry", key=k, value=str(v), type=t)


def array(el, items):
    el[:] = []
    entry(el, "array-size", len(items), "xint")
    for i, item in enumerate(items):
        entry(el, str(i), item)


def position(n, x, y):
    b = key(key(n, "ui_settings"), "extrainfo.node.bounds")
    put(b, "0", x)
    put(b, "1", y)


class Archive:
    def __init__(self, src):
        with ZipFile(src) as z:
            self.files = {n: z.read(n) for n in z.namelist()}
        self.root, = [n for n in self.files if n.count("/") == 1 and n.endswith("/workflow.knime")]
        self.w = {}
        self.path = {0: self.root}
        self.parent = {}
        self.nodes = {}
        self.dirty = set()
        self.serial = 1000
        self.load(0)

    def load(self, i):
        p = self.path[i]
        self.w[i] = E.fromstring(self.files[p])
        if p.endswith("workflow.knime"):
            for n in key(self.w[i], "nodes"):
                j = int(value(n, "id"))
                if j in self.path:
                    raise ValueError(f"nonunique node id: {j}")
                self.nodes[j] = n
                self.parent[j] = i
                self.path[j] = p.rsplit("/", 1)[0]+"/"+value(n, "node_settings_file")
                self.load(j)

    def edit(self, i):
        self.dirty.add(i)
        return self.w[i]

    def model(self, i):
        return key(self.edit(i), "model")

    def clone(self, t, parent, title, x, y):
        self.serial += 1
        i = self.serial
        assert i not in self.path
        n = deepcopy(self.nodes[t])
        r = deepcopy(self.w[t])
        self.w[i], self.nodes[i], self.parent[i] = r, n, parent
        self.dirty.add(i)
        path = re.sub(r'\(#\d+\)', f"(#{i})", value(n, "node_settings_file"))
        self.path[i] = self.path[parent].rsplit("/", 1)[0]+"/"+path
        put(n, "node_settings_file", path)
        put(n, "id", i)
        n.set("key", f"node_{i}")
        position(n, x, y)
        put(key(r, "nodeAnnotation"), "text", title)
        key(self.edit(parent), "nodes").append(n)
        return i

    def edges(self, parent):
        return key(self.edit(parent), "connections")

    def wire(self, parent, src, dst):
        cs = self.edges(parent)
        i = max((int(c.get("key").split("_")[-1]) for c in cs), default=-1)+1
        c = config(cs, f"connection_{i}")
        for k, v in zip(("sourceID", "sourcePort", "destID", "destPort"), (*src, *dst)):
            entry(c, k, v, "xint")

    def port(self, i, side, name, var=False):
        ps = key(key(self.edit(i), f"meta_{side}_ports"), "port_enum")
        j = len(ps)
        p = config(ps, f"{side}port_{j}")
        entry(p, "index", j, "xint")
        entry(p, "name", name)
        entry(config(p, "type"), "object_class", "org.knime.core.node." +
              ("port.flowvariable.FlowVariablePortObject" if var else "BufferedDataTable"))
        return j

    def expose(self, parent, src, name):
        while parent:
            j = self.port(parent, "out", name)
            self.wire(parent, src, (-1, j))
            src, parent = (parent, j), self.parent[parent]
        return src

    def insert_after(self, i, t, label, x, y):
        p = self.parent[i]
        j = self.clone(t, p, label, x, y)
        for c in self.edges(p):
            if value(c, "sourceID") == str(i) and value(c, "sourcePort") == "1":
                put(c, "sourceID", j)
        self.wire(p, (i, 1), (j, 1))
        return j

    def save(self, dest):
        for i in self.dirty:
            r = self.w[i]
            E.indent(r, "    ")
            self.files[self.path[i]] = E.tostring(r, encoding="utf-8", xml_declaration=True)
        with ZipFile(dest, "w", ZIP_DEFLATED) as z:
            for n, b in self.files.items():
                z.writestr(n, b)


def build(src, dest):
    if src.resolve() == dest.resolve() or dest.resolve() == Path(__file__).resolve().parents[3]/"workflows/oral-b-italy.knwf":
        raise ValueError("choose a separate output archive")
    a = Archive(src)
    writers = [i for i, p in a.path.items() if "/CSV Writer (#" in p]
    assert len(writers) == 13

    # The loop's test selection is fold == k before either model's predictor.
    # Reattach that actual iteration identity without adding a predictor feature.
    for i in (117, 120):
        j = a.insert_after(i, 41, "Record the held-out iteration (not a predictor)", 1450, 440)
        m = a.model(j)
        put(m, "expression", "return $${Ik}$$;")
        put(m, "replaced_column", "fold")
        put(m, "return_type", "java.lang.Integer")
    for i in (121, 122):
        m = a.model(i)
        criteria = key(m, "matchingCriteria")
        c = deepcopy(criteria[0])
        c.set("key", "1")
        for e in c.findall(".//{*}entry[@key='regularChoice']"):
            e.set("value", "fold")
        criteria.append(c)
        put(m, "includeLeftUnmatchedInOutput", "true")
        put(m, "includeRightUnmatchedInOutput", "true")
    # Carry surplus/misaligned predictions through the join and reject them.
    # Otherwise an extra score in the wrong fold can disappear without changing the OOF count.
    j = a.insert_after(122, 41, "Fail unmatched predictions (including exploratory folds)", 780, 300)
    m = a.model(j)
    put(m, "expression", 'if ($store_id$ == null || $fold$ == null || $baseline_probability$ == null || '
        '$logistic_probability$ == null || $tree_probability$ == null) throw new Abort("Release guard: unmatched fold score"); return "ok";')
    put(m, "replaced_column", "alignment_check")
    entry(m, "insert_missing_as_null", "true", "xboolean")

    # Preserve the physical activation row through both joins to detect fanout
    # even if another row is lost and totals accidentally still agree.
    rid = a.insert_after(2, 115, "Stable activation input row for reconciliation", 300, 780)
    put(a.model(rid), "newColumnName4RowKeyValues", "activation_row")
    for i in (6, 8):
        put(a.model(i), "includeLeftUnmatchedInOutput", "true")
        f = key(key(key(a.model(i), "leftColumnSelectionConfigV2"), "manualFilter"), "manuallySelected")
        array(f, [e.get("value") for e in list(f)[1:]] + ["activation_row"])

    g = a.clone(241, 0, "No writer can execute until every release identity reconciles.", 2540, 610)
    old = a.path[g]
    name = f"14  Verify and publish (#{g})/workflow.knime"
    a.path[g] = old.split("/")[0]+"/"+name
    put(a.nodes[g], "node_settings_file", name)
    group = a.edit(g)
    put(group, "name", "14  Verify and publish")
    put(key(group, "annotations")[0], "text", "<p><strong>14 Verify and publish</strong></p><p>All CSV writers depend on the release evidence gate.</p>")
    for k in ("nodes", "connections"):
        key(group, k)[:] = []
    key(key(group, "meta_in_ports"), "port_enum")[:] = []

    def take(src, name, var=False):
        j = a.port(g, "in", name, var)
        a.wire(0, src, (g, j))
        return (-1, j)

    flow = take((35, 1), "Output paths", True)
    evidence = []
    def record(i, label, expr, x, y):
        p = a.parent[i]
        j = a.clone(41, p, label, x, y)
        m = a.model(j)
        put(m, "replaced_column", "evidence")
        put(m, "expression", "return "+expr+";")
        entry(m, "insert_missing_as_null", "true", "xboolean")
        a.wire(p, (i, 1), (j, 1))
        f = a.clone(38, p, "Release identity evidence only", x+185, y)
        filt = key(a.model(f), "column-filter")
        array(key(filt, "included_names"), ["evidence"])
        array(key(filt, "excluded_names"), [])
        a.wire(p, (j, 1), (f, 1))
        evidence.append(take(a.expose(p, (f, 1), label), label))

    record(1, "National input IDs", '"store:" + $Pdv Code$', 980, 820)
    record(rid, "Activation input rows", '"raw:" + $activation_row$', 980, 960)
    record(12, "Resolved labels", '"link:" + $activation_row$ + ":" + $Pdv Code$ + ":" + $success$', 1280, 1090)
    record(32, "Code/coordinate conflicts", '"conflict:" + $Pdv Code$', 1280, 1230)
    record(49, "Assigned historical folds", '"fold:" + $store_id$ + ":" + $fold$', 1580, 770)
    def probability(col):
        c = "$"+col+"$"
        return f'({c} != null && {c} >= 0.0 && {c} <= 1.0)'
    record(145, "Held-out decisions by model", '"oof:" + $store_id$ + ":" + $fold$ + ":" + $model$ + ":" + '+probability("probability"), 1680, 800)
    record(338, "National score IDs and sources", '"score:" + $store_id$ + ":" + $score_source$ + ":" + '+probability("p_success"), 1600, 790)

    # A real sentinel guarantees a nonempty aggregate even with all inputs empty.
    sentinel = a.clone(52, g, "Always evaluate the gate, including on empty inputs", 160, 100)
    m = a.model(sentinel)
    for k, v in (("rowIndices", "0"), ("columnIndices", "0"), ("values", "start:release")):
        arr = key(m, k)
        arr[:] = list(arr)[:2]
        put(arr, "array-size", 1)
        put(arr, "0", v)
    col = key(key(m, "columnProperties"), "0")
    put(col, "ColumnName", "evidence")
    put(key(col, "ColumnClass"), "cell_class", "org.knime.core.data.def.StringCell")
    srcport = (sentinel, 1)
    for ix, other in enumerate(evidence):
        j = a.clone(48, g, "Collect release evidence", 210+130*ix, 260)
        a.wire(g, srcport, (j, 1))
        a.wire(g, other, (j, 2))
        srcport = (j, 1)
    agg = a.clone(37, g, "Collect bounded release keys for exact set comparison", 1040, 260)
    a.wire(g, srcport, (agg, 1))
    m = a.model(agg)
    for k in ("InclList", "ExclList"):
        array(key(key(m, "grouByColumns"), k), [])
    ag = key(m, "aggregationColumn")
    array(key(ag, "columnNames"), ["evidence"])
    array(key(ag, "aggregationMethod"), ["Concatenate_V2.4"])
    put(m, "valueDelimiter", "|")
    put(key(key(ag, "columnTypes"), "0"), "cell_class", "org.knime.core.data.def.StringCell")
    check = a.clone(41, g, "Require 170 labels, 510 OOF predictions and 480 scores: 170 historical + 310 unseen", 1250, 260)
    m = a.model(check)
    put(m, "expression", Path(__file__).with_name("guard.java").read_text())
    put(m, "replaced_column", "release_status")
    a.wire(g, (agg, 1), (check, 1))
    a.wire(g, flow, (check, 0))

    for ix, i in enumerate(writers):
        parent = a.parent[i]
        edges = a.edges(parent)
        data, = [c for c in edges if value(c, "destID") == str(i) and value(c, "destPort") == "1"]
        srcport = int(value(data, "sourceID")), int(value(data, "sourcePort"))
        for c in list(edges):
            if value(c, "destID") == str(i):
                edges.remove(c)
        label = value(key(a.w[i], "nodeAnnotation"), "text")
        port = take(a.expose(parent, srcport, label), label)
        n = a.nodes[i]
        key(a.edit(parent), "nodes").remove(n)
        key(group, "nodes").append(n)
        position(n, 1520+190*(ix//5), 150+150*(ix%5))
        old = a.path[i]
        a.path[i] = a.path[g].rsplit("/", 1)[0]+"/"+value(n, "node_settings_file")
        a.files[a.path[i]] = a.files.pop(old)
        a.wire(g, port, (i, 1))
        a.wire(g, (check, 0), (i, 0))
    a.save(dest)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()
    build(args.input, args.output)
