"""Check actual native holdout assignments without executing finance or publishing outputs."""
import copy
import csv
import os
import signal
from pathlib import Path
import subprocess
import sys
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
ENGINE = ROOT / "validation/issue31/native/run.py"
ECLIPSE = "/Applications/KNIME 5.12.1.app/Contents/Eclipse"
ET.register_namespace("", "http://www.knime.org/2008/09/XMLConfig")


def key(el, k):
    return el.find(f"*[@key='{k}']")


def value(el, k):
    return key(el, k).get("value")


def prepare(scratch, candidate):
    with ZipFile(candidate) as archive:
        archive.extractall(scratch)
    wf = scratch / "oral-b-italy-final"
    flow = ET.parse(wf / "workflow.knime")
    ns, cs = (key(flow.getroot(), k) for k in ("nodes", "connections"))
    nodes = {int(value(n, "id")): n for n in ns}
    targets = {44: "identities", 49: "tree", 57: "forest", 67: "logistic"}
    keep = set(targets)
    while extra := {int(value(c, "sourceID")) for c in cs if int(value(c, "destID")) in keep} - keep:
        keep.update(extra)
    for i, n in nodes.items():
        if i not in keep:
            ns.remove(n)
    for c in list(cs):
        if not {int(value(c, k)) for k in ("sourceID", "destID")} <= keep:
            cs.remove(c)
    for i, (source, name) in enumerate(targets.items(), 1000):
        n, c = copy.deepcopy(nodes[102]), copy.deepcopy(cs[0])
        p = wf / f"tap{i}/settings.xml"
        p.parent.mkdir()
        st = ET.parse(wf / value(n, "node_settings_file"))
        st.getroot().remove(key(st.getroot(), "variables"))
        for k, v in (("path", str(scratch / f"{name}.csv")), ("write_row_header", "true")):
            key(st.getroot(), "model").find(f".//*[@key='{k}'][@value]").set("value", v)
        st.write(p, encoding="utf-8")
        n.set("key", f"node_{i}")
        key(n, "id").set("value", str(i))
        key(n, "node_settings_file").set("value", str(p.relative_to(wf)))
        ns.append(n)
        c.set("key", f"connection_{10000+i}")
        for k, v in zip(("sourceID", "destID", "sourcePort", "destPort"), (source, i, 1, 1)):
            key(c, k).set("value", str(v))
        cs.append(c)
    for e, filename in [(flow, wf / "workflow.knime")] + [
        (ET.parse(p), p) for n in ns for p in [wf / value(n, "node_settings_file")]
    ]:
        key(e.getroot(), "state").set("value", "IDLE")
        if (content := key(e.getroot(), "hasContent")) is not None:
            content.set("value", "false")
        e.write(filename, encoding="utf-8", xml_declaration=True)
    return wf


def rows(path):
    with path.open() as f:
        return list(csv.DictReader(f))


if __name__ == "__main__":
    scratch = Path(sys.argv[1]).resolve()
    scratch.mkdir(exist_ok=False)
    wf = prepare(scratch, sys.argv[2] if len(sys.argv) > 2 else ROOT / "workflows/oral-b-italy-final.knwf")
    cmd = [sys.executable, "-B", ENGINE, wf, scratch / "runtime", ECLIPSE]
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                          start_new_session=True,
                          env={**os.environ, "JAVA_TOOL_OPTIONS": "-Djava.awt.headless=true"}) as proc:
        success = False
        for line in proc.stdout:
            print(line, end="")
            if line.strip() == "REVIEW_NATIVE_RESULT false":
                os.killpg(proc.pid, signal.SIGTERM)
                break
            success |= line.strip() == "REVIEW_NATIVE_RESULT true"
        if proc.wait() or not success:
            raise RuntimeError("native execution failed")
    ids = {r["row ID"]: r["Pdv Code"] for r in rows(scratch / "identities.csv")}
    expected = {r["store_id"]: int(r["fold"]) for r in rows(ROOT / "outputs/folds.csv")}
    for model in ("tree", "forest", "logistic"):
        records = rows(scratch / f"{model}.csv")
        actual = {ids[r["row ID"]]: 1 + int(r["fold #"]) for r in records}
        wrong = [i for i in sorted(expected) if actual.get(i) != expected[i]]
        if len(records) != 170 or actual != expected:
            raise ValueError(f"{model}: {len(wrong)} protocol fold mismatches; first IDs: {wrong[:5]}")
        print(f"{model}: all 170 held-out IDs match the protocol")
