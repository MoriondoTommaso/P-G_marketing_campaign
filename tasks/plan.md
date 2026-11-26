# Delivery plan: Oral-B Italy 2027

**26 November model decision:** [Random Forest submission and release plan](../docs/final-model-decision.md). This amendment governs the next scoring/finance package and T13–T19 handoff; the historical delivery record below is retained.

The user approved [the specification](../docs/SPEC.md) and [roadmap](../ROADMAP.md) on 19 November 2026. This records approval of their content despite their original draft banners. Delivery is one annotated KNIME workflow, a traceable funding decision and a 10-minute management presentation. The course deadline is **27 November 2026 at 23:59 on MyLuiss**. The [internal schedule](../docs/TEAM_ASSIGNMENTS_AND_CONTRIBUTIONS.md#internal-deadlines-and-handoffs) sets a verified submission target of **16:00** and an absolute internal deadline of **18:00** (Europe/Rome).

## Team 1 handoff

Team 1's three deliverables are complete and available for handoff.

- **T01** — Teams 2 and 3 can use the [setup runbook](../docs/runbook.md) for input fingerprints, KNIME configuration and the T06 workflow handoff. Team 4's release-role confirmations and a second teammate's KNIME version check are pending for formal closure.
- **T02** — Teams 2–4 can use the [evaluation protocol](../docs/evaluation.md) for the fixed folds, model comparison, funding rule and independent financial checks. Team 3 can configure the workflow now and run it with the verified T06 snapshot. Record receipt at handoff.
- **T03** — Team 4 can use the [shopper evidence](../docs/shopper-evidence.md) to prototype shelf tactics, then use T07 and T11 for store-specific T14 actions. The teammate citation check is pending for formal closure. Persona-specific and SKU-specific copy depend on source confirmation.

## Work, in dependency order

| Two-person team | Exclusive issue block | Earliest start and handoff |
|---|---|---|
| Team 1 · Setup and evidence | #1–3 | Start at kickoff. Prioritize #1 to unblock the data join. Send #2's evaluation rules to Team 3 and #3's shopper evidence to Team 4. |
| Team 2 · Data and baseline | #4–7 | Start #4 immediately, in parallel with Team 1. Start #5 after #1. After #5, split #6 (benchmark/workflow) and #7 (store profiles) across the two members. |
| Team 3 · Modeling and targeting | #8–12 | Start #8 when **both #2 and #6** pass; no need to wait for #7. #10 does require #7 and #9. Release the list at #11 and the financial summary/workflow at #12. |
| Team 4 · Independent QA and presentation | #13–19 | Start **#14** once #3, #7 and #11 pass, even while Team 3 finishes #12. Start **#13** once #4 and #12 pass. #15 and #16 can overlap once their respective blockers clear. |

Each issue carries one `team-N` label on GitHub. Block boundaries assign responsibility; only the issue's native **blocked by** links control sequencing. The owning team records verification and closes its issue, even if others review or present.

[The ledger](todo.md) gives each task's owner, direct predecessors, size, outputs, acceptance checks and verification. [GitHub Issues](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues) mirror the tasks with native “blocked by” links. Use the same T-ID in evidence and handoffs; update the checkbox when its issue closes. XS is a short check or handoff; S and M each fit one focused session, with M reserved for work requiring multiple checks or artifacts.

**Issue index** (T-ID → GitHub issue):
[T01 → #1](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/1) · [T02 → #2](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/2) · [T03 → #3](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/3) · [T04 → #4](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/4) · [T05 → #5](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/5) · [T06 → #6](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/6) · [T07 → #7](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/7) · [T08 → #8](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/8) · [T09 → #9](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/9) · [T10 → #10](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/10) · [T11 → #11](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/11) · [T12 → #12](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/12) · [T13 → #13](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/13) · [T14 → #14](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/14) · [T15 → #15](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/15) · [T16 → #16](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/16) · [T17 → #17](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/17) · [T18 → #18](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/18) · [T19 → #19](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/19).

| Window | Task index | Checkpoint / evidence required |
|---|---|---|
| Nov 19 | T01 kickoff, T02 evaluation contract | Team 1 verifies names, environment, inputs, threshold cases and validation rules before model work. |
| Nov 19–20 | T03 persona evidence, T04 QA worksheet | Team 1 checks cited benefits; Team 2 checks historical arithmetic, zero-selection and slide allocation. |
| Nov 19–20 | T05 join audit, T06 historical baseline | Team 2 releases the checked T05 table immediately. Team 3 imports the T06 snapshot: reproduce 152 + 18 links, 310 unknown and €15,000 realized net before modeling. |
| Nov 21–22 | T07 profile evidence, T08 baseline predictions | Teams 2 and 3 check group counts, national coverage and stable fold assignments before interpretation. |
| By Nov 23 | T09 candidate predictions, T10 validate and choose | Team 3 checks 510 held-out decisions reconcile to fold and pooled totals, geographic evidence and the documented model choice. |
| By Nov 24, 21:00 | T11 score and stress-test, T12 release candidate | Team 3 verifies 480 scores, both comparisons, stress scenarios and the exact workflow/summary hashes handed to QA. |
| By Nov 25 | T13 independent finance QA, T14 shopper actions | Team 4 signs matching totals and the store-to-message evidence. Decide on a pilot or broader rollout. |
| Nov 26 | T15 fresh rerun, T16 deck | Team 4's release reviewer ties the PDF figures to the exact clean-rerun snapshot. An early deck draft is allowed; no final rehearsal with unverified figures. |
| Nov 26–27 | T17 rehearsals, T18 upload | Presentation lead signs two timed runs; named submission owner verifies uploaded copies and privately retains confirmation. |
| Following week | T19 live delivery | Presentation lead confirms actual Q&A rehearsal and live session with a teammate. |

**Critical chain:** T01 → T05 → T06 → T08 → T09 → T10 → T11 → T12 → T13 → release checks → T17 → T18 → T19. T02 feeds T08, T03/T07 feed T14, and T04 feeds independent QA. The precise AND-dependencies are in the ledger. Start an unblocked task without waiting for unrelated tasks in the same window.

**Checkpoint protocol:** reviewers record pass/fail and evidence on the relevant issues before closing them. At integrated workflow gates, import the designated snapshot, **Reset → Execute all** and record its hash. If a gate fails, leave the affected issue open, stop its dependent tasks and return it to the producer; independent lanes may continue. A changed workflow or financial summary voids prior QA: repeat T13/T15 on the new T12 revision, refresh any affected shopper claims and deck, then repeat T17 on the final PDF.

## Working agreements

- Team 2 edits the workflow through T06, then hands the editable copy and a `.knwf` snapshot to Team 3. Team 3 is the sole subsequent editor. Team 4 verifies an exported copy, owns the deck and runs the independent financial check. See the [named team assignments](../docs/TEAM_ASSIGNMENTS_AND_CONTRIBUTIONS.md).
- Keep `data/` read-only. Use the national store code as the output key, retain original headers at import, name KNIME stages by business action and annotate reasons. Store model inputs, held-out scores and funding outputs separately. Use configured paths and unrounded probabilities; sort decision exports by store ID for reproducible comparison.
- Run commands from the repository root. The spec's execution interface is KNIME **Reset → Execute all** (or execute the named stage while developing). Shell checks supplement the operator checks; there is no project test runner. Output paths in the ledger are contracts for the future tasks, not files expected at breakdown time. Tabular exports are UTF-8 CSVs with a header, one record per line and stable ordering.
- Controls: no fuzzy linkage or fabricated negatives; no target leakage; no causal, individual-level or market-share claims from catchment data. Use the approved all-480, uncapped base case unless new constraints are confirmed. Ask before changing assumptions or tools.
- The three selected extras run alongside the core tasks. Teams 1–3 hand their material to Team 4 by Nov 25 at 18:00 for the integrated presentation at 20:00. See the [optional activity briefs](../docs/TEAM_ASSIGNMENTS_AND_CONTRIBUTIONS.md#selected-optional-activities).
