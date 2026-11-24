"""Check the native predictor tap and downstream economics for the held-out row."""
import csv
from decimal import Decimal
from pathlib import Path
import sys


def row(path):
    with path.open(newline="") as stream:
        result, = csv.DictReader(stream)
    return result


def check(directory):
    raw = row(directory / "raw.csv")
    base = row(directory / "base.csv")
    if raw["case"] != "held_out" or base["case"] != "held_out":
        raise SystemExit("Missing held-out prediction")
    fields = (raw["P (target=success)"], base["p_success"],
              base["expected_net_eur"], base["recommend_activate"])
    print("raw=%s policy_probability=%s expected_net_eur=%s recommend_activate=%s" % fields)
    if tuple(map(Decimal, fields)) != tuple(map(Decimal, ("0.6000000238418579", ".6", "0", "0"))):
        raise SystemExit("FAIL: expected the widened 6/10 prediction and an unfunded zero-net tie")
    print("PASS: trained 6/10 leaf; held-out tie is unfunded")


if __name__ == "__main__":
    check(Path(sys.argv[1]))
