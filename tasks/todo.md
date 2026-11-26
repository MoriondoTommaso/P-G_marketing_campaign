# Oral-B Italy delivery ledger

Each issue has one owning two-person team; T01 records the names. Start as soon as all listed dependencies pass. Consecutive numbers denote ownership, not a requirement to finish the entire preceding block. See [team handoffs and checkpoints](plan.md).

## T01 — Record the team, environment and input fingerprints
- [ ] Runbook delivered; confirmations pending · Team 1 · XS · Depends: none
- **Output:** [Setup runbook](../docs/runbook.md) — Teams 2 and 3 can use the recorded input hashes and KNIME settings for the T05 join and T06 handoff.
- **Before closing:** Team 4 names the submission owner, backup, release reviewer and presentation lead; a second teammate records their KNIME version and required-feature check on #1.
- **Accept:** Name two members per team, eight distinct people total. From Team 4 identify the human submission owner and backup, release reviewer and presentation lead. Record KNIME version/extensions, configurable input path and the two workbook hashes. Record all 480 stores eligible, repeats allowed and no cap as the approved base case; escalate any new constraint.
- **Verify:** `shasum -a 256 data/Activated_Stores.xlsx data/Italian_Stores.xlsx`; compare both lines with the runbook. A second member checks the recorded KNIME version against their installation.

## T02 — Define the held-out funding test before fitting
- [ ] Protocol delivered; handoff receipt pending · Team 1 · S · Depends: none
- **Output:** [Evaluation protocol](../docs/evaluation.md) — ready for Teams 2–4. The fold assignments and 59/60/61% funding decisions have been checked.
- **Before closing:** Team 3 records receipt on #2. Model execution is verified under T08–T12.
- **Accept:** Specify seed, a fixed five-fold outcome-stratified assignment by store, a small national-feature shortlist, and fold-local preprocessing/selection; reserve any tuning for inner training folds. Define the baseline, logistic and shallow-tree comparisons using Brier score, calibration near 60%, fold variation and held-out net versus all/none. Define the spatial grouping and fallback for sparse groups before seeing model results.
- **Accept:** Before results, record the numerical near-threshold band, the scale-change trigger for a like-budget comparison, and how to compare equal numbers of stores if fewer than 170 qualify without adding loss-making stores to the recommendation. Share the rules with Teams 2–4.
- **Verify:** `git diff --exit-code -- data/`; walk a hypothetical held-out store through the design: it cannot affect training statistics or its own prediction. Hand-check 59%, 60%, 61% net −€25, €0, +€25 and only the last funded.

## T03 — Establish which shopper claims the case supports
- [ ] Evidence matrix delivered; citation review pending · Team 1 · S · Depends: none
- **Output:** [Shopper evidence and action matrix](../docs/shopper-evidence.md) — Team 4 can prototype the neutral shelf guide now.
- **Before closing:** A teammate checks the citations and claim wording against case pp. 41–46 and records the result on #3. Named personas and SKU-specific copy need separate source confirmation before use.
- **Accept:** Cite case pages for relevant toothpaste benefits and in-store tactics. Record whether class-provided personas were available; distinguish sourced descriptions from team hypotheses. Draft the evidence → need → message → placement → measure matrix, leaving unverified profiles open.
- **Verify:** `open 'docs/PG_Luiss_Business Case_13_11_26.pdf'` on macOS (otherwise open in a PDF reader); a teammate checks citations against pp. 41–46 and confirms no unsupported product claim is labeled as fact.

## T04 — Prepare the independent finance worksheet and decision outline
- [ ] Worksheet and storyboard delivered; second-reviewer check pending · Team 2 · S · Depends: none
- **Outputs:** `outputs/finance-qa.xlsx`, `presentation/storyboard.md`
- **Before closing:** a second reviewer runs the 108 → 107 test in Excel and records the result on #4.
- **Accept:** Create a worksheet independent of the KNIME calculations. On 108 successes out of 170, reproduce €270,000 sales, €255,000 spend and €15,000 net; include zero-selected and 59/60/61% boundary cases. Reserve space in the storyboard for the two distinct comparators, shopper action, uncertainty and the contributions appendix.
- **Verify:** `open outputs/finance-qa.xlsx`; a second reviewer changes success count from 108 to 107 with spend unchanged and observes net fall by €2,500; restore the example. Inspect boundary decisions and slide allocation.

## T05 — Recover the 2026 outcomes and audit the national join
- [ ] Delivered; in review (branch `ele/t05-join`, reviewer Tommaso) · Team 2 · M · Depends: T01
- **Before closing:** Tommaso approves the PR and records pass/fail on #5.
- **Outputs:** `workflows/oral-b-italy.knwf`, `outputs/join-audit.csv`, `outputs/store-universe.csv`
- **Accept:** Import both `default` sheets; keep national attributes. Match 152 by nonblank code (106/46 successes/failures, including 38 incomplete coordinate pairs); recover exactly 18 blank codes by unique exact coordinate pairs (2/16). Flag ambiguous/conflicting links for review; do not guess.
- **Accept:** Audit IDs, outcomes, duplicate keys, missing values, units and plausible ranges; resolve or document exceptions. Output 480 distinct national IDs, with 108 successes, 62 failures and 310 unknown outcomes. Keep join method for audit only.
- **Verify:** KNIME **Reset → Execute all**; inspect grouped counts by match method and outcome and require zero ambiguous/unresolved links on the supplied inputs. `wc -l outputs/join-audit.csv outputs/store-universe.csv` must show 171 and 481 lines respectively.

## T06 — Publish the historical benchmark and hand off KNIME
- [ ] Delivered; in review (branch `ele/t05-join`, reviewer Tommaso) · Team 2 · S · Depends: T05
- **Before closing:** Team 3 imports the `.knwf` snapshot, reruns it in a fresh workspace and records the handoff on #6.
- **Outputs:** `workflows/oral-b-italy.knwf`, `outputs/baseline-2026.csv`, `docs/runbook.md`
- **Accept:** From all linked outcomes compute counts, incremental sales, spend and net at €2,500/€1,500; publish the two euro inputs in one labeled workflow configuration. Annotate why the 18 recovered stores matter.
- **Verify:** The receiving Team 3 imports the `.knwf` snapshot, sets `data/`, resets and selects **Execute all**. `cat outputs/baseline-2026.csv` must show 170 activated, 108 successful, €270,000 sales, €255,000 spend, €15,000 net. Team 2 records the handoff; Team 3 now owns the editable workflow.

## T07 — Identify store traits and gaps in national coverage
- [ ] Profiles and insights delivered and merged (PR #21); Ele's review applied; peer trace on #7 pending · Team 2 · S · Depends: T05
- **Outputs:** `outputs/store-profiles.csv`, `docs/store-insights.md`
- **Before closing:** Ele traces one trait back to `outputs/store-universe.csv` and records the result on #7. Needs the T05 branch merged so `store-universe.csv` is in the repository.
- **Accept:** Compare successes with failures on interpretable national traits; report direction, denominators, sample sizes and a plausible explanation labeled as a hypothesis. Compare the 170 labeled and 310 unlabeled stores on geography and major features, flagging low-support profiles or documenting observed overlap. Work on an export, not the shared workflow.
- **Verify:** `open outputs/store-profiles.csv`; trace one featured trait back to `outputs/store-universe.csv` and reproduce both group denominators and the direction. Review the geography comparison for evidence of extrapolation.

## T08 — Produce leakage-free baseline probabilities
- [x] DONE · Team 3 · S · Depends: T02, T06 (verified) · Implementation: `612658a`
- **Execution gate:** The focused test first failed on missing `folds.csv`. Fresh KNIME Desktop runs A (11:09) and B (11:19, reversed input) produced byte-identical exports, 171 lines each. Both fold hashes matched `a5be2eeea3a41874ddb88db300c1f35fc9f7c052aab8f962a67f25b653ff9745`. Independent CSV checks verified all 170 probabilities per run: 34 held-out stores per fold, 136 training labels, 310 unlabeled excluded. Fold 1: (108 − 22) / (170 − 34) = 86/136.
- **Reproduce:** [Repo-local workspace and evidence](../validation/T08/README.md); `python3 scripts/t08_validation.py check` verifies the archived A/B runs.
- **Verified handoff:** Team 3 [received the protocol](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/2#issuecomment-7096835693) and [reproduced T06 in KNIME Desktop](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/6#issuecomment-7097223938) at `717adc3`: 170 linked, 310 unlabeled and €15,000 historical net; all three exports byte-identical.
- **Handoff:** Team 3 can configure the folds from the [evaluation protocol](../docs/evaluation.md) now. Run them on the verified T06 snapshot once both gates pass; compare the sorted fold mapping with the protocol reference, including after reordering the input rows.
- **Outputs:** `workflows/oral-b-italy.knwf`, `outputs/folds.csv`, `outputs/baseline-oof.csv`
- **Accept:** Assign each of 170 linked IDs to one of five fixed stratified test folds. For each store export its fold and the success rate of the other four folds. Do not include unlabeled stores in training.
- **Verify:** Execute the KNIME validation stage; record `shasum -a 256 outputs/folds.csv`, reset and re-execute, and compare the second hash with the first. `wc -l outputs/folds.csv outputs/baseline-oof.csv` must show 171 lines each. Recalculate one fold's constant prediction from the other folds' success and store counts.

## T09 — Generate comparable logistic and tree predictions
- [x] DONE · Team 3 · M · Depends: T08 (verified at `831ecc7`) · Implementation: `bf8d2da`
- **Red gate:** `python3 validation/T09/check.py` failed on missing `outputs/held-out.csv` before workflow changes.
- **Desktop verification:** The 12:02 rerun loaded the explicit training-median settings without error. Both learners and predictors completed five folds with no learner/convergence warnings. All 170 stores matched the T08 mapping and baseline, with three valid probabilities each; the two runs' exports were byte-identical. Fold 4 had 136 training and 34 disjoint test IDs; store `15596` had tree probability 8/10. [Reproduction and evidence](../validation/T09/README.md).
- **Outputs:** `workflows/oral-b-italy.knwf`, `outputs/held-out.csv`
- **Accept:** Apply logistic regression and a shallow decision tree to the same saved folds. Fit preprocessing and feature selection inside training folds, with any tuning nested. Exclude identifiers, join method and activation-file fields from predictors. Export actual outcome, fold, baseline and both candidate probabilities on one row per labeled store.
- **Verify:** In KNIME execute each model path; inspect learner inputs and one fold's disjoint train/test ID sets. `wc -l outputs/held-out.csv` must show 171; check 170 distinct IDs with three nonmissing probabilities in [0,1].

## T10 — Select a model on decision value and geographic robustness
- [x] DONE · Team 3 · M · Depends: T07 ([peer check](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/7#issuecomment-7096929089)), T09 (`51c0645`) · Implementation: `357a2f2`
- **Red gate:** `python3 validation/T10/check.py` failed on the missing decision export before implementation.
- **Verified figures:** KNIME Desktop at 12:14 CET: 7 fits per learner, 510 ordinary decisions, 510 separate exploratory band audit rows, 27 reconciled summaries. Pooled all/none €15,000/€0. [Choose the shallow tree for a pilot](../docs/model-choice.md) from ordinary folds (€88,000). Qualifying geographic validation is unavailable: the primary southern test set has 4 failures and the fallback northern holdout trains on only 5 failures. The exploratory €16,500 is not sign-off evidence.
- **Workflow revision verified:** Desktop runs A/B completed at 12:34/12:35 CET on the grouped workflow. Each learner and predictor ran seven times per run. Only the deliberately reversed universe export changed order; all other exports were byte-identical across runs. The native funding fixture excluded an exact 60% tie. [Checksums and boundary evidence](../validation/T10/grouped-evidence/).
- **Outputs:** `workflows/oral-b-italy.knwf`, `outputs/held-out-decisions.csv`, `outputs/model-comparison.csv`, `docs/model-choice.md`
- **Accept:** For baseline and both models report Brier score, calibration near 60% with sample counts, selected counts, and observed net versus activate-all/none overall and by fold. For the candidates, compare performance with nearby stores held out together, or document group sizes that preclude a meaningful comparison.
- **Accept:** Name one model and justify complexity, selection bias and limits of performance estimates; do not portray model selection as independent validation. State when weak evidence warrants a pilot.
- **Accept:** Export one decision per held-out store/model (170 × 3), including ID, fold, probability, actual outcome, strict funding flag and realized net: €0 unfunded, +€1,000 funded success, −€1,500 funded failure. Aggregate these rows to the published fold and pooled results.
- **Verify:** KNIME **Reset → Execute all**; `wc -l outputs/held-out-decisions.csv` must show 511. Group the independent recomputation by fold/model; match counts and euro totals against `outputs/model-comparison.csv`. For pooled activate-all/none require €15,000/€0.

## T11 — Export the funding list and test threshold sensitivity
- [x] DONE · Team 3 · M · Depends: T10 (`e1ad414`) · Implementation: `38f5ce2`
- **Red gate:** `python3 validation/T11/check.py` failed on the missing `national-scores.csv` before workflow changes.
- **Verified:** Desktop at 19:41 CET: 480 unique IDs (170 held out, 310 refit); 278 base selections, €417,000 spend, €250,602.05 forecast net. All 1,440 scenario rows reconciled; 274 always funded, four lower-case drops, no upper additions. The base and shifted 60% ties are unfunded. Nine upstream exports byte-identical. [Forecast by source and scenario, exact IDs, fixture and reproduction](../validation/T11/README.md).
- **Outputs:** `workflows/oral-b-italy.knwf`, `outputs/national-scores.csv`, `outputs/activation-list.csv`, `outputs/sensitivity.csv`
- **Accept:** Refit the chosen model on all 170 labeled stores to score the 310 unseen; use the chosen model's held-out probabilities for the 170 historical stores. Export 480 unique `store_id` values traceable to `Pdv Code`, each with `p_success`, `score_source`, `expected_net_eur`, and `recommend_activate`. Export only positive unrounded net decisions to the list; zero selections is valid.
- **Accept:** Use the T02 near-threshold band and shift affected probabilities ±5 percentage points (bound to [0,1]); report changes in IDs, count and net, distinguishing robust from marginal decisions. Label this a scenario, not an interval.
- **Verify:** Execute the KNIME funding-rule check: 59/60/61% yield −€25/€0/+€25 and only 61% funds. `wc -l outputs/national-scores.csv outputs/activation-list.csv` must give 481 and selected count + 1. Compare actual ID sets before and after filtering; check 170/310 score sources. Recompute lower/base/upper counts and net from the scenario rows; match each scenario's added/dropped IDs to the base list.

## T12 — Release the workflow candidate and both Size of Prize comparisons
- [ ] RC1 verified; in PR review, merge on hold · Team 3 · S · Depends: T11 (`96925fd`) · Artifacts: `8b5fd51`
- **Red gate:** `python3 validation/T12/check.py` failed on the missing `financial-summary.csv` before workflow changes.
- **Verified:** Desktop at 19:57 CET; all five financial rows reconciled, 12 upstream exports unchanged. Optimized forecast vs 2026 actual +€235,602.05; vs repeat forecast +€234,612.18; at 170 stores per policy and €255,000 spend each +€153,433.21. [Team 4 handoff, pinned revision and both SHA-256 hashes](../docs/release-candidate.md).
- **Outputs:** `workflows/oral-b-italy.knwf`, `outputs/financial-summary.csv`, `docs/release-candidate.md`
- **Accept:** Export optimized and repeat-170 forecast count, sales, spend and net, plus 2026 actual. Reuse the same probabilities for repeat IDs. Report optimized net minus €15,000 actual separately from optimized net minus repeat-list forecast. Apply the like-budget rule defined in T02; include its result or why it did not trigger.
- **Verify:** KNIME **Reset → Execute all**, export the `.knwf`, then `shasum -a 256 workflows/oral-b-italy.knwf outputs/financial-summary.csv`. Record both hashes, the release revision, and output locations in the handoff to Team 4. Revisions supersede, never silently replace, an earlier candidate.

## T13 — Independently reconcile the release candidate’s economics
- [ ] TODO · Team 4 · S · Depends: T04, T12
- **Outputs:** `outputs/finance-qa.xlsx`, finance sign-off on the T13 issue
- **Accept:** Independently recompute count, sales, spend, net and both Size of Prize differences from the candidate's store-level exports, including like-budget results where applicable. Sign off on the T12 hashes only on agreement; send mismatches to Team 3 for a new candidate and rerun the check.
- **Verify:** `shasum -a 256 workflows/oral-b-italy.knwf outputs/financial-summary.csv` against T12. `open outputs/finance-qa.xlsx`; refresh from national scores/list, compare exact selected IDs/count and totals with `outputs/financial-summary.csv` within €0.01 after final rounding.

## T14 — Turn selected store profiles into shopper actions
- [ ] Delivered; in PR review ([#39](https://github.com/MoriondoTommaso/P-G_marketing_campaign/pull/39), branch `task/T-014-shopper-actions`); peer trace pending · Team 4 · S · Depends: T03, T07, T11
- **Red gate:** `python3 validation/T14/check.py` failed on the missing `docs/shopper-actions.md` before the document was written; the first draft's "no funded 2026 failure" assumption was also falsified by the check (8 failures are funded at model probability > 0.60).
- **Verified coverage:** Of 278 funded stores (€417,000 spend, €250,602.05 forecast net per the frozen summary): 100 held-out 2026 successes, 8 held-out failures, 170 refit-unseen; North 55 / Centre 88 / South 135; dentist distance ≤ 25: 194, 25–100 gap range: 84, > 100: zero; schools = 0: 115. Actions are tied to the T07 tercile citations (dentist 51 / 57 = 89% → 8 / 57 = 14%; schools 33 / 72 = 46% → 48 / 53 = 91%). Every consumer need is labeled a hypothesis; class personas are recorded as not identified in the supplied files; whitening wording stays conditional on SKU/claim confirmation; water hardness, income and geography-alone are explicitly not action bases. Framed as a bounded pilot per the decision brief.
- **Handoff:** Prototype the [T03 shelf guide](../docs/shopper-evidence.md) with neutral descriptors now. Finalize store-specific actions after the T03 review, using T07 profile counts and T11 selected IDs. Use persona- or SKU-specific wording only when its source is confirmed.
- **Output:** `docs/shopper-actions.md`
- **Accept:** Tie each priority persona to a supported store profile, consumer need, specific toothpaste message, channel/placement and measure. Cite observed comparisons, not individual shopper preferences; label inferred needs as hypotheses. If no stores qualify, frame actions for a bounded test rather than a national campaign.
- **Verify:** `open docs/shopper-actions.md`; a peer traces each action to a profile count and source, checks actual selected-store coverage against `outputs/activation-list.csv`, and confirms class personas or explicit hypothesis labels.

## T15 — Reproduce the exported workflow in a clean workspace
- [ ] TODO · Team 4 · S · Depends: T13
- **Output:** `docs/rerun.md` (QA evidence; the `.knwf` is a read-only input)
- **Accept:** A non-author imports the finance-approved T12 workflow hash in a fresh workspace, points to read-only inputs, and writes to a separate `outputs/rerun/` location. Reproduce audit counts, 480 decisions, exact selected IDs and both financial comparisons. Document environment, annotations, differences and resolution. Team 4's release reviewer signs this exact version; only Team 3 can produce a new candidate.
- **Verify:** `shasum -a 256 data/Activated_Stores.xlsx data/Italian_Stores.xlsx` against T01. KNIME **Reset → Execute all**. Run `cmp outputs/national-scores.csv outputs/rerun/national-scores.csv`, `cmp outputs/activation-list.csv outputs/rerun/activation-list.csv` and `cmp outputs/financial-summary.csv outputs/rerun/financial-summary.csv`. Require stable results and audit counts before release.

## T16 — Export the manager decision deck
- [ ] TODO · Team 4 · S · Depends: T13, T14
- **Outputs:** editable deck and `presentation/campaign.pdf`
- **Accept:** Within 10 content slides including any approved extra, explain which stores, how many, spend, both value comparisons, evidence for store traits, shopper actions and uncertainty. Separate historical outcomes from forecasts; support a pilot if indicated. Attach one separate appendix slide identifying each participant's actual contribution.
- **Verify:** Export PDF from the slide editor; `open presentation/campaign.pdf`. Count slides, read without speaker notes, trace headline figures to the frozen finance summary and verify all eight contributions with their owners.

## T17 — Rehearse within ten minutes twice
- [ ] TODO · Team 4 · S · Depends: T15, T16
- **Outputs:** `presentation/rehearsals.md`, final deck/PDF if timing edits are needed
- **Accept:** Confirm the deck uses the exact T15 QA-passed figures. Record two complete rehearsals of the release presentation, each ≤10:00, with timings and speakers. If content or figures change, repeat until the final version passes twice. Prepare answers on the store join, funding rule, selection bias and workflow.
- **Verify:** `open presentation/campaign.pdf`; time both full runs with the exported PDF. Compare the recorded version and durations to `presentation/rehearsals.md` and recheck the content-slide limit.

## T18 — Submit and verify the course package
- [ ] TODO · Team 4 · XS · Depends: T17
- **Output:** MyLuiss submission confirmation; receipt retained privately by the team
- **Accept:** Upload the final presentation PDF and KNIME workflow, plus only separately approved required attachments. On 27 Nov (Europe/Rome), aim for verified submission by 16:00; the absolute internal deadline is 18:00 and MyLuiss closes at 23:59. Verify the uploaded copies open; record filenames, timestamp and confirmation. Schedule Q&A rehearsal before the following week's talk.
- **Verify:** Before upload run `shasum -a 256 presentation/campaign.pdf workflows/oral-b-italy.knwf`. Download the submitted copies, compare hashes, reopen the PDF and import the workflow. Confirm the portal shows the submission and timestamp; keep credentials and receipt off the public issue.

## T19 — Present the decision to P&G managers
- [ ] TODO · Team 4 · S · Depends: T18
- **Output:** live delivery confirmation and Q&A rehearsal record on the T19 issue
- **Accept:** Confirm the course slot for the following week, rehearse Q&A on the join, model, profit assumptions and shopper actions, and deliver the management presentation within 10 minutes. Record the slot, actual duration and completion; do not close this task at upload.
- **Verify:** `shasum -a 256 presentation/campaign.pdf` matches the submitted PDF. A teammate records who attended the Q&A rehearsal and confirms the live delivery time after the session.

## #31 — Respond to independent model review
- [x] Record the selection and transfer limitations, extreme leaf counts, uncertainty, broad probability stress and bounded pilot comparator in the [decision brief](../docs/model-review/pilot.md); revise slides 1, 5 and 8 of the storyboard.
- [x] Label missing predictor reference dates, dentist-distance units and historical selection criteria unknown. Team 2 owns follow-up with the data provider.
- [x] RC2: supplied-probability boundary fixture, 13 reconciled exports and [eight corruption checks](../validation/issue31/guards/native-results.txt). RC2 did not validate final finance, activation or sensitivity rows.
- [x] RC3 (`e1185d7`): final writer-input tables feed the shared release gate; all 13 clean CSVs reconciled.
- [ ] Team 4: independently rerun the pinned corrected archive in a fresh workspace, record hashes and sign-off on T13/T15 and integrate the qualified decision into T16.

## T-052 — Verify the Decision B KNIME release
- [ ] **IN PROGRESS** · [RF-WF #52](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/52) · Team 3; Team 2 verifies linkage. Owner approved the [reviewed task](https://github.com/MoriondoTommaso/P-G_marketing_campaign/blob/39c7a809694af09ca6e89aaeda274360d5b3b9d0/tasks/todo.md#rf-wf--build-and-verify-the-knime-release-candidate) with [Decision B](../docs/final-model-decision.md).
- **Native shared-fold slice:** on `d067910` the tree held out 138 of 170 IDs in the wrong protocol fold. The candidate computes class-wise hash ranks, orders by fold and text ID, then uses linear 34-row test blocks. The native test checks the *actual* test IDs for tree, forest and logistic against `outputs/folds.csv`. This is pre-finance verification, not release sign-off.
