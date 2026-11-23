"""T07 (#7): store profiles from the KNIME export.

Reads   outputs/store-universe.csv  (480 stores, from the T05 KNIME workflow)
Writes  outputs/store-profiles.csv

Only describes the data. Nothing is normalised, filled or removed, and the
310 never-activated stores stay "unknown", never "failure".

Run from the repository root:
    python scripts/t07_store_profiles.py
"""
import sys

import numpy as np
import pandas as pd

SRC = sys.argv[1] if len(sys.argv) > 1 else "outputs/store-universe.csv"
OUT = sys.argv[2] if len(sys.argv) > 2 else "outputs/store-profiles.csv"

# Team 3's five predictors, from docs/evaluation.md
MODEL_PREDICTORS = ["Total Population", "Avg Income per Household", "Households avg components",
                    "Nr of Hygienists", "Distance from a Dentist"]

# Traits shown by success rate per third of the labelled stores
TERCILE_TRAITS = ["Distance from a Dentist", "Water hardness IDX", "Online Consumption IYA", "Nr of Schools"]

# Notes agreed in Team 2 (see docs/runbook.md, T05 data audit)
NOTES = {
    "Online Consumption IYA": "timing unknown (may be measured after the 2026 campaign); not a driver; "
                              "kept out of the model, slides and Extra 2",
    "Distance from a Dentist": "unit not stated in source",
    "Water hardness IDX": "index, base not stated in source; higher/lower only",
}

u = pd.read_csv(SRC)

# Sanity checks on the input
assert len(u) == 480 and u["store_id"].is_unique, "expected 480 unique stores"
grp = u["success"].map({1: "success", 0: "failure"}).fillna("unknown")
assert grp.value_counts().to_dict() == {"unknown": 310, "success": 108, "failure": 62}, "expected 108 / 62 / 310"

u["label_status"] = np.where(grp == "unknown", "never_activated", "activated")
u["region_band"] = np.where(u["Latitude"] < 41.5, "South/islands (lat < 41.5)",
                   np.where(u["Latitude"] < 44.5, "Centre (41.5 <= lat < 44.5)", "North (lat >= 44.5)"))
u["fallback_band"] = np.where(u["Latitude"] < 43.0, "South (lat < 43.0)", "North (lat >= 43.0)")

# Every numeric store trait; labels and helper columns are left out
not_traits = {"store_id", "success", "target", "label_status", "region_band", "fallback_band"}
traits = [c for c in u.columns if c not in not_traits]


def stats(s):
    return dict(n=int(s.notna().sum()), mean=s.mean(), median=s.median(),
                p25=s.quantile(0.25), p75=s.quantile(0.75), min=s.min(), max=s.max())


def separation(a, b):
    """Share of (a, b) pairs where the a value is higher; ties count half.
    0.5 = no difference. Same as the AUC of that one trait."""
    a, b = a.values, b.values
    return (a[:, None] > b[None, :]).mean() + 0.5 * (a[:, None] == b[None, :]).mean()


rows = []
labelled = u[grp != "unknown"]
north = labelled[labelled["Latitude"] >= 43.0]

# 1. Success vs failure, and activated vs never activated, for every trait
for t in traits:
    s = u.loc[grp == "success", t]
    f = u.loc[grp == "failure", t]
    k = u.loc[grp == "unknown", t]
    score = separation(s, f)
    score_north = separation(north.loc[north["success"] == 1, t], north.loc[north["success"] == 0, t])
    gap = abs(score - 0.5)
    strength = "strong" if gap >= 0.2 else "moderate" if gap >= 0.1 else "weak / none"
    outside = int(((k < labelled[t].min()) | (k > labelled[t].max())).sum())

    for name, ser in (("success", s), ("failure", f), ("activated_all", labelled[t]), ("never_activated", k)):
        r = dict(comparison="success_vs_failure" if name in ("success", "failure") else "activated_vs_never",
                 trait=t, group=name, **stats(ser), note=NOTES.get(t))
        if name == "success":
            r.update(auc_success_vs_failure=round(score, 3), auc_within_north_lat43=round(score_north, 3),
                     direction="higher in successes" if score > 0.5 else "lower in successes",
                     separation=strength)
        if name == "never_activated":
            r["never_activated_outside_labelled_range"] = outside
        rows.append(r)

# 2. Store counts per latitude band
for col in ("region_band", "fallback_band"):
    for band, d in u.groupby(col):
        g = grp[d.index]
        activated = (g != "unknown").sum()
        rows.append(dict(comparison=f"geography_{col}", trait=col, group=band, n=len(d),
                         n_success=int((g == "success").sum()), n_failure=int((g == "failure").sum()),
                         n_never_activated=int((g == "unknown").sum()),
                         success_rate_among_activated=round((g == "success").sum() / max(activated, 1), 3)))

# 3. Success rate in each third of the labelled stores, plus how many never-activated stores fall there
for t in TERCILE_TRAITS:
    _, edges = pd.qcut(labelled[t], 3, retbins=True, duplicates="drop")
    edges[0], edges[-1] = -np.inf, np.inf
    lab_bins = pd.cut(labelled[t], edges)
    unk_bins = pd.cut(u.loc[grp == "unknown", t], edges)
    for b in lab_bins.cat.categories:
        d = labelled[lab_bins == b]
        rows.append(dict(comparison="trait_tercile", trait=t, group=str(b), n=len(d),
                         n_success=int(d["success"].sum()), n_failure=int((d["success"] == 0).sum()),
                         n_never_activated=int((unk_bins == b).sum()),
                         success_rate_among_activated=round(d["success"].mean(), 3), note=NOTES.get(t)))

# 4. Team 3's predictors: activated vs never activated inside each band
for t in MODEL_PREDICTORS:
    for band, d in u.groupby("region_band"):
        a = d.loc[d["label_status"] == "activated", t]
        k = d.loc[d["label_status"] == "never_activated", t]
        for name, ser in (("activated", a), ("never_activated", k)):
            r = dict(comparison="model_predictor_by_band", trait=t, group=f"{band} | {name}",
                     **stats(ser), note=NOTES.get(t))
            if name == "never_activated":
                r["never_activated_outside_labelled_range"] = int(((k < a.min()) | (k > a.max())).sum())
            rows.append(r)

cols = ["comparison", "trait", "group", "n", "n_success", "n_failure", "n_never_activated",
        "success_rate_among_activated", "mean", "median", "p25", "p75", "min", "max",
        "auc_success_vs_failure", "auc_within_north_lat43", "direction", "separation",
        "never_activated_outside_labelled_range", "note"]
pd.DataFrame(rows).reindex(columns=cols).to_csv(OUT, index=False, float_format="%.6g", lineterminator="\n")
print(f"wrote {OUT}: {len(rows)} rows")
