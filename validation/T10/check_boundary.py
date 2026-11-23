"""Check the below/at/above-break-even rows emitted by the Desktop fixture."""
import csv
import sys
from pathlib import Path


def check(path):
    with path.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    fields = ("success", "funded", "realized_net_eur", "near_n", "low_n", "high_n")
    actual = {r["probability"]: tuple(int(r[k]) for k in fields) for r in rows}
    expected = {
        "0.5999999": (1, 0, 0, 1, 1, 0),
        "0.6":       (1, 0, 0, 1, 1, 0),
        "0.6000001": (0, 1, -1500, 1, 0, 1),
    }
    if len(rows) != 3 or actual != expected:
        raise ValueError(f"Funding / calibration boundary mismatch: {actual}")
    print("PASS: 60% excluded from funding and included only in the lower sub-band.")


if __name__ == "__main__":
    check(Path(sys.argv[1]))
