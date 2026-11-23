# T10 — choosing a model for the funding decision

**Ordinary-fold choice: the shallow tree.** On the same 170 held-out stores, it
returned €88,000 net, €4,000 more than logistic regression. That exceeds the
prespecified €2,500 tie tolerance, so no Brier tie-break was needed. This is one
depth-limited tree on the five approved features, not an unrestricted ensemble.

| Ordinary validation | Funded | Funded successes / failures | Pooled net | Brier | Fold net range |
|---|---:|---:|---:|---:|---:|
| Training-rate baseline | 170 | 108 / 62 | €15,000 | 0.23181 | €1,500–€4,000 |
| Logistic regression | 104 | 96 / 8 | €84,000 | 0.11341 | €8,500–€21,000 |
| Shallow tree | 108 | 100 / 8 | €88,000 | 0.08081 | €8,500–€21,000 |

Activate-all returned €15,000; activate-none returned €0. The baseline funded
everyone. The tree exceeded activate-all in all five folds, but its weakest fold
returned only €8,500. The €73,000 pooled difference is a retrospective comparison
under the case's sales and spend assumptions, not a forecast of national gains.

**The funding boundary is poorly supported.** In the inclusive 55–65% band,
4 tree scores averaged 61.54% and all 4 stores succeeded. None scored in the
55–60% sub-band. Logistic had 5 scores in the full band (2 at or below 60%, 3
above) and all 5 succeeded. These cells are too small to establish calibration.
The baseline had all 170 in the upper sub-band; its mean score and observed
success rate both equal 63.53%. This agreement does not distinguish stores.

## Geographic transfer and deployment

The predefined three-band split fails its support gate: south has 34 successes
but only 4 failures (minimum 5). Centre has 44/5 and north 30/53; holding out
the north leaves only 9 failures for training (minimum 10). The 43°N
fallback also fails. The southern test band has 46 successes and 5 failures,
and the northern test band has 62/57. When testing in the north, the southern
**training** complement has only 5 failures (minimum 10).

**Qualifying geographic validation: unavailable.** The following opposite-band
refits are retained for exploration only (`validation=spatial_exploratory`).
Each cell gives **funded count / realized net**.

| Held-out latitude band | Activate all | Training-rate baseline | Logistic | Shallow tree |
|---|---:|---:|---:|---:|
| South (<43°), 51 stores | 51 / €38,500 | 0 / €0 | 38 / €28,000 | 50 / €40,000 |
| North (≥43°), 119 stores | 119 / −€23,500 | 119 / −€23,500 | 106 / −€36,500 | 119 / −€23,500 |
| Pooled, 170 stores | 170 / €15,000 | 119 / −€23,500 | 144 / −€8,500 | 169 / €16,500 |

Activate-none earns €0 in each band. Against the strongest pooled spatial
reference (activate-all), the tree's advantage stays positive but falls from
€73,000 to **€1,500**: it avoids one failed southern activation and funds the
entire north. Logistic falls €23,500 below activate-all. Pooled spatial Brier
scores are 0.34634 (baseline), 0.39088 (logistic) and 0.33352 (tree). No tree
scores fell within 55–65% in this check, so calibration near the funding boundary
cannot be assessed. Logistic had 11 there; all succeeded against a mean prediction
of 60.02%, a +39.98 percentage-point gap that exceeds the protocol's warning
threshold. The [comparison CSV](../outputs/model-comparison.csv) reports every
band, fold, control and calibration sub-band, including empty bins.

[T07's coverage comparison](store-insights.md) shows why ordinary cross-validation
alone is insufficient: the primary southern, central and northern bands contain
110, 117 and 83 never-activated stores respectively. Among southern stores, 35
of 110 never-activated sites lie outside the activated range for dentist distance;
the median shifts from 5.7 to 22.4 source units. In the central band it shifts
from 3.5 to 65.8. The five source fields have no confirmed measurement dates.

**Choose the shallow tree for pilot planning, not national rollout.** The choice
rests on ordinary folds; the exploratory €1,500 difference does not establish
geographic robustness. Use a **bounded pilot**, with outcomes collected near 60% and
in underrepresented profiles before expanding. The campaign locations were not
randomly selected. These folds both compare and select the model, their training
sets overlap, and a latitude boundary does not fully separate nearby stores.
Neither validation design measures performance at the 310 never-activated sites.

**Verify:** `python3 validation/T10/check.py` reconciles the release decision
rows and the [separate spatial audit](../validation/T10/spatial-decisions.csv)
against all 27 comparison rows. To reproduce in KNIME, import the workflow,
point #34 to `data/` and #35 to a writable output folder, then reset and execute
all. Block **06 Decide funding** writes `spatial-decisions.csv` beside the ordinary
decisions. Pass that fresh output folder to the checker; it also requires the
score and universe files from that same run.
