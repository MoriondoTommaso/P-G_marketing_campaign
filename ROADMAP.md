# Roadmap: Oral-B Italy 2027 campaign

**Draft for approval.** [Full specification and acceptance criteria](docs/SPEC.md). The external deadline is **27 November 2026, 23:59 on MyLuiss**; dates below are proposed internal checkpoints, not course deadlines. The team presents the following week.

## Four parallel pairs

| Pair | Owns | First independent work | Handoff |
|---|---|---|---|
| 1 · Store data and baseline | One row per national store; 2026 reconciliation | Verify workbook inputs, resolve store IDs, calculate campaign economics | Labeled table, national scoring table and join audit to Pair 2; €15,000 benchmark to Pair 4 |
| 2 · Prediction and targeting | Model comparison, probability estimates, selection rule | Design evaluation and test the economics on hand-calculated examples while Pair 1 checks the data | Held-out results, selected IDs and reconciled value estimates to Pairs 3 and 4 |
| 3 · Store insights and communication | Store profiles, priority shoppers, messages and placement | Check course persona references and case-supported product benefits; draft a matrix connecting evidence to messaging | Validate profiles with Pair 2, then supply evidence-backed actions and measures to Pair 4 |
| 4 · Management decision and QA | Deck, independent arithmetic, rehearsal and submission | Outline the decision slide and prepare an independent calculation of the 2026 result | Reconcile exports, verify workflow import and assemble the upload package |

Assign names at kickoff. Pair 1 owns the shared KNIME workflow through the data handoff; Pair 2 integrates the modeling stages after that. Pair 4 verifies the exported copy. This avoids simultaneous edits to the same workflow.

## Core phases and dependencies

| Phase / proposed date | Work and dependencies | Exit checkpoint |
|---|---|---|
| 0 · Scope and setup · Nov 19 | Team reviews spec, confirms owners, assumptions and available tools. | Explicit approval; named participants and submission owner; common KNIME version recorded. |
| 1 · Reconcile inputs · Nov 19–20 | After approval: Pair 1 checks stores and derives baseline. Pairs 2–4 start their independent work above. | 152 code matches + 18 unique coordinate matches = 170 distinct labeled stores; 310 unlabeled; historical net €15,000. Resolve any discrepancy before fitting. |
| 2 · Test targeting and investigate traits · Nov 21–23 | Pairs 2 and 3 use the checked tables in parallel. Pair 4 challenges the comparator and drafts the decision story. | Comparable held-out results for baseline and two models; documented choice, calibration and selection-bias checks; store insights with sample sizes. |
| 3 · Make the recommendation · Nov 24–25 | Pair 2 scores stores and exports the proposed list. Pair 3 matches messages to selected profiles. Pair 4 independently recomputes both financial comparisons. | Freeze the list, store count, spend and Size of Prize. Pair 4 can trace every number to store rows; Pair 3 can explain each action. If evidence is weak, agree on a pilot recommendation. |
| 4 · Package and rehearse · Nov 26 | Depends on the frozen recommendation. Pair 4 integrates; other pairs verify their claims, rerun the exported workflow and rehearse. | Submission-ready PDF and `.knwf`, contributions appendix, clean-workspace rerun and two timed rehearsals meeting the 10-minute limit. |
| 5 · Submit · Nov 27 | Submission owner verifies final exports and uploads to MyLuiss. Proposed internal target: **18:00**, leaving time to correct upload issues. | Confirm uploaded files open and retain the submission receipt. Before the live session the following week, rehearse Q&A on store selection, limitations and workflow. |

**Critical dependency:** verified store linkage → held-out model comparison → frozen store list and economics → final deck and workflow. Persona research, slide planning and independent financial checks can start earlier.

## Risks that change the decision

| Risk / trigger | Response and owner |
|---|---|
| Missing IDs disproportionately hide failures | Pair 1 reproduces the exact coordinate recovery. Dropping the 18 rows removes 16 failures; report the before/after counts and investigate any mismatch. |
| 2026 stores do not represent the other 310 | Pair 2 compares geography and feature ranges. Flag unfamiliar profiles, test geographic sensitivity and qualify any rollout beyond well-represented stores. |
| Small sample or unreliable probabilities near 60% | Pair 2 reports fold variation and a sensitivity range for count/value. If the business conclusion changes, distinguish robust stores from marginal ones and propose a pilot. |
| Larger spend makes the forecast look like a targeting win | Pair 4 shows spend and store counts alongside net value, distinguishes history from a forecast repeat, and compares like budgets where scale drives the result. |
| Personas or product claims lack support | Pair 3 seeks the class materials; distinguish P&G evidence from team hypotheses. Connect messaging to a testable shopper action. |
| Workflow handoff fails or presentation overruns | Pair 4 tests an import early, checks relative/configurable input paths and times the talk. Cut optional material first. |

## Optional backlog — outside the core schedule

No extra is assigned by default. **Decision point: after Phase 3**, only if the required recommendation reconciles, an owner has spare time, and the team can preserve packaging and rehearsal time. Each attempted extra can score −1 to +1; skipping it scores zero. Include an extra only if it adds a defensible management insight within the same 10 content slides.

| Priority | Extra | Minimum useful result and stop rule |
|---|---|---|
| First candidate | **2 · Additional data** | Compare an open source (e.g. commuter flows) and a paid source (e.g. store footfall): what gap each fills, geographic coverage, join feasibility, cost/access and how to test added value on the same folds. Recommend one next acquisition. Retrieval and modeling are optional; claim no measured gain without a test. |
| Parked | **1 · Power BI dashboard** | No team member has Power BI experience. Revisit only with confirmed ownership, tool access and enough time to verify the PBIX and PDF against the store list. |
| Parked | **3 · Influencer shortlist** | The subject is power toothbrushes. Revisit only with sourced Meta/TikTok evidence and a clear distinction from the toothpaste recommendation. |
| Parked | **4 · LLM brand ranking** | Requires a defensible consumer prompt set and documented, comparable runs. Skip if the ranking cannot be substantiated. |
| Parked | **5 · GenAI consumer experience** | Requires a specific shopper problem and a credible way to assess the proposed experience. A prototype is optional. |

If no extra clears the decision point, proceed directly to packaging. **Next step after explicit approval of this roadmap and the spec: `/breakdown`.**
