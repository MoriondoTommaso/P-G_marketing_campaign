# Final submitted KNIME workflow (25 Nov 2026)

**The workflow to submit on MyLuiss is [`workflows/oral-b-italy-final.knwf`](../workflows/oral-b-italy-final.knwf).**
It rebuilds the modelling part with the nodes taught in class (week 2 and week 5) and was agreed with Tommaso
on 25 Nov 2026. `workflows/oral-b-italy.knwf` (RC3) stays in the repo as the earlier team pipeline and is not
the submission.

## How to open it

1. KNIME: **Import workflow** → `workflows/oral-b-italy-final.knwf`.
2. **Execute all.** Nothing to configure: the two Excel inputs travel inside the file (`data/inputs`) and the
   CSV outputs are written inside it (`data/outputs`). No path points to a personal computer.

## What it does

| Part | Nodes (class style) | Result |
|---|---|---|
| Link 2026 activations to stores | Joiner on store code, Joiner on coordinates for the 18 without code, GroupBy checks | 170 stores: 108 success / 62 failure, 310 never activated |
| Anti-leakage | Column Filter keeps only store traits + target | Campaign details, IDs, coordinates and `Online Consumption IYA` are out |
| EDA | GroupBy medians success vs failure, Rule Engine region, Conditional Box Plot, Bar Chart, GroupBy by region | `eda-success-profile.csv`, `eda-region-success.csv`, two charts |
| 2026 baseline | Variable Creator (€2,500 / €1,500), GroupBy, Math Formula | €270,000 sales, €255,000 spend, **€15,000 net** |
| Compare 3 models | X-Partitioner (5 folds, stratified, seed 2026) → Learner → Predictor → X-Aggregator, same folds for all 3 | Scorer, ROC Curve, net € per model |
| Business rule | Rule Engine: fund only if p > 60% (break-even) | Net € per store: +1,000 / −1,500 / 0 |
| 2027 plan | Final tree refit on all 170, scores the 310; held-out scores kept for the 170 | `national-scores-class.csv` (480), `activation-list-class.csv` (287) |

Every one of the 97 nodes has a plain-language comment.

## EDA findings (170 activated stores)

**Successful stores are close to a dentist, and this holds inside every region**, so it is not only a
North/South effect. Source: the KNIME EDA branch (GroupBy #39 and #41 → `outputs/eda-success-profile.csv`,
`outputs/eda-region-success.csv`; GroupBy #106 for the within-region check). The same numbers are reproduced by
[`scripts/eda_region_check.py`](../scripts/eda_region_check.py).

**Charts in the workflow** (open the node's view in KNIME):
- *Conditional Box Plot* (#103), the lab 5 node: "Successful stores are much closer to a dentist". Distance, water
  hardness and schools, success vs failure.
- *Bar Chart* (#105): "Northern stores succeed far less often". Success rate by region, axis from 0 to 1.

| Trait (median) | Success (108) | Failure (62) |
|---|---:|---:|
| Distance from a Dentist | **9.0** | **155.0** |
| Water hardness IDX | 40 | 89 |
| Nr of Schools | 4 | 2 |
| Avg Income per Household | €18,269 | €19,730 |
| Total Population | 130,161 | 168,650 |

| Region (Rule Engine #40) | Successes / activated | Success rate | Never activated |
|---|---:|---:|---:|
| North (lat ≥ 44.5) | 30 / 83 | **36%** | 83 |
| Centre (41.5–44.5) | 44 / 49 | 90% | 117 |
| South (< 41.5) | 34 / 38 | 89% | 110 |

| Distance from a Dentist, median | Success | Failure |
|---|---:|---:|
| North | 18.8 (30 stores) | 157.1 (53 stores) |
| Centre | 3.5 (44) | 70.9 (5) |
| South | 8.3 (34) | 0.3 (4) |

The North is where the model earns its money: it holds most failures, and inside it the dentist distance still
separates successes from failures. Centre and South have only 9 failures together, too few to read. The distance
unit is not stated in the source. These are 2026 associations, not causes. The full trait-by-trait profile,
with separation scores, is in [`store-insights.md`](store-insights.md); its medians match the ones above.

## Model comparison (170 stores, each scored by a model that never saw it)

| Model | Accuracy | Precision | Sensitivity | F1 | AUC | Net € |
|---|---:|---:|---:|---:|---:|---:|
| Random Forest (100 trees) | 91.8% | 93.5% | 93.5% | 93.5% | 0.926 | €90,500 |
| **Decision Tree (chosen)** | 90.6% | 92.6% | 92.6% | 92.6% | 0.864 | **€88,000** |
| Logistic Regression | 89.4% | 90.9% | 92.6% | 91.7% | 0.912 | €85,000 |
| Activate all (2026) | 63.5% | 63.5% | 100% | 77.7% | 0.5 | €15,000 |

**Choice: Decision Tree (team decision with Tommaso).** It is €2,500 below the forest, one store out of 170,
and it is the only model managers can read. Its one rule: distance from a dentist
≤ 56.07 → 100 of 108 stores succeeded; > 56.07 → 54 of 62 failed. Confusion matrix at 60%: 100 funded
successes, 8 funded failures, 8 missed successes, 54 avoided failures.

## Size of Prize

| Scope | Net € |
|---|---:|
| 2026 actual (all 170 activated) | €15,000 |
| Same 170 stores with the model (held-out) | €88,000 (**+€73,000**) |
| 2027 plan, 287 stores, €430,500 spend (forecast) | €234,154 |

The 2027 total splits into €88.3k from 108 stores already activated in 2026 (known result) and €145.9k from
179 new stores (forecast). Propensity buckets: High > 65% = 287, Marginal 55–65% = 0, Low ≤ 55% = 193.
The geographic-transfer and pilot caveats in [`model-choice.md`](model-choice.md) still apply.

## Amendment: the 5 model features

**Decision (25 Nov 2026, team): keep the final workflow's 5 features; do not change the model.**

| | Features |
|---|---|
| Final workflow | Distance from a Dentist, Water hardness IDX, Nr of Schools, Total Population, Avg Income per Household |
| Frozen protocol (`evaluation.md`) | Distance from a Dentist, Total Population, Avg Income per Household, Households avg components, Nr of Hygienists |

**Why this needs recording.** Water hardness and schools were added after the protocol was frozen.
Features chosen by looking at the same 170 outcomes can make a cross-validated result look better than it is.

**Evidence that the result does not depend on the choice.** [`scripts/feature_robustness_check.py`](../scripts/feature_robustness_check.py),
20 × stratified 5-fold CV, p > 60% rule. It is a scikit-learn approximation of the KNIME nodes, so compare rows
with each other, not with KNIME's €88,000.

| Features given to the tree | Avg net € | Avg AUC |
|---|---:|---:|
| Final 5 | €82,850 | 0.938 |
| All 32 allowed traits | €82,850 | 0.937 |
| Protocol 5 | €85,425 | 0.929 |

"Allowed" = every column of `Italian_Stores.xlsx` except store code, latitude, longitude and
`Online Consumption IYA`. Given all 32, the tree chooses Distance from a Dentist by itself (86% of its splits)
and reaches the same net. The dentist distance carries the model whichever set is used.

**Q&A answer:** "We checked: if we give the tree all 32 store traits, it picks distance from a dentist by itself
and earns the same profit. The result does not depend on our choice of features."
**Do not say** the 5 features were fixed beforehand: they were not.
