"""Fail the pre-finance comparison on the first different store, including a single vote."""
from pathlib import Path
import sys

from native_folds import rows


def scores(run, model):
    ids = {r["row ID"]: r["Pdv Code"] for r in rows(run / "identities.csv")}
    result = {}
    for r in rows(run / f"{model}.csv"):
        i = r["Pdv Code"] if model == "refit" else ids[r["row ID"]]
        if i in result:
            raise ValueError(f"duplicate {model} ID {i}")
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
