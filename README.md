# P&G Oral-B Italy 2027 Marketing Campaign

**LUISS Guido Carli · Business and Marketing Analytics**

This repository documents a group analytics project and the technical work directed by **Lorenzo Pazienza (Lollo)**, a member of **Team 1 — Research & Methodology** with Petra. His documented scope covers the three mandatory Team 1 deliverables, T01–T03.

## Project overview

P&G wants to decide which Italian stores to activate for its 2027 Oral-B toothpaste campaign, how much to invest, what value to expect relative to 2026, and how to communicate with shoppers in the selected stores. The project uses a 480-store national workbook and binary outcomes from the 170 stores activated in 2026. Under the approved planning assumptions, all 480 stores are eligible, repeat activation is allowed, and there is no binding budget cap.

The planned KNIME workflow links the two workbooks, compares predictive models on held-out 2026 activations, and converts success probabilities into store-level funding decisions. It will estimate the Size of Prize against both the 2026 historical benchmark and a forecast that repeats the original activation list. The shopper strategy connects store evidence to proposed in-store messages and tests. [Course assignment](docs/Business%20and%20Marketing%20Analytics%20-%20Group%20Assignment.pdf) · [Project specification](docs/SPEC.md)

## Project team

| Team | Members | Mandatory scope | Selected extra |
|---|---|---|---|
| 1 · Research & Methodology | Petra and **Lorenzo Pazienza (Lollo)** | T01–T03 · Setup, statistical evaluation protocol and shopper evidence | Extra 3 · Influencer Shortlist |
| 2 · Data Preparation & Analytics | Ele and Denis | T04–T07 · Financial QA worksheet, KNIME data preparation, baseline and store profiles | Extra 2 · Additional Data |
| 3 · Predictive Modeling & AI | Tommy and Ale | T08–T12 · Model implementation and validation, targeting, and financial forecasts | Extra 5 · GenAI Consumer Experience |
| 4 · Marketing Strategy, QA & Delivery | Bianca and Linda | T13–T19 · Independent QA, shopper actions, presentation and submission | None. Integrates the selected extras into the presentation. |

Lorenzo's contribution record covers T01–T03. The power-toothbrush influencer shortlist is handled separately. [Team assignments](docs/TEAM_ASSIGNMENTS_AND_CONTRIBUTIONS.md) · [Task ledger and acceptance criteria](tasks/todo.md)

## Lorenzo Pazienza — Detailed technical contributions

Lorenzo specified the three deliverables, directed an AI-assisted development and verification process, set the criteria for a separate technical and source-level audit, and directed the corrections and final handoff. The inspection, calculations, document drafting and programmatic tests described below were performed through that AI-assisted process. Petra and Lorenzo share Team 1 ownership of the deliverables.

### T01 — Environment, reproducibility and data verification

- **Environment.** Documented the locally inspected installation of KNIME Analytics Platform **5.12.0** on arm64 macOS with bundled Temurin Java **21.0.9**. Recorded installed extension builds for Excel import, file handling, transformations, Java Snippet and the decision-tree nodes. The runbook specifies one configurable input directory and a separate output path for clean reruns.
- **Input integrity.** Read both workbooks programmatically and fingerprinted their original files with SHA-256. The national `default` sheet has **480 rows and 36 columns**. The activation `default` sheet has **170 rows and four columns**, excluding headers in both cases. The verification checked field types, blanks, unique national IDs and coordinate pairs, duplicate rows and activation labels.
- **Linkage.** Reconciled **152** populated `Pdv Code` values and recovered **18** blank-code records using unique, exact latitude–longitude pairs. Checks using the raw Excel decimals and doubles gave the same recoveries. All 170 activation records mapped to distinct stores, with zero ambiguous or unmatched links and zero available-coordinate conflicts. The 310 remaining outcomes are unknown.
- **Handoff.** Reconstructed 2026 campaign economics from the 108 successes and 62 failures under the assignment's stipulated amounts. Documented reader settings, row-count and match checks, and the expected exports for Team 2's T05–T06 workflow. Team 3 will import the T06 snapshot into a fresh workspace and confirm the input checks before modeling. [T01 setup runbook, hashes and reconciliation](docs/runbook.md)

### T02 — Statistical evaluation and decision methodology

- **Fixed evaluation design.** The protocol uses five outcome-stratified folds keyed by unique store. A fixed seed and a SHA-256 sort key give the same assignments regardless of row order. Independent Python and Node.js reproductions agreed on every store assignment. Each fold has **34 test stores** and **136 training stores**. All candidate paths use the same folds, with one out-of-fold probability per store and model.
- **Leakage controls and predictors.** The five national inputs cover population, household income and size, and two dental-access measures. Imputation, scaling and the usable-feature mask are fitted inside each training partition. Store identifiers, coordinates, matching metadata and activation-only fields stay out of the learners. The audit identified missing predictor measurement dates. The protocol now requires a timing and source check, excludes confirmed post-activation or outcome-derived inputs, and qualifies retrospective results when timing is unresolved.
- **Model comparison and calibration.** The training-fold success-rate baseline provides a reference for regularized logistic regression and a single shallow decision tree. Its analytically reproduced probabilities all exceed 60%, so it reproduces the activate-all reference. Fixed learner settings constrain complexity with 170 labels. Brier score evaluates probability accuracy, while the prespecified **55–65%** band and its split at 60% show calibration where forecasts can change funding decisions. The comparison reports sample counts and variation across folds. Model choice uses pooled realized net, with fixed Brier and simplicity rules for close results. Follow-up tuning is nested. Any future calibration map must use training-derived cross-fitted scores and a separate assessment split.
- **Funding and sensitivity.** Expected store net is `€2,500 × p − €1,500`. A store qualifies only when its unrounded probability is **strictly above 60%**. Held-out net uses observed outcomes and compares the decision against activating all or none on the same stores. The protocol stresses near-threshold probabilities by ±5 percentage points and recomputes selected IDs, count, spend and expected net. Equal-store-count comparisons use the same per-store cost when spend differs by at least **17 activations** or when fewer than 170 qualify. The funding list keeps only qualifying stores.
- **Geographic robustness and external validity.** The planned latitude-band holdout falls back to two bands because the primary southern band has only four observed failures. The fallback has **46 successes and five failures in the south** versus **62 successes and 57 failures in the north**. The south contains **167 of the 310** unlabeled stores. The audit documented this imbalance and explained why internal validation on selected 2026 stores leaves 2027 transfer uncertain. Winner selection can make its reported performance optimistic. Equal-spend gains are projections based on the same ranking scores used to choose stores.
- **KNIME implementation.** The handoff specifies the seeded fold key, a single fold mapping, train/test loop, fold-local preparation, probability joins and export checks. The release design uses out-of-fold probabilities for the 170 historical stores and a fit on all 170 labels to score the 310 unseen stores, with score sources labeled. Candidate fitting, performance measurement and release workflow execution belong to Team 3. [T02 evaluation protocol and implementation checks](docs/evaluation.md)

### T03 — Consumer research and marketing evidence

- **Source review.** Inspected the assignment and visually checked the P&G case's oral-care section on PDF pages **41–46**. Page 42 provides historical brand positioning in the Italian oral-care market. Pages 43–44 show whitening positioning on one pictured toothpaste pack. The Oral-B iO callout concerns wider innovation context and provides no toothpaste campaign effect estimate. Page 46 supports easy navigation, shopper education, premium visibility and convenience as in-store tactics.
- **Evidence to action.** Developed a matrix that links each cited observation to a hypothesized shopper need, proposed message, placement and KPI. The recommended starting prototype is a shelf-edge guide with neutral descriptors. The proposed KPI is correct variant-finding within a fixed time, divided by all attempts. Alternatives cover a comparison card with premium unit mix and total units, and a restock prompt with units per store-week.
- **Claim and measurement review.** Corrected the page reference for the historical share chart and distinguished the iO sales callout from the toothpaste evidence. Refined the KPIs to include unsuccessful navigation attempts and to require pre-exposure purchase intent plus actual purchase before drawing conclusions about unplanned buying. The local course materials establish neither named class personas nor the approved 2027 Italian lineup and SKU wording. Proposed shopper situations remain testable hypotheses. [T03 shopper evidence and action matrix](docs/shopper-evidence.md) · [P&G case, oral-care section](docs/PG_Luiss_Business%20Case_13_11_26.pdf#page=41)

## Independently reproduced quantitative findings

The AI-assisted verification independently reconstructed these figures from the source files. Economic amounts apply the course assumptions to the binary activation outcomes. They represent the case's financial measure of campaign value. The source workbooks supply no accounting profit, contribution margins or store-level euro results.

| Measure | Verified result | Basis |
|---|---:|---|
| National store universe | **480** | Distinct national store IDs |
| Stores activated in 2026 | **170** | 152 ID matches + 18 exact coordinate matches |
| Stores without observed activation outcomes | **310** | 480 − 170 |
| Coordinate-based recoveries | **18** | Two successes and 16 failures among blank-code records |
| Successful activations | **108** | 106 ID matches + 2 coordinate matches |
| Unsuccessful activations | **62** | 46 ID matches + 16 coordinate matches |
| Historical success rate | **63.53%** | 108 ÷ 170 |
| Case-imputed incremental sales | **€270,000** | 108 × €2,500 + 62 × €0 |
| Activation spend | **€255,000** | 170 × €1,500 |
| Project-defined historical net value | **€15,000** | €270,000 − €255,000 |
| Economic break-even probability | **60%** | €1,500 ÷ €2,500. At 59%, 60% and 61%, expected net is −€25, €0 and +€25 respectively. Only 61% qualifies. |

[Historical reconciliation](docs/runbook.md#exact-reconciliation) · [Funding rule and boundary checks](docs/evaluation.md#decision-data-and-scope)

## Technical audit and quality assurance

| Verification performed | Correction or assurance |
|---|---|
| **Original-file checks.** Inspected Excel XML, recomputed SHA-256, checked coordinate multiplicity and conflicts, and linked IDs without rounding coordinates. | Made the exact join reproducible and preserved 16 observed failures among the 18 recovered rows. |
| **Independent numerical reproduction.** Reconstructed the folds in two implementations and checked class counts, geographic support and the historical net. | Added a reference digest for Team 3 and made the geographic imbalance explicit. |
| **Synthetic methodological checks.** Exercised train-only preprocessing, decision boundaries, decimal sensitivity shifts, model-selection tolerances and equal-spend cases. | Clarified safeguards for predictor timing and calibration, and distinguished projected matched-spend gains from evidence of realized targeting lift. Synthetic tests covered the protocol logic. |
| **Source and document checks.** Compared PDF text, visuals and page links, and checked the consistency of the documentation and handoffs. | Narrowed product attribution, separated evidence from hypotheses, and specified denominators for shopper measures. |
| **KNIME install inspection.** Checked installed features and node definitions for the proposed implementation. | Established a local implementation reference. The candidate fits and clean rerun of a project KNIME workflow remain downstream work. |

## Files and deliverables

| File | Purpose | Work completed | Status |
|---|---|---|---|
| [`docs/runbook.md`](docs/runbook.md) | T01 · Environment and reproducibility | Installation record, hashes, data checks, exact join, financial baseline and rerun instructions | Team 1 work complete. Ready for Team 2. Formal closure pending role and second-machine checks. |
| [`docs/evaluation.md`](docs/evaluation.md) | T02 · Statistical and economic protocol | Fixed folds, preprocessing, comparison, funding rules, robustness and implementation checks | Team 1 work complete. Ready for Team 3 to implement. Execution follows the T06 handoff. |
| [`docs/shopper-evidence.md`](docs/shopper-evidence.md) | T03 · Evidence for shopper actions | Source review, limitations, action matrix and measurement proposals | Team 1 work complete. Ready for Team 4 to use. Formal closure pending teammate citation review. |

Responsibilities, acceptance criteria and handoffs are recorded in the [team assignments and contribution logs](docs/TEAM_ASSIGNMENTS_AND_CONTRIBUTIONS.md), [task ledger](tasks/todo.md), [delivery plan](tasks/plan.md) and [roadmap](ROADMAP.md).

## Reproducibility

1. **Verify the inputs.** Compare the local workbook hashes with the runbook using `shasum -a 256 data/Activated_Stores.xlsx data/Italian_Stores.xlsx` from the repository root. The runbook also provides a PowerShell command.
2. **Reproduce the data preparation.** Use KNIME 5.12.0 and check the feature list for Excel reading, path variables, preparation, Java Snippet and modeling. Point both readers at the local `data/` directory through the shared input setting. Team 2 reproduces the linkage and history checks and supplies the editable workflow and a T06 export.
3. **Implement and validate the models.** Team 3 imports the T06 snapshot, reproduces the baseline, checks the sorted fold mapping against the reference, and implements T08–T12. Team 4 uses the finance-approved export for an independent clean-workspace rerun. [Environment and rerun instructions](docs/runbook.md#configure-and-reproduce-the-workflow) · [Evaluation handoff checklist](docs/evaluation.md#verification-and-handoff)

## Limitations and pending confirmations

- **T01 closure.** A second teammate must confirm the KNIME version and required features on their machine. Team 4 must name the submission owner, backup, release reviewer and presentation lead.
- **T03 closure and campaign copy.** A teammate must complete the independent citation review. Persona-specific messaging and SKU benefit statements require the class materials or confirmed product information and approved Italian wording.
- **Modeling and release.** Team 2 owns the KNIME preparation and snapshot. Team 3 owns model fitting, validation and forecasts. Team 4 owns independent release QA, final shopper actions, the deck and delivery. Predictor measurement dates and performance in previously unactivated stores remain evidence limitations.

## Individual Contribution — Lorenzo Pazienza

**Lorenzo Pazienza** directed development, technical verification and handoff of the three mandatory Team 1 deliverables. He set the scope and acceptance criteria for environment and data verification, statistical decision methodology, and consumer evidence. He commissioned the AI-assisted audit and directed follow-up corrections to the reproducibility instructions, leakage and calibration safeguards, and marketing evidence and measures. The resulting documents are joint Team 1 deliverables with Petra. The programmatic calculations and document checks came from the AI-assisted work under Lorenzo's direction. The individual contribution log remains the place for students to record their personally verified activities. Git history records changes to files and does not establish who performed each analytical activity. [Team ownership and contribution logs](docs/TEAM_ASSIGNMENTS_AND_CONTRIBUTIONS.md#individual-contribution-logs)

## Repository structure and project documentation

```text
.
├── README.md
├── ROADMAP.md
├── data/
│   ├── Activated_Stores.xlsx
│   └── Italian_Stores.xlsx
├── docs/
│   ├── Business and Marketing Analytics - Group Assignment.pdf
│   ├── PG_Luiss_Business Case_13_11_26.pdf
│   ├── SPEC.md
│   ├── TEAM_ASSIGNMENTS_AND_CONTRIBUTIONS.md
│   ├── evaluation.md
│   ├── runbook.md
│   └── shopper-evidence.md
└── tasks/
    ├── plan.md
    └── todo.md
```

## Submission and project status

The official deadline is **Friday, 27 November 2026 at 23:59 on MyLuiss** for the presentation PDF and KNIME workflow. The presentation allows up to ten content slides including any extras, plus a separate individual-contributions appendix. The team presents the following week in a ten-minute slot. [Course assignment, p. 4](docs/Business%20and%20Marketing%20Analytics%20-%20Group%20Assignment.pdf#page=4)

| Internal milestone · Europe/Rome | Target |
|---|---|
| Team 1 methodology handoff, then Team 2 cleaned-data handoff | 21 Nov · 12:00 and 18:00 |
| Initial analytical and modeling results | 23 Nov · 21:00 |
| Team 3 final targeting, finance and workflow handoff to Team 4 | 24 Nov · 21:00 |
| Selected extras due, then first integrated presentation | 25 Nov · 18:00 and 20:00 |
| Final QA, reproducibility checks and rehearsals | 26 Nov · 20:00 |
| Verified submission target | 27 Nov · 16:00 |
| Absolute internal submission deadline | 27 Nov · 18:00 |

This checkout records completion of the Team 1 documentation and readiness for handoff. The fitted models, release workflow, presentation and submission are downstream milestones. [Internal schedule and dependencies](docs/TEAM_ASSIGNMENTS_AND_CONTRIBUTIONS.md#internal-deadlines-and-handoffs)
