"""Print a revision-bound handoff only after a matching full native rerun."""
import argparse
from hashlib import sha256
from pathlib import Path
import subprocess

from reconcile import ROOT, check


def digest(data):
    return sha256(data).hexdigest()


def manifest(run):
    workflow = "workflows/oral-b-italy.knwf"
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    pinned = {}
    for path in (workflow, "outputs/financial-summary.csv", "data/Activated_Stores.xlsx", "data/Italian_Stores.xlsx"):
        blob = subprocess.check_output(["git", "show", f"{revision}:{path}"], cwd=ROOT)
        if blob != (ROOT / path).read_bytes():
            raise ValueError(f"Working file differs from {revision}: {path}")
        pinned[path] = digest(blob)
    if (run / "release.sha256").read_text().split()[0] != pinned[workflow]:
        raise ValueError("Rerun used a different workflow; do not sign this revision.")
    exports = check(run / "outputs")
    return "\n".join([f"Artifact revision: {revision}", "Pinned artifacts and inputs:",
                      *(f"{h}  {p}" for p, h in pinned.items()),
                      "Fresh KNIME exports matching reviewed references:", exports])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path, help="Run directory created by threshold/full.py")
    print(manifest(parser.parse_args().run))
