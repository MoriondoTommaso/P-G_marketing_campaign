"""Extra 2: does our own data suggest new data would help? (26 Nov 2026)

Checks behind docs/additional-data.md ("What our data says about the value of new data").
The tree's errors are taken from its rule at the 60% threshold:
fund if Distance from a Dentist <= 56.07 (100 / 8 / 8 / 54 on the 170 stores).

Run from the repo root:  python3 scripts/extra2_value_checks.py   (needs pandas, numpy)
"""
from math import asin, cos, radians, sin, sqrt

import numpy as np
import pandas as pd

u = pd.read_csv("outputs/store-universe.csv")
lab = u[u["success"].notna()].reset_index(drop=True)
y = lab["success"].astype(int).values
fund = (lab["Distance from a Dentist"] <= 56.07).values
missed = ~fund & (y == 1)
skipped_fail = ~fund & (y == 0)
funded_fail = fund & (y == 0)
err = missed | funded_fail


def km(a, b, c, d):
    a, b, c, d = map(radians, [a, b, c, d])
    return 6371 * 2 * asin(sqrt(sin((c - a) / 2) ** 2 + cos(a) * cos(c) * sin((d - b) / 2) ** 2))


lat, lon = lab["Latitude"].values, lab["Longitude"].values
D = np.array([[km(lat[i], lon[i], lat[j], lon[j]) for j in range(len(lab))] for i in range(len(lab))])
np.fill_diagonal(D, np.inf)
nn, nd = D.argmin(1), D.min(1)

print(f"Tree errors: {err.sum()} (missed successes {missed.sum()}, funded failures {funded_fail.sum()})")
for r in [1, 2, 5]:
    m = nd <= r
    print(f"Stores with an activated neighbour within {r} km: {m.sum()}, same result: {(y[m] == y[nn[m]]).mean():.0%}")
print(f"Errors whose nearest activated store had the opposite result: {(y[err] != y[nn[err]]).sum()} of {err.sum()}")

M = D[np.ix_(missed, missed)]
close = [(row[np.isfinite(row)] <= 15).sum() for row in M]
print("Missed successes with another missed success within 15 km:", sum(c > 0 for c in close), "of", missed.sum())

c = "Online Consumption IYA"
print(f"{c} medians: missed successes {lab[c][missed].median()}, failures skipped {lab[c][skipped_fail].median()}")
