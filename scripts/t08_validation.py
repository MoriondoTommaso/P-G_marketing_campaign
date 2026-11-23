"""Prepare a repo-local KNIME workspace or check T08's paired Desktop runs."""

import argparse
import csv
import hashlib
import math
from pathlib import Path, PurePosixPath
from xml.sax.saxutils import escape
from zipfile import ZipFile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
QA = ROOT / "validation/T08"
LOCAL = QA / "local"
REFERENCE = "a5be2eeea3a41874ddb88db300c1f35fc9f7c052aab8f962a67f25b653ff9745"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def prepare():
    workspace = LOCAL / "workspace"
    require(not any((workspace / f"T08-{tag}").exists() for tag in "AB"),
            f"Workflow already exists in {workspace}; refusing to overwrite.")
    for tag in "AB":
        out = LOCAL / "results" / tag
        require(not out.exists() or not any(out.iterdir()), f"Results already present: {out}")
    with ZipFile(ROOT / "workflows/oral-b-italy.knwf") as archive:
        def base(folder):
            name, = [n for n in archive.namelist() if n.endswith(f"(#{folder})/settings.xml")]
            r = ET.fromstring(archive.read(name))
            return r.find("./{*}config[@key='model']/{*}config[@key='base_folder']/"
                          "{*}config[@key='path']/{*}entry[@key='path']").attrib["value"].encode()

        old_input, old_output = base(34), base(35)
        for tag in "AB":
            dest = workspace / f"T08-{tag}"
            out = LOCAL / "results" / tag
            out.mkdir(parents=True, exist_ok=True)
            replacements = [(old, escape(str(new), {'"': '&quot;'}).encode())
                            for old, new in [(old_input, ROOT / "data"), (old_output, out)]]
            for member in archive.infolist():
                path = PurePosixPath(member.filename)
                require(path.parts[0] == "oral-b-italy" and ".." not in path.parts, "Invalid archive path")
                if member.is_dir():
                    continue
                data = archive.read(member)
                if path.suffix in {".knime", ".xml"}:
                    for old, new in replacements:
                        data = data.replace(old, new)
                if tag == "B" and path.parent.name == "Sorter (#21)" and path.name == "settings.xml":
                    require(data.count(b'value="ASCENDING"') == 1, "Unexpected upstream sort")
                    data = data.replace(b'value="ASCENDING"', b'value="DESCENDING"')
                target = dest.joinpath(*path.parts[1:])
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
    print(f"Open this workspace in KNIME Desktop: {workspace}")


def rows(file):
    with file.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def check(root):
    order = []
    for tag in "AB":
        folder = root / tag
        universe = rows(folder / "store-universe.csv")
        ids = [r["store_id"] for r in universe]
        order.append(ids)
        y = {r["store_id"]: int(r["success"]) for r in universe if r["success"] != ""}
        require(len(ids) == len(set(ids)) == 480 and len(y) == 170
                and set(y.values()) == {0, 1} and sum(y.values()) == 108, f"{tag}: unexpected labels")
        for name in ("folds.csv", "baseline-oof.csv"):
            data = (folder / name).read_bytes()
            require(data == (ROOT / "outputs" / name).read_bytes(), f"{tag}: differs from release {name}")
            require(data.count(b"\n") == 171, f"{tag}: wrong row count in {name}")
        require(hashlib.sha256((folder / "folds.csv").read_bytes()).hexdigest() == REFERENCE,
                f"{tag}: fold reference mismatch")
        folds = {r["store_id"]: int(r["fold"]) for r in rows(folder / "folds.csv")}
        scores = rows(folder / "baseline-oof.csv")
        require(len(scores) == 170 and {r["store_id"] for r in scores} == folds.keys() == y.keys(),
                f"{tag}: missing, duplicate or unlabeled IDs")
        for r in scores:
            k = folds[r["store_id"]]
            train = [label for i, label in y.items() if folds[i] != k]
            require(int(r["fold"]) == k and len(train) == 136
                    and math.isclose(float(r["baseline_probability"]), sum(train) / len(train),
                                     rel_tol=0, abs_tol=1e-12), f"{tag}: wrong rate for {r['store_id']}")
    require(order[0] == order[1][::-1], "Run B did not reverse the input order")
    print("PASS: reversed input, reference folds and all 170 training-only probabilities in both runs.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "check", "check-rerun"])
    cmd = parser.parse_args().command
    if cmd == "prepare":
        prepare()
    else:
        check(QA / "evidence" if cmd == "check" else LOCAL / "results")
