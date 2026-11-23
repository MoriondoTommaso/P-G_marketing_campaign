"""Compare a fresh native rerun with the 13 reviewed exports; print a hash manifest."""
import argparse
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILES = (
    "store-universe", "join-audit", "baseline-2026", "folds", "baseline-oof",
    "held-out", "held-out-decisions", "model-comparison", "spatial-decisions",
    "national-scores", "activation-list", "sensitivity", "financial-summary",
)


def check(folder):
    rows = []
    for stem in FILES:
        ref_dir = "validation/T10" if stem == "spatial-decisions" else "outputs"
        name = stem + ".csv"
        data = (folder / name).read_bytes()
        if data != (ROOT / ref_dir / name).read_bytes():
            raise ValueError(f"Native export differs: {name}; investigate before delivery")
        rows.append(f"{sha256(data).hexdigest()}  {name}")
    return "\n".join(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rerun_directory", type=Path)
    print(check(parser.parse_args().rerun_directory))
