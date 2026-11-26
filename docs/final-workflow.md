# Class KNIME workflow: Random Forest

**Current candidate:** [`oral-b-italy-final.knwf`](../workflows/oral-b-italy-final.knwf) uses no Java Snippets. Table Creator #150 lists the five groups used to test the models. Joiner #151 matches each historical store to its group by store ID; Sorter #159 puts the groups in order. This lookup is fixed for the 170 labeled stores in the supplied workbooks. See the [Team 2 checkpoint and current comparison](../handoff/pre-finance-check.md) for verification and submission status.

## Earlier submission at `7fc7ff8` (historical instructions and figures)

The instructions and numbers below describe the [earlier archive](https://github.com/MoriondoTommaso/P-G_marketing_campaign/blob/7fc7ff8/workflows/oral-b-italy-final.knwf).
It rebuilds the modelling part with the nodes taught in class (week 2 and week 5). Since 26 Nov 2026 the
**Random Forest scores every store.** Under [confirmed Decision B](final-model-decision.md), the 2026 result selects repeats and forest votes select new stores;
the Decision Tree stays as the simple one-rule benchmark and logistic regression as a cross-check.
`workflows/oral-b-italy.knwf` (RC3) stays in the repo as the earlier team pipeline and is not the submission.

## How to open it

1. KNIME: **Import workflow** → `workflows/oral-b-italy-final.knwf`.
2. **Execute all.** Nothing to configure: the two Excel inputs travel inside the file (`data/inputs`) and the
   CSV outputs are written inside it (`data/outputs`). A few nodes still store an old local path as a hidden
   default, but the workflow-relative variables override it, so nothing needs changing on another computer.

## What it does

| Part | Nodes (class style) | Result |
|---|---|---|
| Link 2026 activations to stores | Joiner on store code, Joiner on coordinates for the 18 without code, GroupBy checks | 170 stores: 108 success / 62 failure, 310 never activated |
| Anti-leakage | Column Filter keeps only store traits + target | Campaign details, IDs, coordinates and `Online Consumption IYA` are out |
| EDA | GroupBy medians success vs failure, Rule Engine region, Conditional Box Plot, Bar Chart, GroupBy by region | `eda-success-profile.csv`, `eda-region-success.csv`, two charts |
| 2026 baseline | Variable Creator (€2,500 / €1,500), GroupBy, Math Formula | €270,000 sales, €255,000 spend, **€15,000 net** |
| Compare 3 models | X-Partitioner (5 folds, stratified, seed 2026) → Learner → Predictor → X-Aggregator, same folds for all 3 | Scorer, ROC Curve, net € per model |
| Business rule | Rule Engine: a new store is funded only if more than 60 of the 100 trees vote success (break-even 60%; a 60-vote tie is not funded); the 170 stores activated in 2026 follow their real result (decision B) | Net € per store: +1,000 / −1,500 / 0 |
| 2027 plan | Forest test-fold scores for the 170 activated stores; a final forest (same settings, all 170) scores the 310; Math Formula rounds every score to the exact vote share (votes ÷ 100); Rule Engine #94 funds the 108 stores that succeeded in 2026 and the new stores with more than 60 votes | `national-scores-class.csv` (480), `activation-list-class.csv` (276) |
| Size of Prize | Rule-based Row Filter, GroupBy ×2, Joiner ×2, Math Formula ×2 (#143–#149) | Plan vs 2026 actual and vs repeating the 2026 list |
| Model charts (right of the comparison) | ROC of all three models, net € by model, forest variable importance, logistic coefficients, tree with and without pruning | See *Model comparison* |
| Extra 2 (bottom row) | CSV Reader of OpenStreetMap counts, Joiner, Column Filter, a copy of the forest row | Forest + 3 OSM counts: €88,000 vs €90,500 without, so OSM is dropped ([`additional-data.md`](additional-data.md#osm-test-result-26-nov-2026)) |

Every one of the 137 nodes has a plain-language comment. Built and tested in KNIME 5.12.1.

## EDA findings (170 activated stores)

**Successful stores are close to a dentist, and the gap holds inside the North**, where 53 of the 62 failures are
(median 18.8 vs 157.1), so it is not only a North/South effect. Centre and South have too few failures to test. Source: the KNIME EDA branch (GroupBy #39 and #41 → `outputs/eda-success-profile.csv`,
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
| **Random Forest, 100 trees (chosen)** | 91.8% | 93.5% | 93.5% | 93.5% | 0.926 | **€90,500** |
| Decision Tree (benchmark) | 90.6% | 92.6% | 92.6% | 92.6% | 0.864 | €88,000 |
| Logistic Regression (cross-check) | 89.4% | 90.9% | 92.6% | 91.7% | 0.912 | €85,000 |
| Activate all (2026) | 63.5% | 63.5% | 100% | 77.7% | 0.5 | €15,000 |

**Choice: Random Forest (team decision, 26 Nov 2026, [#51](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/51)).**
On the 170 held-out stores it earns the most (€90,500) and ranks stores best (AUC 0.926). Confusion matrix at the
vote rule: 101 funded successes, 7 funded failures, 7 missed successes, 55 avoided failures. Its gain over the
tree is modest (€2,500) and the tree wins in Tommaso's harder geographic tests
([independent geographic comparison](https://github.com/MoriondoTommaso/P-G_marketing_campaign/blob/0e35db52845d135ae86a7ca39b9c5f38b6d3797f/docs/model-review/model-selection-2026-11-26.md)), so the list is a
**bounded pilot plan**, not proven national profitability.

**What the forest relies on** (chart #127, splits ÷ candidates over the top 3 levels of the 100 trees): distance from
a dentist 2.17, water hardness 1.51, schools 1.37, income 0.95, population 0.69. The logistic cross-check (chart #131,
standardised, + = higher odds of success) agrees: distance from a dentist −2.61, schools +1.59. These are associations,
not causes.

**Tree benchmark, with and without pruning** (#87 and #141). With MDL pruning the tree keeps one rule: distance from a
dentist ≤ 56.07 → 100 of 108 succeeded; > 56.07 → 54 of 62 failed. Without pruning it grows 7 leaves, but most extra
splits do not change any decision, and the one that does (far from a dentist but more than 5.5 schools) rests on 13
stores, 8 of them successes: the kind of rule pruning removes to avoid overfitting.

## Size of Prize

| Scope | Stores | Spend | Net € |
|---|---:|---:|---:|
| 2026 actual (all 170 activated) | 170 | €255,000 | €15,000 |
| Same 170 stores with the forest (held-out, observed outcomes) | 108 | €162,000 | €90,500 (**+€75,500**) |
| **2027 plan (forecast, forest probabilities)** | **276** | **€414,000** | **€182,250** |
| of which the 108 stores that succeeded in 2026 | 108 | €162,000 | €77,525 |
| of which new stores | 168 | €252,000 | €104,725 |
| 2027 plan, best case (every 2026 success repeats) | 276 | €414,000 | €212,725 |

The 2027 figures are expected values (2,500 × p − 1,500 per funded store, p = forest probability); the €90,500
backtest uses observed outcomes. The plan is expected to make **€182,250**, or €212,725 if every 2026 success repeats;
the downside cases in the [financial report](financial-report-class.html) go below zero if the probabilities are 30 points too optimistic.

Compared with the 2026 actual result, the plan forecasts **€167,250 more net**. Compared with repeating all 170
historical stores in 2027 (forecast €13,275), it forecasts **€168,975 more net** and costs €159,000 more.
At equal spend (€255,000, k = 170), targeting the top 170 stores forecasts **€130,100 more net** than repeating the
original 170. These are model-implied comparisons, not measured lift. The first two are computed in KNIME (nodes #143–#149,
bottom right of the plan); the equal-spend comparison and the stress test are computed by the script below.

**Stress test** (new-store scores in 55–65% moved by ±5 points; repeat stores stay fixed): 272 stores and €181,900
(lower) to 284 stores and €183,200 (upper); 4 stores drop out, 8 come in. Store-level detail in
[`sensitivity-class.csv`](../outputs/sensitivity-class.csv); totals in
[`financial-summary-class.csv`](../outputs/financial-summary-class.csv), both generated from this run by
[`scripts/rf_finance_package.py`](../scripts/rf_finance_package.py). The [financial report](financial-report-class.html)
([PDF](financial-report-class.pdf)) uses the same figures.

Display buckets (they do not decide funding): High > 65% = 272, Marginal 55–65% = 18, Low < 55% = 190.

**Decision B (team, 26 Nov 2026, #51): the 170 stores activated in 2026 follow their real result.** All 108 that
succeeded are in the plan and none of the 62 that failed. Before this decision the forest's score decided, which
re-funded 7 stores that had failed (68672, 2006331, 23781, 97240, 71884, 98235, 79237) and left out 7 that had
succeeded (2007481, 77034, 28340, 20013, 30967, 8914, 109086). On the real 2026 results the swap is worth +€17,500
(7 failures avoided, 7 successes kept); the model-based forecast falls by €8,950 because the forest still rates the
7 kept successes as risky (33–54%). The plan size and spend are unchanged. As a result, 7 funded repeat stores show a negative expected € in
`national-scores-class.csv` and 7 left-out ones a positive one: this is deliberate, not an error.

**Deferred engineering checks (team, 26 Nov 2026, #51).** Store-ID-based (hash) folds, the reversed-input proof and an
automatic release gate with fault tests are not implemented: they cannot be built with the class nodes. Known limitation:
results are exactly reproducible with the files as delivered; changing the row order of the input files can move a few
scores by one vote. The geographic-transfer and pilot caveats in [`model-choice.md`](model-choice.md) still apply.

## Amendment: the 5 model features

**Decision (25 Nov 2026, team): keep the final workflow's 5 features; do not change the model.**

| | Features |
|---|---|
| Final workflow | Distance from a Dentist, Water hardness IDX, Nr of Schools, Total Population, Avg Income per Household |
| Frozen protocol (`evaluation.md`) | Distance from a Dentist, Total Population, Avg Income per Household, Households avg components, Nr of Hygienists |

**Why this needs recording.** Water hardness and schools were added after the protocol was frozen.
Features chosen by looking at the same 170 outcomes can make a cross-validated result look better than it is.

**Evidence that the choice barely changes the result.** [`scripts/feature_robustness_check.py`](../scripts/feature_robustness_check.py),
20 × stratified 5-fold CV, p > 60% rule. It is a scikit-learn approximation of the KNIME nodes, so compare rows
with each other, not with KNIME's €88,000.

| Features given to the tree | Avg net € | Avg AUC |
|---|---:|---:|
| Final 5 | €82,850 | 0.938 |
| All 32 allowed traits | €82,850 | 0.937 |
| Protocol 5 | €85,425 | 0.929 |

"Allowed" = every column of `Italian_Stores.xlsx` except store code, latitude, longitude and
`Online Consumption IYA`. Given all 32, the tree chooses Distance from a Dentist by itself (86% of the tree's feature importance)
and reaches the same net. The dentist distance carries the model whichever set is used.

**Q&A answer:** "We checked: if we give the tree all 32 store traits, it picks distance from a dentist by itself
and earns the same profit. The result hardly changes with our choice of features."
**Do not say** the 5 features were fixed beforehand: they were not.

The robustness check above was run on trees. The chosen forest uses the same 5 features.
