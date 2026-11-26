"""Fail the pre-finance comparison on the first different store, including a single vote."""
from pathlib import Path
import sys
import math
import struct

from native_folds import rows


def check_funded(records, expected):
    ids = [r["store_id"] for r in records]
    if len(set(ids)) != len(ids) or set(ids) != expected:
        raise ValueError("funded IDs do not match Decision B")


def votes(raw, denominator):
    if denominator != "100":
        raise ValueError(f"expected 100 contributing trees; got {denominator}")
    p = float(raw)
    if not math.isfinite(p) or not 0 <= p <= 1:
        raise ValueError(f"invalid probability {raw}")
    n = round(p * 100)
    exact = n / 100
    widened, = struct.unpack("f", struct.pack("f", exact))
    if p not in (exact, widened):
        raise ValueError(f"off-grid success probability {raw}")
    return n


def scores(run, model):
    ids = {r["row ID"]: r["Pdv Code"] for r in rows(run / "identities.csv")}
    result = {}
    for r in rows(run / f"{model}.csv"):
        i = r["Pdv Code"] if model == "refit" else ids[r["row ID"]]
        if i in result:
            raise ValueError(f"duplicate {model} ID {i}")
        if model in ("forest", "refit"):
            votes(r["P (target=success)"], r["model count"])
        result[i] = (r.get("fold #"), r["P (target=success)"], r.get("model count"))
    return result


if __name__ == "__main__":
    a, b = map(Path, sys.argv[1:])
    for model in ("tree", "logistic", "forest", "refit"):
        original, reversed_ = scores(a, model), scores(b, model)
        for i in sorted(original.keys() | reversed_.keys()):
            if original.get(i) != reversed_.get(i):
                raise ValueError(f"{model} {i}: original {original.get(i)}, reversed {reversed_.get(i)}")
        print(f"{model}: {len(original)} keyed results identical")
