# Independent Model Review — P&G Oral-B Italy 2027

**Review date:** 23 November 2026  
**Prepared for:** Tommaso, Ele, and the Teams 2–4 release review  
**Review coordinated by:** Lorenzo Pazienza (Team 1)  
**Scope:** T08–T12 predictive models, financial decisions, and downstream release requirements  
**Reference implementation:** Local release candidate at commit `c23610a`, reviewed using KNIME Analytics Platform 5.12.0

> **Verdict: MAJOR REVISION REQUIRED for national-rollout claims.** The workflow is reproducible on the reviewed inputs, and the shallow Decision Tree is the supported model for retrospective comparison and pilot design. The current 278-store list and €250,602.05 model-implied net forecast **do not establish reliable prospective national performance**. Distinguish implementation defects from limitations of the available evidence.

## 1. What passed

The independent local review reported a successful KNIME rerun of the release workflow, byte-for-byte agreement with the committed outputs, and an input-order invariance check. The 480-store universe, 170 labeled activations, 18 exact-coordinate recoveries, five shared stratified folds, and exported financial arithmetic reconciled on the reviewed candidate. No predictive models were retrained or modified as part of the review.

| Retrospective OOF metric | Training-rate baseline | Logistic regression | Shallow Decision Tree |
|---|---:|---:|---:|
| Brier score (lower is better) | 0.231812 | 0.113414 | **0.080815** |
| ROC AUC | 0.485 | 0.867 | **0.934** |
| Stores funded on held-out scores | 170 | 104 | **108** |
| Realized case net on held-out outcomes | €15,000 | €84,000 | **€88,000** |

The tree meets the [predefined model-selection protocol](../evaluation.md), but its €4,000 net advantage over logistic regression comes from **four additional funded successes**. Model selection and performance reporting use the same OOF outcomes; the selected winner's reported results may therefore be optimistic. The sample is too small to establish prospective superiority.

## 2. Findings requiring action

### P0 — Correct the strict 60% break-even comparison (implementation defect)

- **Observed:** A native KNIME tree leaf with 6 successes out of 10 produces `0.6000000238418579` (single-precision representation), which passes a literal `p > 0.60` comparison although the exact rate is 60%.
- **Evidence:** Local synthetic native-node test; release workflow node references `#143`, `#337`, `#348–350`.
- **Impact:** Incorrect inclusion of exact break-even leaves on other inputs. **No published 278-store recommendation changes on the reviewed data.**
- **Fix / acceptance test:** Evaluate the tree leaf's exact success-to-total ratio where leaf counts are available (e.g., `5 × success_count > 3 × leaf_count`), and apply the same rule consistently in sensitivity scenarios. Add a regression fixture through the actual native predictor with a 6/10 leaf. If exact counts cannot be used, document and test an equivalent policy-preserving comparison rather than rounding indiscriminately.

### P0 — Prevent silent data loss and duplicates at export (release-engineering defect)

- **Observed:** Inner joins can discard unmatched rows; audit branches do not stop export. Within-fold score joins use `store_id` alone instead of the specified `(store_id, fold)` identity; the national score union lacks a blocking uniqueness assertion.
- **Evidence:** Workflow blocks `01` (`#6`, `#8`, `#32`, `#37`), `04` (`#121–122`), and `10` (`#335`).
- **Impact:** No defect affected the current reviewed exports, but changed inputs could silently generate an incomplete or duplicated recommendation list.
- **Fix / acceptance test:** Fail the workflow on unmatched or conflicting activation links; assert exactly 170 unique historical labels, one OOF prediction per `(store_id, model)`, fold-consistent joins, 480 unique national scores, and exactly 170 historical plus 310 previously unactivated IDs before any final writer runs.

### P1 — Geographic generalization is not demonstrated (statistical validity)

- **Observed:** Both geographic support gates fail. In an exploratory cross-band test, the tree funded all 119 northern test stores and generated **−€23,500 realized case net**. The tree's pooled exploratory geographic Brier score rose to **0.334**.
- **Impact:** Strong ordinary random-fold performance does not validate transport to underrepresented areas or to previously unactivated stores. The result is exploratory because the predefined support requirements were unmet.
- **Required response:** Present the full 278-store list as a **model-implied planning scenario**, not a validated national rollout. Recommend a geographically stratified, bounded pilot with prospective outcomes and an explicit comparator. Do not treat the exploratory geographic metric as an unbiased estimate of national performance.

### P1 — Extreme tree probabilities drive the national forecast (forecast validity)

- **Observed:** Among the 170 previously unactivated stores selected by the refitted tree, **113 score 100%** (leaf: 41/41 historical successes) and **57 score 94.23%** (leaf: 49/52). The model implies **166.71 successes out of 170** new activations. Three historical held-out failures received a tree score of 100%.
- **Impact:** Small-leaf empirical frequencies, particularly 100%, cannot be treated as certain prospective outcomes. The €250,602.05 projected net depends heavily on these estimates.
- **Required response:** Report leaf sample sizes and uncertainty; label forecast values as conditional on model scores and case assumptions. Any calibration method must be evaluated without reusing held-out outcomes for fitting and scoring. Add a broad probability-stress scenario as a supplement to the prescribed local threshold test.

### P1 — Predictor provenance and historical selection remain unresolved (data validity)

- **Observed:** The five predictor fields have no documented measurement/reference dates; dentist distance has undocumented units. The 170 historical activations were selected, not randomly sampled from all 480 stores. The south accounts for about **30%** of labeled stores but **54%** of unactivated stores.
- **Impact:** Prospective feature availability, post-activation information leakage, and distribution shift cannot be ruled out by correct cross-validation alone.
- **Required response:** Team 2 should document field definitions, units, measurement dates and whether each field was available before the 2026 activation. Record the historical store-selection mechanism if known. If unresolved, retain the retrospective-only qualification.

## 3. Financial interpretation — verified arithmetic, conditional forecast

The released scoring policy funds stores when model-estimated `p(success) > 0.60`, under `expected case net = €2,500 × p − €1,500`.

| Scenario | Stores | Spend | Case net |
|---|---:|---:|---:|
| Observed 2026 activation outcomes | 170 | €255,000 | €15,000 |
| Repeat-170 model forecast | 170 | €255,000 | €15,989.87 |
| **Optimized model forecast** | **278** | **€417,000** | **€250,602.05** |
| Equal-spend optimized model forecast | 170 | €255,000 | €169,423.08 |

The **€235,602.05 Size of Prize versus 2026 observed** is a comparison of a forecast with historical realized case values, not a causal or independently validated profit improvement. The equal-spend comparison is ranked and valued using the **same** model probabilities and therefore does not independently prove targeting lift. Case net is not accounting profit.

## 4. Release checklist and ownership

- [ ] **Team 3 / Tommaso and Ale:** Correct the native exact-60% decision path; add the 6/10 test and rerun the release outputs.
- [ ] **Team 3:** Add blocking activation-join, fold-score and national-score uniqueness/completeness assertions.
- [ ] **Team 3:** Report tree leaf counts, near-threshold evidence, and limitations of the full-refit forecast; preserve the five-fold OOF comparison.
- [ ] **Team 2 / Ele and Denis:** Verify predictor definitions, dentist-distance units, reference dates and historical activation selection, or label these unknown.
- [ ] **Team 4:** Ensure the decision deck distinguishes the 278-store planning scenario from a defensible bounded pilot; show geographic-support failure and uncertainty of forecast probabilities.
- [ ] **Team 4:** Independently rerun the corrected release candidate (T13/T15), reconcile all outputs and record release sign-off/hashes before delivery.

**Closure standard:** The two implementation defects have fixes plus passing native KNIME regression tests; verified exports reconcile after rerun; all statistical limitations are stated without asserting unsupported prospective performance. If a substantive predictor-provenance issue cannot be resolved by the deadline, keep it explicitly open as a limitation rather than claiming verification.

## 5. Evidence and review boundaries

- [Evaluation protocol](../evaluation.md) · [Model choice](../model-choice.md) · [Release candidate](../release-candidate.md)
- [Held-out scores](../../outputs/held-out.csv) · [Held-out decisions](../../outputs/held-out-decisions.csv) · [Model comparison](../../outputs/model-comparison.csv)
- [National scores](../../outputs/national-scores.csv) · [Financial summary](../../outputs/financial-summary.csv) · [Geographic exploratory decisions](../../validation/T10/spatial-decisions.csv)
- [Release KNIME workflow](../../workflows/oral-b-italy.knwf) · [Store insights](../store-insights.md)

**Evidence basis:** Read-only local independent-review report dated 23 November 2026, referencing release commit `c23610a`, original Excel inputs, KNIME 5.12.0 workflow reruns, and the exported project artifacts. The findings above reflect that reviewed candidate; reassess implementation findings if the workflow has changed since. This report is a review, not evidence that any corrective changes have already been made.
