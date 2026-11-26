# T-052: Team 2 linkage checkpoint — awaiting reviewer

**Status: automated pre-finance comparison PASS; Team 2 sign-off PENDING.** This is not a published RF release. A named Team 2 linkage reviewer must record PASS/FAIL on this exact candidate before final finance is generated. If the archive or the comparisons change, repeat the check.

**Candidate:** `workflows/oral-b-italy-final.knwf` at `a8cc8f5`; SHA-256 `f1d0b0985a4bb90be9f2c6fcdc45a2fab3e1cf14fd42612fffe95016696d1fca`. KNIME Analytics Platform **5.12.1** on macOS. In two fresh workspaces, reset the candidate's upstream graph, added read-only CSV taps at the named nodes, and executed the complete tapped graph. This exercises the actual learners, selectors and comparators; the finance and publication branches are deliberately outside this checkpoint.

| Input | Original SHA-256 | Reversed SHA-256, observed run |
|---|---|---|
| Activated_Stores.xlsx | `17ae67bcec8263bedcc1e20fe7f61638091349d442b922fb9f1ec541576a4796` | `d8a0018fa23ccc8940cc75d897b041755af367ed606f9744fc811d5fe386ae66` |
| Italian_Stores.xlsx | `f5b8cb8b68fe43499f4fb6c5793e8b40aacba9230f5aabdeee0bb66ed10a553f` | `06b553699477a1c9b774b1cc7a8a4033efb438e6d904ead66253f001bbad3e50` |

The reversed fixture preserves the workbook header, reverses every data row and updates cell references. The verifier checks worksheet and ZIP member contents, independent of ZIP timestamps.

### Results for the reviewer

All seven [pre-finance evidence tables](../validation/T52/review-data/) match byte-for-byte across runs, after keying and sorting. Verify against the committed tables, not against a manifest regenerated from the run under review.

| Evidence | Actual result |
|---|---|
| `links.csv`, `folds.csv` | 152 code + 18 coordinate links, 108 successes + 62 failures, 310 unseen. Each model's five actual test folds match the protocol's 170 IDs; fold-file SHA-256 `a5be2eeea3a41874ddb88db300c1f35fc9f7c052aab8f962a67f25b653ff9745`. |
| `oof-scores.csv`, `rf-refit-votes.csv` | All 170 OOF and 310 full-refit RF probabilities match by store; every denominator is 100. Baseline is derived from the fold's training labels only. Tree and logistic OOF scores also match. |
| `model-metrics.csv` | Held-out observed net: RF €90,000; tree €86,000; logistic €84,500; training-rate baseline funds all (€15,000); fund none €0. Includes per-fold and pooled Brier, AUC and near-threshold counts. One logistic fold reached its epoch limit in both runs. Geographic holdouts are separate and [below the protocol support thresholds](../docs/evaluation.md#geographic-robustness). |
| `tree-benchmark.csv`, `selection.csv` | 480 tree probabilities/strict comparator flags; 480 RF vote counts and Decision B flags. Exact selected IDs match the native filtered output: 108 historical successes and 168 previously unactivated stores. Counts are descriptive, not acceptance fixtures. |
| Native boundary fixture | Actual candidate Math Formula #142 and Rule Engine #94: 59/60/61 new-store votes → no/no/yes, including raw `0.6000000238418579`; 52-vote prior success → yes, 98-vote prior failure → no. |

The native forest learners #62 and #119 use 100 Gini trees, seed 2026, full-size random bootstrap with replacement, square-root feature sampling at each node; predictors #63 and #120 use hard voting and expose both class probabilities and model count. #45 explicitly selects only the target and the five approved predictors; #72/#73 fit and apply the logistic normalizer within each fold. Store IDs are row keys, not predictors. The pre-finance checker reads **success-class** votes, rejects non-100 denominators and off-grid probabilities, and independently rebuilds Decision B from observed labels and new-store votes.

### Reproduce before signing

```sh
D=$(mktemp -d "${TMPDIR:-/tmp}/t52.XXXXXX")
python3 -B validation/T52/native_folds.py "$D/A" > "$D/A.log" &&
python3 -B validation/T52/native_folds.py "$D/B" --reverse > "$D/B.log" &&
python3 -B validation/T52/pre_finance.py "$D/A" "$D/B" "$D/compared" &&
diff -ru validation/T52/review-data "$D/compared" &&
python3 -B validation/T52/native_boundary.py "$D/boundary"
```

**Reviewer record:** Name: pending · PASS/FAIL: pending · compared archive SHA / evidence revision / date: pending. Record the result here or on the T-052 PR. Do not promote the candidate, generate final finance or start #53 on this automated check alone.
