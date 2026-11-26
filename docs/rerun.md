# T15 — Reproduction evidence and release history

**Current recommendation: Decision B (Random Forest, 276 stores).** See the first section for the current verification. The subsequent RC3 and Decision Tree sections are superseded historical evidence, not current recommendations.

## Current verification — Decision B (27 November 2026)

- Independent operator: **Linda Carla Zorzoli — Team 4**, T15 / issue #15.
- Repository snapshot: `c384317c305bc9e8914cccf8a94446b00c2afd61` (ZIP comment); workflow revision identified in the decision document: `a345811`.
- Environment: macOS, KNIME Analytics Platform 5.12.1 LTS; exact build and macOS version not recorded.
- Independent clean-run reproduction: **PASS within the checks below**. T13 independent workbook submitted in PR #57; reviewer approval and updated finance export reconciliation are pending.

### Input and reference fingerprints

| Artifact | SHA-256 |
|---|---|
| `workflows/oral-b-italy-final.knwf` | `d12c0933814f3671f84881d3c09080462815e81586a7c9b476f2c6acbe1dde7c` |
| `data/Activated_Stores.xlsx` | `17ae67bcec8263bedcc1e20fe7f61638091349d442b922fb9f1ec541576a4796` |
| `data/Italian_Stores.xlsx` | `f5b8cb8b68fe43499f4fb6c5793e8b40aacba9230f5aabdeee0bb66ed10a553f` |
| `extra2/osm-counts-2026-01-01.csv` | `b8e21e6577bcb909de9cdb86248f6bc0eeb00dec3c00ca4ebac666567625bb63` |
| `validation/T52/review-data/selection.csv` | `918b214211268c2eff9aa918980f54abca647ff58bfb9bee35c717145c580148` |
| `validation/T52/review-data/oof-scores.csv` | `43e0f42bf0b22700eeaacec7cc23dfe7c486ca686aa7e43ad67f34329121ee8e` |
| `validation/T52/review-data/rf-refit-votes.csv` | `f90964791339d8922fa7acff8058d883d169b400e90e267ba310f84ddb1fc0ed` |

### Procedure

1. Extracted the repository into `P-G_FINAL_DECISION_B` and verified workflow and reference hashes. Imported the workflow into a fresh workspace `knime-workspace-DECISION-B-T15`.
2. Import reported IDLE-to-CONFIGURED node-state warnings. The workflow opened in an unexecuted state; Reset all was disabled. No node settings were modified.
3. Verified all three embedded input hashes and confirmed `data/outputs/` was empty using `ls -la outputs`.
4. Executed all; operator inspected the canvas and reported green nodes. Seven native CSVs were generated at approximately 00:03 local time on 27 November.
5. Used Python standard-library CSV and Decimal calculations to check unique IDs, activation membership, exact reference probabilities, financial totals and historical join counts. A first long terminal paste failed with a syntax error; subsequent shorter commands completed successfully. No workflow rerun or data modification was required for that error.
6. Copied the seven exports into `outputs/rerun-decision-b/`; all seven `cmp -s` comparisons against the fresh workspace files passed. Recorded hashes with `shasum -a 256 outputs/rerun-decision-b/*.csv`.

### Fresh evidence manifest

| File in `outputs/rerun-decision-b/` | Data rows | SHA-256 |
|---|---:|---|
| activation-list-class.csv | 276 | `084f24976c0de965ff49a3c455a04528412e18ce83e51509808f12970f23a958` |
| baseline-2026.csv | 1 | `6df5ad9f263783a114030377f2455027c90e8e1f7542433a39af09947591f55e` |
| eda-region-success.csv | 9 | `c4d73571bdb2bc5a8745b14c55506672ca3fc2e17f6ab87477dee204728530e7` |
| eda-success-profile.csv | 2 | `4dcdb64dfb9218be88beb8bbce23f44272791b279dd8c9b6eb22e8e747da480a` |
| join-audit.csv | 170 | `a8bf662688b25788edc57dd0b6f9ef37dd1ac1debad720b3efc70f7ae3d534a1` |
| national-scores-class.csv | 480 | `7b746ac0b6745208bcc4e528bf554087fe0b0233d5c3fbfd2bb6ee1c8818adfa` |
| store-universe.csv | 480 | `17be4d40346fb87957e8382f33b61eb1125f8904c734d94491ad7ff1067b83b4` |

### Reconciliation

| Check | Result |
|---|---|
| National score rows / unique IDs | 480 / 480 |
| Selected rows / unique IDs | 276 / 276 |
| Activation ID set vs national funding flags | Exact match |
| Activation ID set vs T52 selection reference | Exact match |
| National ID-to-probability map vs T52 votes / 100 | 480/480 exact matches |
| Activation rows vs corresponding national score rows | 276/276 exact matches |
| Historical score-source count | 170 |
| Join audit rows / unique resolved IDs | 170 / 170 |
| Code / coordinate matches | 152 / 18 |
| Historical successes / failures | 108 / 62 |

Decision B repeats the 108 historical successes and funds 168 previously unactivated stores with more than 60 out of 100 success votes, as specified by T52. The exact selected ID set was reproduced; this is not a universal probability-threshold policy for historical stores. Both cohorts use Random Forest probabilities for expected sales. The T13 workbook separately reconstructs the policy from the source predictions.

### Financial reconciliation

Expected sales = sum of selected probabilities × €2,500; spend = selected count × €1,500; expected net = sales minus spend. Repeat forecast uses all 170 historical scores. Equal-budget optimized scenario takes the top 170 expected net values within the selected Decision B list.

| Scenario | Stores | Sales (€) | Spend (€) | Net (€) |
|---|---:|---:|---:|---:|
| 2026 actual | 170 | 270,000 | 255,000 | 15,000 |
| Repeat forecast | 170 | 268,000 | 255,000 | 13,000 |
| Decision B full forecast | 276 | 590,525 | 414,000 | 176,525 |
| Decision B equal-budget forecast | 170 | 397,075 | 255,000 | 142,075 |

Size of Prize versus actual: €161,525; versus repeat forecast: €163,525; equal-budget advantage: €129,075. All headline values agree with the T13 workbook and `docs/final-model-decision.md`. Forecasts are conditional planning estimates, not realized future returns.

### Scope, limitations and release status

- This is independent clean-run reproduction on the original input order, not a repetition of the adversarial integrity tests or reversed-input fold tests. No claim is made that all audit blockers are resolved.
- The import warning did not prevent the observed execution. A complete warning log was not captured. Input files were not edited; filesystem read-only permissions were not established.
- The seven hashes above are operator-reported fingerprints; copying was checked byte-for-byte, not equality of every fresh file against the older repository exports. The fresh CSVs have not been independently uploaded to this reviewer for byte inspection at the time of this report. EDA exports were checked for presence and row counts, not full cell-by-cell equality.
- The separate `outputs/financial-summary-class.csv` in the tested snapshot is stale (SHA-256 `c9f44b62a053af652cb255d6113ad4973235dcb623e59bedb2b49e632c01d1e5`); it was not treated as a valid reference. Team 3 is responsible for replacing it. The corrected export must be reconciled against this run and bound to the accepted release manifest.
- Technical clean-run verification: PASS. Formal T13/T15 reviewer acceptance, corrected finance export verification and final release-integrity approval remain pending. A changed workflow hash requires renewed verification. No source workflow changes are submitted by this operator.

---

## Superseded historical verification records

# T15 — Independent clean-workspace reproduction (RC3)

- Issue: #15 (Team 4); prerequisite: T13, approved according to the operator and shown closed on GitHub.
- Operator/reviewer: Linda Carla Zorzoli
- Date: 24 November 2026
- Environment: macOS, KNIME Analytics Platform 5.12.0; fresh workspace `knime-workspace-T15`. Exact macOS build not recorded.
- Artifact revision: `e1185d746bdb37d1cae4e55fac14741ae3a9def5` (RC3; pinned GitHub ZIP snapshot, not a Git clone).
- Result: reproduction PASS; local validation commands completed successfully; formal sign-off and repository integration pending submission/review of this evidence.

## 1. Input and release identity

The operator ran `shasum -a 256 workflows/oral-b-italy.knwf outputs/financial-summary.csv data/Activated_Stores.xlsx data/Italian_Stores.xlsx` in the separate RC3 folder before import. The recorded values match the release handoff and T01 runbook.

| File | SHA-256 |
|---|---|
| `workflows/oral-b-italy.knwf` | `8ffc1942669c6c266dc91a146d1f9ecfefa4573ba7878e4bc28f6400e83fc394` |
| `outputs/financial-summary.csv` | `11a33bd099dba704063b4698631bc300c508521c9f6f3320ce59fb23cecb80dd` |
| `data/Activated_Stores.xlsx` | `17ae67bcec8263bedcc1e20fe7f61638091349d442b922fb9f1ec541576a4796` |
| `data/Italian_Stores.xlsx` | `f5b8cb8b68fe43499f4fb6c5793e8b40aacba9230f5aabdeee0bb66ed10a553f` |

## 2. Execution procedure

1. Downloaded the pinned RC3 archive to a separate local folder (`P-G_RC3_T15`). Created `outputs/rerun/` separately from the reference exports.
2. Created a fresh KNIME workspace and imported the original RC3 workflow archive. The earlier exploratory run and its layout edits were not used as formal evidence.
3. Changed only the input directory (#34) to `data/` and the output directory (#35) to `outputs/rerun/` within that separate folder. Confirmed all 13 generated output paths. Retained the original economic variables (€2,500 per success; €1,500 per funded store).
4. Reset all and executed all. All 14 numbered blocks, including 14 Verify and publish, displayed execution checkmarks. All 13 CSV files were generated. Saved only the local imported workflow. No analytical nodes or annotations were edited in the formal run.

Source workbooks were used as inputs, not edited during the run; filesystem read-only permissions were not independently established. The original archive was not re-exported as a new release candidate.

## 3. Reconciliation and audit counts

The operator's Terminal comparison found 12 byte-identical files under `outputs/`. The initial CHECK for `spatial-decisions.csv` occurred because the reference is stored in `validation/T10/`, not `outputs/`. Subsequent verification of the uploaded rerun ZIP against the repository's official reference files and integrated hash manifest (using the supplied repository copy) confirmed all 13 byte-identical matches. No data discrepancy was found.

| Check | Result |
|---|---:|
| National universe / unique national IDs | 480 / 480 |
| Historical activations / unique matched IDs | 170 / 170 |
| Matched by store code | 152 |
| Matched by coordinates | 18 |
| Historical successes / failures | 108 / 62 |
| Previously unseen stores | 310 |
| National funding decisions | 480 |
| Funded / unfunded | 278 / 202 |
| Activation list unique IDs | 278 |
| Exact funded ID set and finance reconciliation | PASS |

| Policy | Stores | Sales (€) | Spend (€) | Net (€) |
|---|---:|---:|---:|---:|
| 2026 actual | 170 | 270,000.00 | 255,000.00 | 15,000.00 |
| Repeat forecast | 170 | 270,989.87 | 255,000.00 | 15,989.87 |
| Optimized forecast | 278 | 667,602.05 | 417,000.00 | 250,602.05 |
| Matched optimized | 170 | 424,423.08 | 255,000.00 | 169,423.08 |
| Matched repeat | 170 | 270,989.87 | 255,000.00 | 15,989.87 |

Size of Prize: optimized versus 2026 actual €235,602.05; optimized versus repeat forecast €234,612.18; equal-spend forecast difference €153,433.21. These are model-implied planning comparisons, not measured future lift.

## 4. Official validation commands

The two repository scripts were executed against the uploaded fresh rerun ZIP and supplied reference repository copy: both exited successfully. `reconcile.py` confirmed all 13 reference comparisons; `check.py` reported `Verified 278 optimized, 170 repeat, 2026 actual; matched comparison: True, k=170.` and unittest `OK` (one test).

For operator-side evidence, run from the pinned RC3 folder:

```sh
python3 -B validation/issue31/reconcile.py outputs/rerun
python3 -B validation/T12/check.py outputs/rerun
```

Operator-side script execution: confirmed on 24 November 2026. `reconcile.py` returned all 13 CSV SHA-256 values without a visible error; `check.py` reported `Verified 278 optimized, 170 repeat, 2026 actual; matched comparison: True, k=170.` and `Ran 1 test in 0.004s`, followed by `OK`. The operator retained the Terminal screenshot as evidence. T13 finance worksheet was previously prepared in Google Sheets and submitted in PR #34; fresh outputs are identical to the reference inputs used for that reconciliation. Native Excel recalculation was not tested.

## 5. Warnings, differences and limitations

- Import reported IDLE-to-CONFIGURED state changes for the Variable Creator and both file/folder variable nodes, and deprecated Table Creator and Table Row To Variable Loop Start nodes in block 04, plus a deprecated Table Creator in block 14. No replacements were made. These warnings did not prevent successful execution.
- The earlier exploratory run required macOS Desktop access permission and included annotation layout adjustments. The formal run used a fresh import without those edits.
- The spatial reference location explained the initial CHECK; no output changes were needed.
- Reproduction verifies consistency of this release, not future campaign performance. Formal acceptance remains with the Team 4 reviewer; update the task ledger when acceptance is recorded.

---

# T15 — Independent reproduction of the final submitted workflow

- Date: 26 November 2026; operator: Linda Carla Zorzoli.
- Pinned GitHub ZIP revision: `98adfb472075f63130092a419ef418528286195c` (ZIP comment). This is the tested snapshot, not a claim about the current main branch tip.
- Environment: macOS, KNIME Analytics Platform 5.12.1 LTS (About dialog confirmed; exact build and macOS version not recorded).
- Status: technical reproduction PASS; formal T15 reviewer acceptance pending. Final finance workbook PR #48 was merged; separate issue-level sign-off was not independently established.
- Scope: `workflows/oral-b-italy-final.knwf`, superseding RC3 for submission. The historical section above is retained as evidence only; its 278-store result is not the final plan.

## Final release and inputs

| Artifact | SHA-256 |
|---|---|
| `workflows/oral-b-italy-final.knwf` | `8073a6174337dc1c2a7666b0b3e5dc03581e7d8c8f1349f9b68547cf60d74634` |
| `outputs/financial-summary-class.csv` | `0c65bdde3ada29f83fc24a5ff4bce2392a1da4e147706aafba734fa4bbadd9de` |
| `data/Activated_Stores.xlsx` | `17ae67bcec8263bedcc1e20fe7f61638091349d442b922fb9f1ec541576a4796` |
| `data/Italian_Stores.xlsx` | `f5b8cb8b68fe43499f4fb6c5793e8b40aacba9230f5aabdeee0bb66ed10a553f` |
| `extra2/osm-counts-2026-01-01.csv` | `b8e21e6577bcb909de9cdb86248f6bc0eeb00dec3c00ca4ebac666567625bb63` |

The operator verified the release workflow and financial summary hashes before import. All three embedded `data/inputs/` files matched their repository counterparts by SHA-256.

## Clean execution

1. Extracted the pinned repository into `P-G_FINAL_T15` and imported the final workflow into a new workspace `knime-workspace-FINAL-T15`.
2. Initial KNIME 5.12.0 import reported a newer workflow version. Updated KNIME and its listed extensions to 5.12.1 LTS, restarted and opened the workflow successfully.
3. In the imported workflow's `data/` folder, renamed the existing `outputs` directory to `outputs_original` and created an empty `outputs` directory. No analytical configuration or source archive was changed.
4. Used Reset all and Execute all. Seven fresh native CSV exports appeared in the empty output directory. The inspected Rule-based Row Filter warning stated “Node created an empty data table.” Its output had 0 rows and 40 columns, as required by the conflicting-coordinates audit. No fix was needed.
5. Compared each fresh CSV against `outputs_original` with `cmp -s`; copied the fresh files into the separate local repository's `outputs/rerun/` directory and compared them against `outputs/` reference files using `cmp -s` again. All comparisons passed on the operator's Mac. The uploaded fresh CSVs were also checked against the supplied repository and embedded archive copies.

| Native CSV | Data rows | Embedded original | Repository reference |
|---|---:|---|---|
| activation-list-class.csv | 287 | PASS | PASS |
| baseline-2026.csv | 1 | PASS | PASS |
| eda-region-success.csv | 9 | PASS | PASS |
| eda-success-profile.csv | 2 | PASS | PASS |
| join-audit.csv | 170 | PASS | PASS |
| national-scores-class.csv | 480 | PASS | PASS |
| store-universe.csv | 480 | PASS | PASS |

All 14 comparisons were byte-for-byte matches. No missing reference or difference was reported. Original reference exports remain unchanged.

## Independent financial reconciliation

Using the fresh national scores and historical join audit, the selected IDs were checked against the exact set satisfying `p_success > 0.60`. There are 480 unique national IDs, 170 unique matched historical IDs (152 code, 18 coordinates; 108 successes, 62 failures), and 287 funded stores. Expected net per funded store is `2500 * p_success - 1500`. Repeat uses all 170 historical stores; matched optimized uses the top 170 national probabilities. Actual 2026 uses observed outcomes rather than probabilities.

| Policy | Stores | Sales (€) | Spend (€) | Net (€) |
|---|---:|---:|---:|---:|
| 2026 actual | 170 | 270,000.00 | 255,000.00 | 15,000.00 |
| Repeat forecast | 170 | 270,105.49 | 255,000.00 | 15,105.49 |
| Optimized forecast | 287 | 664,653.75 | 430,500.00 | 234,153.75 |
| Matched optimized | 170 | 395,306.26 | 255,000.00 | 140,306.26 |
| Matched repeat | 170 | 270,105.49 | 255,000.00 | 15,105.49 |

Optimized vs 2026 actual: €219,153.75; optimized vs repeat forecast: €219,048.27; equal-spend difference: €125,200.77 (differences calculated before rounding). These agree with `outputs/financial-summary-class.csv` to cents. The finance summary is a separate reference calculation, not an eighth native KNIME output. The €88,000 held-out backtest reported in `docs/final-workflow.md` is based on observed historical outcomes and is distinct from forecast net. RC3 validation scripts were not treated as final workflow acceptance tests.

## Limitations and acceptance

The exact installed build number and a complete workflow-wide warning log were not recorded. The inspected empty-table warning was expected and did not prevent reproduction. The operator executed KNIME locally. Native Excel recalculation was not tested as part of this rerun. Reproducibility does not establish future campaign performance or eliminate model-validation limitations documented in `docs/final-workflow.md`. Technical evidence is ready for review; formal acceptance and repository integration of this T15 evidence remain pending.
