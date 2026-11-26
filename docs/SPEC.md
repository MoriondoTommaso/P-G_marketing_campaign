# Oral-B Italy: 2027 toothpaste campaign decision

**Status: draft for explicit approval.** Audience: P&G marketing managers. Planning outputs: this specification and [the roadmap](../ROADMAP.md). This planning pass produces documentation only.

**Funding-policy amendment, 26 Nov 2026:** [Decision B](final-model-decision.md) is confirmed for the 2027 planning list. The historical model comparison still uses held-out predictions and the break-even threshold; the 2027 list uses the two cohort rules below.

## Objective and required deliverables

Recommend which Italian stores should receive the 2027 campaign, how many to fund, what the investment is expected to return versus 2026, and how to speak to shoppers in those stores. The decision is about incremental sales after campaign costs; classification accuracy alone cannot answer it.

| Deliverable | What a manager or reviewer must be able to do |
|---|---|
| Store selection and economics | Find every recommended store by `Pdv Code`, see why it cleared the funding rule, and trace the count, spend and expected gain back to that list. |
| Store insights and shopper communication | Understand which store traits distinguish successes from failures; see a concrete message, channel or in-store activity for the priority audience, with an explanation of why it fits. |
| Reproducible evidence | Open one annotated KNIME workflow, compare at least two predictive models against a simple baseline, and reproduce the recommendation from the supplied workbooks. |
| Management presentation | Deliver the decision in 10 minutes, with at most 10 content slides including any extras, plus a separate contributions appendix. Submit the PDF and KNIME workflow to MyLuiss by **Friday, 27 November 2026, 23:59**. Present the following week. |

**Team scope:** eight participants work in four pairs. Extras 2, 3 and 5 have planned owners and remain optional under the course requirements. See the [team assignments](TEAM_ASSIGNMENTS_AND_CONTRIBUTIONS.md) for the owners and internal milestones.

## Evidence and inputs

- [Group assignment](Business%20and%20Marketing%20Analytics%20-%20Group%20Assignment.pdf), pp. 1–6: decision, financial assumptions, submission rules and scoring.
- [P&G business case](PG_Luiss_Business%20Case_13_11_26.pdf), pp. 41–46: Oral-B positioning, shopper education, shelf navigation and assortment. Its historical category figures are context, not a forecast for this toothpaste campaign.
- `data/Italian_Stores.xlsx`: sheet `default`, 480 distinct store codes, 36 columns. Features include coordinates, local population by age, household income, schools, hygienists and distance from a dentist.
- `data/Activated_Stores.xlsx`: sheet `default`, 170 activation records, with store code, coordinates and outcome. A read-only inspection established the following reference counts; KNIME must reproduce them:

| Link to national store | Records | Incremental sales | No incremental sales |
|---|---:|---:|---:|
| Nonblank code matches | 152 | 106 | 46 |
| Blank code; unique exact latitude **and** longitude match | 18 | 2 | 16 |
| Total distinct linked stores | **170** | **108** | **62** |

Use the code first. Of the 152 code matches, 38 lack one or both activation coordinates; the code is sufficient. For blank codes only, use the unique exact coordinate pair and record the match method. Keep national-file attributes for modeling. Any ambiguous link, conflict or unexpected count goes to review before training. The other **310 stores are unlabeled**, not failures.

## Decision rules and assumptions for approval

**Given by P&G:** €2,500 incremental sales per successful activation, €0 per unsuccessful activation, €1,500 cost per activated store. Under this simplified case, “net campaign value” means incremental sales less activation spend; it is not accounting profit after product costs.

| Decision | Proposed rule |
|---|---|
| Historical benchmark | 2026 realized incremental sales = 108 × €2,500 = **€270,000**; spend = 170 × €1,500 = **€255,000**; net campaign value = **€15,000**. Use all 170 linked outcomes. |
| Eligibility and budget | Score all 480 national stores; the base case has no binding budget or retailer quota. For the equal-spend comparison, rank stores within the Decision B list by forecast probability. |
| Funding rule | Repeat a historical activation **if and only if it succeeded in 2026**. For a previously unactivated store, require **61–100 forest success votes**; 60 votes is unfunded. For both cohorts, expected value = €2,500 × forest probability − €1,500. |
| Size of Prize | Show expected 2027 sales, spend and net value separately. Report expected optimized net value minus the **€15,000 realized in 2026**, explicitly labeled forecast versus history. Also estimate the value of repeating the 170-store list under the same forecasting assumptions; compare it with the optimized list to isolate the change in targeting and scale. Show a same-spend comparison if scale accounts for much of the difference. |
| Interpretation | Assume the 2026 relationships and case economics are informative for 2027. Only selected stores were activated in 2026. Predicted success is conditional on activation; these data do not independently identify causal effects, individual preferences or a percentage-point gain in brand share. |

## Model, validation and testing strategy

1. **Validate the inputs.** Reconcile the join to the counts above. Check target values, duplicates, missingness, numeric units and plausible ranges. Compare the 170 labeled stores with the 310 unlabeled ones on geography and major traits; flag poorly represented profiles before recommending a national rollout.
2. **Compare models fairly.** Proposed: a training-fold success-rate baseline, logistic regression and a shallow decision tree. Use the same fixed, outcome-stratified five folds for all three. Keep a store wholly within one fold. Fit preprocessing and feature selection inside training folds; exclude store ID, join method and activation-file fields from predictors. Prefer a small set of interpretable features over dozens of overlapping demographic counts.
3. **Test the funding decision.** For each held-out store, record its probability and the net value that would have resulted from applying the 60% rule. Report selected count and realized net value against activating all or none on the same held-out stores. Check probability calibration near 60%, Brier score (mean squared probability error), and variation across folds. If model choices are tuned, tune inside training folds. Treat comparisons used to choose the winner as estimates, not independent proof.
4. **Check generalization.** Compare results when nearby stores are held out together, where sample sizes allow. Report how the list changes when predicted probabilities near break-even move up or down by five percentage points. This is a sensitivity scenario, not a confidence interval. Prefer a simpler model if added complexity provides no credible decision benefit.
5. **Produce the list.** Refit the chosen model on the labeled sample for scoring previously unseen stores. For the 170 previously activated stores, use held-out probabilities for the planning estimate so a store's own outcome does not determine its forecast. Use the same store-level estimates for the repeat-list comparator. Document these score sources. Export one score per national code and a filtered activation list. If validation does not support expansion, state that and recommend a bounded pilot rather than promising a gain.
6. **Verify independently.** A second pair reconstructs the expected ID set from the historical labels and new-store votes, then recomputes spend, sales, net value and Size of Prize. At 59, 60 and 61 votes, per-store expected net is −€25, €0 and +€25; only the 61-vote **new** store qualifies. For repeats, test a below-threshold prior success and an above-threshold prior failure. Reopen the exported workflow in a fresh workspace and reproduce the counts, IDs and totals.

## Marketing evidence standard

For each featured store trait, report its direction, supporting comparison and sample size. Offer a plausible business explanation labeled as a hypothesis. For each priority shopper persona, link **store evidence → consumer need → message → placement → measure**. For example, a shelf guide organized by benefit is consistent with the case's emphasis on easier assortment navigation; the store data must justify where to test it. Local demographics describe catchments, not individual buyers. Confirm any personas presented in class; if those materials are unavailable, label proposed personas as team hypotheses.

## Tech stack, commands and structure

Use KNIME Analytics Platform with Excel readers, native preparation/modeling nodes and tabular exports. Use the team's slide editor for PDF export. Pair 1 records the actual KNIME version and required extensions before workflow handoff. The core requires neither Power BI nor a separate scripting environment.

| Operation | Command or operator action |
|---|---|
| Verify inputs from project root (macOS/Linux) | `shasum -a 256 data/Activated_Stores.xlsx data/Italian_Stores.xlsx` — record the two hashes with the workflow run details. |
| Reproduce analysis | In KNIME, import the delivered `.knwf` into a fresh workspace, point its input directory at `data/`, reset the workflow and choose **Execute all**. Compare the audit outputs with the reference counts above. |
| Package submission | Export the KNIME workflow as `.knwf`; export the management deck as PDF. Reopen both exported files before upload. |

| Location | Purpose |
|---|---|
| `data/` | Existing, read-only source workbooks |
| `docs/`, `ROADMAP.md` | Existing briefs, this spec and the delivery plan |
| `workflows/` | Proposed future location of the annotated KNIME workflow; checks live beside the workflow stages they validate |
| `outputs/` | Proposed future home of join audit, held-out predictions, model comparison, national scores, activation list and financial summary |
| `presentation/` | Proposed future home of editable slides, PDF and contributions appendix |

**Workflow and code style:** name KNIME sections by business action, e.g. `02 — Reconcile 2026 activations`. Annotate *why* each join, exclusion and threshold exists. Preserve source headers at import; use descriptive export names such as `store_id`, `p_success`, `score_source`, `expected_net_eur` and `recommend_activate`. Keep the two financial assumptions in one labeled configuration; round only for presentation.

## Boundaries and acceptance

- **Always:** preserve the raw workbooks; distinguish observed 2026 outcomes from forecasts; trace every headline number to an output; document material limitations and each participant's actual contribution.
- **Ask first:** changing the eligibility or budget assumption, using approximate matches, substituting tools for KNIME, changing the financial benchmark, or starting an extra outside the current plan.
- **Never:** treat unlabeled stores as failures, use a store's outcome to predict itself, edit the target list manually to improve the story, or present an optional activity as necessary for submission.

**Core is complete when** the KNIME export reruns; all 170 labels and 480 national decisions reconcile; the model comparison and held-out funding test are visible; the activation list, count and financial comparisons agree; and the deck explains store traits, shopper actions and uncertainty in terms a manager can use. The PDF must meet the slide limit, include the contributions appendix, and be rehearsed at least twice within the 10-minute slot. No minimum profit improvement or extra is required to pass these checks.

## Open questions

| Question | Owner and latest point to resolve |
|---|---|
| Are there budget limits, retailer constraints or restrictions on reactivating stores beyond the brief? | Pair 1, before finalizing the funding rule; otherwise seek approval for the stated base case. |
| Are the named consumer personas or lineup details from the class presentation available separately? | Team 1 researches this in #3; Team 4 uses the evidence for messages and product claims in #14. |
| Who owns submission, and which KNIME version will the team use? | Team, at kickoff. Confirm the T01 release and presentation roles. |

**Approval gate:** the full spec and phase roadmap are drafts until the team explicitly approves them. After approval, run `/breakdown`.
