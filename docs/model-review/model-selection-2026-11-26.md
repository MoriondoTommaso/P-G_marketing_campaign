# Which model should select Oral-B campaign stores?

**Status:** This review's original tree-first recommendation, retained below for provenance, was superseded by the [final Random Forest decision](../final-model-decision.md) after the [feature interpretation and retraining checks](forest-interpretability.md). The validation results and geographic limitations still apply.

**Original review recommendation:** Keep the Decision Tree as the primary **pilot targeting rule** for the class submission. Use the Random Forest as the **challenger** and deliberately test stores where the two disagree. The forest is the better predictor on ordinary held-out stores. There is no consistent evidence that replacing the tree would increase net value when targeting new locations. Neither model has earned a national rollout.

## What was independently verified

Reviewed remote `main` at `6e1f081ff3774184fce1d9e452964fc805e455ab`. The [final class workflow](../../workflows/oral-b-italy-final.knwf) is byte-identical to the one at [issue #49](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/49)'s audited commit `1a710c5` (workflow SHA-256 `8073a6174337dc1c2a7666b0b3e5dc03581e7d8c8f1349f9b68547cf60d74634`). The later rerun evidence did not change the model. RC3 is a different specification.

A reset copy run with the repository's [native integration harness](../../validation/issue31/native/run.py) in KNIME 5.12.1 wrote all seven CSVs into an empty directory; every file matched the published reference byte-for-byte. For the comparisons below, disposable workflow copies ran the original linkage, learner and predictor nodes on the embedded workbooks. These are fresh native fits, not sklearn substitutes. Scores were reconciled by store ID and outcome. The original-order tree probabilities reproduced the published values at **all 480 IDs**. The release fault-injection suite was not repeated in this model review.

All candidates received the final five predictors: dentist distance, water hardness, school count, total population and household income. The class tree is the native Gini/MDL-pruned decision tree, minimum node setting 10; it is **not** RC3's depth-limited tree. The forest uses 100 bootstrapped Gini trees, square-root feature sampling per split, seed 2026 and hard voting. Logistic regression uses the class SAG configuration and training-partition normalization. No hyperparameters or funding thresholds were tuned. The original [evaluation protocol](../evaluation.md) compared logistic and tree, not forest; extending its economic criterion to a third candidate is a retrospective amendment.

## Model evidence

The case pays €1,000 net for a funded success, loses €1,500 on a funded failure and assigns €0 to skipping. A store therefore qualifies only if `p(success) > 0.60`. The primary metric below is net on **observed held-out labels**, not each model's own forecast. Activate-all earns €15,000 and activate-none €0 on these same 170 stores.

| Validation on 170 historical activations | Decision Tree | Random Forest | Logistic |
|---|---:|---:|---:|
| Submitted five folds | €88,000 | **€90,500** | €85,000 |
| Protocol's ID-based folds, current learners/features | €86,000 | **€90,500** | €84,500 |
| 11 ID-based five-fold assignments, mean | €87,045 | **€89,455** | €83,864 |
| Leave one geographic cell out, 44 cells | €83,500 | **€84,000** | €83,500 |
| Same cells; exclude training stores within 15 km of test stores | **€83,500** | €82,000 | **€83,500** |
| Five geographic folds with a 30 km exclusion, 11 assignments, mean | **€85,909** | €77,909 | €78,955 |

**The forest's ordinary-fold advantage is real but modest.** On the submitted split both models funded 108 stores at the same €162,000 spend. The tree funded 100 successes and eight failures; the forest funded 101 and seven. Eight identities changed, not one: the four forest-only stores all succeeded; the four tree-only stores included three successes and one failure. Original pooled Brier/AUC: forest **0.0663/0.9256**, tree **0.0864/0.8638**, logistic **0.0800/0.9125**. Across 11 ID-based assignments, forest beat tree on net nine times, tied once and lost once (paired difference −€1,500 to +€6,500). It had better Brier and AUC in all 11. Neither tree nor forest had an original held-out score in 55–65%; better overall Brier does not establish calibration at break-even.

**Geographic transfer changes the decision.** Median distance to the nearest *other* labeled store is 2.3 km for historical stores. For the 310 previously unactivated stores the median distance to a labeled store is 34.4 km; 167 are at least 30 km away. Ordinary folds can give an easier task than national targeting. The one-cell holdout with the 15 km exclusion yields a 34.2 km median test-to-training distance and retains 148–169 training stores per fit. In this test the forest still had better Brier (0.0835 vs 0.1012) and AUC (0.931 vs 0.829) but **lower net at the required threshold**. It avoided one tree-funded failure in aggregate at the cost of three fewer funded successes.

The 30 km multi-cell stress is deliberately harder (median separation 69.1 km). The tree beat the forest on money on **10 of 11** assignments. The forest still ranked stores better on average (AUC 0.920 vs 0.879), but had worse mean Brier (0.0995 vs 0.0941) and funded about nine fewer successes per assignment. These exploratory designs reuse the same stores; the win counts are sensitivity checks, not independent trials or significance tests. No one blocking geometry measures the national deployment distribution.

**The strongest counterexample to using the tree everywhere:** training only below 43°N and testing north, the tree funded all 119 northern stores and lost **€23,500**; the forest funded 55 and earned **€32,500**. Testing south gave tree **€40,000**, forest **€39,500**. The north-test training set contains just five failures and fails the prespecified minimum of ten. Forest calibration also broke down there: among 49 northern stores scoring 55–65%, only 15 succeeded versus 59.5% mean predicted. Treat this as a warning about regional extrapolation for both models, not a qualification test that the forest passed.

## The threshold and the store list

Reversing the national workbook reproduced the tree's 287 → 289 funded stores and 150 changed probabilities. It also clarifies issue #49's reported forest/tree tie: the forest's raw score for failed store `15596` was `0.6000000238418579`, the serialized representation of **60 votes out of 100**. The raw comparison funds it, giving €85,000 for both models. Excluding the exact tie gives forest **€86,500**, tree **€85,000**. The same trap occurs on an unseen store in the original-order RF refit. For this 100-voter configuration, verify 100 contributing trees and compare the success **vote count > 60**; do not round arbitrary logistic or tree probabilities. In the evidence tables `rf_raw` is the native value and `rf` is its verified vote fraction.

For a like-for-like planning scenario, the review used the protocol's ID folds, numeric-ID-sorted training partitions, held-out scores for the 170, and an all-170 refit for the 310. This is a diagnostic branch, not a replacement release:

| Model / specification | Repeat stores | New stores | Total | Spend | Model-implied net |
|---|---:|---:|---:|---:|---:|
| Published tree on `main` | 108 | 179 | 287 | €430,500 | €234,153.75 |
| Tree, ID-fold diagnostic | 111 | 179 | 290 | €435,000 | €234,656.01 |
| Forest, same ID-fold diagnostic | 108 | 169 | 277 | €415,500 | €181,950.00 |

Do **not** select the tree because its own forecast is larger. Its full refit assigns only two probabilities to the 310 new stores: 100/108 (92.6%) or 8/62 (12.9%), depending on a single dentist-distance split near 56.07 source units. It cannot distinguish stores within either leaf, and crossing the split changes the estimated return sharply. Dentist proximity is a historical association; the distance unit, feature vintages and 2026 selection mechanism are not established. The forest offers a ranking within those groups, but votes are not automatically calibrated chances of success.

Reversing the workbook on the diagnostic ID folds preserved forest fold membership and all 480 decisions, but changed **one** held-out and **11** unseen RF probabilities by one vote each. Sorting training rows alone did not make the score and finance package invariant. The native success/failure column order also reversed; scores here were always taken by positive-class name. Resolve the remaining order dependence and test store-level score equality before publishing any RF forecast.

## What to submit and what to test

1. **For the presentation:** name the tree as the primary pilot rule, show the ordinary-fold win for the forest and the geographic comparison alongside it, and label the published 287 stores a conditional planning scenario. Explain the dentist-distance association rather than claiming the tree discovered a causal driver. Do not mix an RF store count with tree economics.
2. **For the field test:** the two ID-fold models agree to fund 161 previously unactivated stores; **18 are tree-only and eight forest-only**. Include both disagreement groups, a sample from agreement groups and near-threshold stores. Stratify by geography and proximity to historical activations. Randomize activation versus business-as-usual within strata where feasible, predefine the success measurement and use observed incremental sales and spend. If sampling overrepresents disagreements, weight the policy comparison back to the eligible population. Set the budget, duration, uncertainty criterion and minimum economically worthwhile improvement before launch. Twenty-six disagreements alone cannot settle a national comparison.
3. **Before switching the official scorer:** require prospective evidence that RF targeting improves case net at comparable spend, alongside calibration checks near 60%. Regenerate the 170/310 score sources, activation IDs, finance, Size of Prize and equal-spend benchmark from the same run. Require the input-order and zero-partial-release checks from issue #49 whichever model is used.

## How to check the evidence

- [Per-design metrics](../../validation/T10/model-selection-2026-11-26/metrics.csv) · [held-out scores, labels, store IDs and folds](../../validation/T10/model-selection-2026-11-26/held-out-scores.csv) · [480-store diagnostic comparison](../../validation/T10/model-selection-2026-11-26/national-diagnostic.csv). `dt`, `rf`, `lr` denote tree, forest and logistic; blanks in the national target mean unknown, not failure. National diagnostic scores are not approved activation instructions.
- `reference` and `reversed` use the submitted X-Partitioner settings. `hash-*` uses the protocol's class-specific SHA-256 store-ID ordering and offsets, with the reference seed `20261120` and perturbation seeds `101`–`110`. The reference assignments were checked against `outputs/folds.csv`. Training rows were sorted by numeric ID in the explicit-split diagnostics. Repeats were averaged as 170-store campaigns, never summed.
- Geographic cells are `(floor(2 × latitude), floor(2 × longitude))`. `cell-0km` and `cell-15km` leave each occupied cell out once. `buffer30` assigns each cell to `int(sha256("2026:latCell:lonCell"), 16) mod 5`; suffixes use seeds `101`–`110` instead. Training stores within 30 km of **any** test store were excluded (great-circle distance, radius 6,371 km). `north` and `south` refer to the two opposite-side holdouts at 43°N. Spatial results are exploratory. Every complete design covers 170 unique stores; north/south cover 119/51 separately.
