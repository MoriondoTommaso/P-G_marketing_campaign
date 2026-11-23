"""Prepare isolated native workflows; check publication only after Execute All."""
import argparse
import re
import shutil
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

ET.register_namespace("", "http://www.knime.org/2008/09/XMLConfig")
ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")

ROOT = Path(__file__).resolve().parents[3]
CASES = ("valid", "conflict", "unmatched", "duplicate-label", "wrong-source",
         "missing-oof", "duplicate-oof", "duplicate-national", "wrong-fold")


def prepare(archive, dest, case):
    dest.mkdir(parents=True, exist_ok=False)
    data = dest / "data"
    shutil.copytree(ROOT / "data", data)
    (dest / "output").mkdir()
    workbook = data / "Activated_Stores.xlsx"
    if case in {"conflict", "unmatched", "duplicate-label"}:
        with ZipFile(workbook) as z:
            files = {n: z.read(n) for n in z.namelist()}
        sheet = "xl/worksheets/sheet1.xml"
        xml = files[sheet]
        if case == "duplicate-label":
            row2 = re.search(rb'<row r="2".*?</row>', xml).group()
            row3 = row2.replace(b'r="2"', b'r="3"')
            row3 = re.sub(rb'r="([A-D])2"', rb'r="\g<1>3"', row3)
            xml = re.sub(rb'<row r="3".*?</row>', lambda _: row3, xml)
        else:
            addr = b"B2" if case == "conflict" else b"A2"
            xml, n = re.subn(rb'(<c r="' + addr + rb'"><v>).*?(</v>)',
                             rb'\g<1>99999999\2', xml)
            assert n == 1
        files[sheet] = xml
        with ZipFile(workbook, "w", ZIP_DEFLATED) as z:
            for n, b in files.items():
                z.writestr(n, b)
    with ZipFile(archive) as z:
        z.extractall(dest / "workspace")
    # Also localize reader schema snapshots and writer fallback paths, as in T08.
    for i, target in [(34, data), (35, dest/"output")]:
        p, = (dest / "workspace").glob(f"**/* (#{i})/settings.xml")
        old = ET.parse(p).find(".//{*}entry[@key='path']").get("value").encode()
        new = escape(str(target.resolve()), {'"': '&quot;'}).encode()
        for f in (dest/"workspace").rglob("*"):
            if f.suffix in {".xml", ".knime"}:
                f.write_bytes(f.read_bytes().replace(old, new))
    def setting(i, key, value):
        p, = (dest / "workspace").glob(f"**/* (#{i})/settings.xml")
        r = ET.parse(p)
        e = r.find(f".//{{*}}entry[@key='{key}']")
        e.set("value", value)
        r.write(p, encoding="utf-8", xml_declaration=True)
    if case == "wrong-source":
        setting(334, "0", 'TRUE => "held_out_2026"')
    elif case == "missing-oof":
        setting(145, "0", '$fold$ <= 4 => TRUE')
    elif case == "duplicate-oof":
        # 510 rows still exist; every tree key now appears twice.
        setting(137, "0", 'TRUE => "tree"')
    elif case == "duplicate-national":
        p, = (dest / "workspace").glob("**/* (#232)/workflow.knime")
        xml = ET.parse(p)
        for c in xml.findall(".//{*}config[@key='connections']/{*}config"):
            props = {e.get("key"): e for e in c}
            if props["destID"].get("value") == "335" and props["destPort"].get("value") == "2":
                props["sourceID"].set("value", "333")
        xml.write(p, encoding="utf-8", xml_declaration=True)
    elif case == "wrong-fold":
        # Retain the same national IDs, but corrupt the join identity of baseline rows.
        p, = (dest / "workspace").glob("**/* (#59)/settings.xml")
        # Select a shifted fold using a native Rule Engine just before the score join.
        # Inject it into the same place regardless of whether guards are present.
        w = p.parent.parent
        src, = (dest / "workspace").glob("**/* (#126)/settings.xml")
        target = w / "Rule Engine (#890)"
        target.mkdir()
        r = ET.parse(src)
        rule = r.find(".//{*}config[@key='rules']")
        rule[:] = list(rule)[:2]
        rule[0].set("value", "1")
        rule[1].set("value", "TRUE => 9")
        r.write(target / "settings.xml", encoding="utf-8", xml_declaration=True)
        import copy
        xml = ET.parse(w / "workflow.knime")
        nodes = xml.find("./{*}config[@key='nodes']")
        n = copy.deepcopy(nodes[0])
        n.set("key", "node_890")
        n.find("./{*}entry[@key='id']").set("value", "890")
        n.find("./{*}entry[@key='node_settings_file']").set("value", target.name + "/settings.xml")
        nodes.append(n)
        edges = xml.find("./{*}config[@key='connections']")
        edge, = [c for c in edges if c.find("./{*}entry[@key='destID']").get("value") == "-1"]
        new = copy.deepcopy(edge)
        edge.find("./{*}entry[@key='destID']").set("value", "890")
        edge.find("./{*}entry[@key='destPort']").set("value", "1")
        new.set("key", "connection_890")
        new.find("./{*}entry[@key='sourceID']").set("value", "890")
        edges.append(new)
        xml.write(w / "workflow.knime", encoding="utf-8", xml_declaration=True)


def check(dest, case):
    out = dest / "output"
    if case == "valid":
        expected = {p.name: p.read_bytes() for p in (ROOT / "outputs").glob("*.csv")}
        expected.pop("store-profiles.csv")  # separate T07 analysis, not a workflow export
        expected["spatial-decisions.csv"] = (ROOT / "validation/T10/spatial-decisions.csv").read_bytes()
        for p in out.glob("*.csv"):
            assert expected.pop(p.name) == p.read_bytes(), p
        assert not expected, expected.keys()
    else:
        assert not list(out.iterdir()), f"writer ran on invalid {case}: {list(out.iterdir())}"


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("action", choices=["prepare", "check"])
    ap.add_argument("archive", type=Path)
    ap.add_argument("dest", type=Path)
    ap.add_argument("case", choices=CASES)
    a = ap.parse_args()
    if a.action == "prepare":
        prepare(a.archive, a.dest, a.case)
    else:
        check(a.dest, a.case)
