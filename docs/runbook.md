# T01 — Setup and reproducibility

The [task ledger](../tasks/todo.md#t01--record-the-team-environment-and-input-fingerprints) defines the setup checks. Use this runbook to verify the source workbooks and reproduce the KNIME handoff.

**Team 1 status: complete and ready for Team 2.** Team 4's role confirmations and the second teammate's KNIME check are pending for formal T01 closure.

## Teams and release roles

| Team | Members | Mandatory issues |
|---|---|---|
| 1 · Research & Methodology | Petra and Lollo | #1–3 |
| 2 · Data Preparation & Analytics | Ele and Denis | #4–7 |
| 3 · Predictive Modeling & AI | Tommy and Ale | #8–12 |
| 4 · Marketing Strategy, QA & Delivery | Bianca and Linda | #13–19 |

The roster matches the [team assignments](TEAM_ASSIGNMENTS_AND_CONTRIBUTIONS.md). Team 4 must confirm and record who fills each role before T01 closes. Assignments are pending confirmation.

| Team 4 role | Named owner |
|---|---|
| MyLuiss submission owner | Pending confirmation |
| Submission backup | Pending confirmation |
| Release reviewer | Pending confirmation |
| Presentation lead | Pending confirmation |

## KNIME environment

KNIME Analytics Platform **5.12.0** was independently verified from the installed app's `Info.plist`. The executable is native arm64 and its bundled Temurin Java **21.0.9** was checked directly. Install a build for the receiving machine's OS and CPU, and check the features below. Use the bundled Java runtime for Java Snippet and verify the fold export rather than assuming byte-identical model probabilities across platforms.

| Installed feature | Installed build | Use |
|---|---|---|
| KNIME Base nodes (`org.knime.features.base`) | `5.12.0.v202606261225` | Tables, joins, loops, aggregation, learners and predictors |
| KNIME Excel Support (`org.knime.features.ext.poi`) | `5.12.0.v202605041104` | Excel Reader for both source workbooks |
| KNIME File Handling Core (`org.knime.features.filehandling.core`) | `5.12.0.v202606231323` | Workflow path and file handling |
| KNIME Expressions (`org.knime.features.base.expressions`) | `5.12.0.v202606171353` | Derived fields, audit rules and decision arithmetic |
| KNIME Javasnippet (`org.knime.features.javasnippet`) | `5.12.0.v202606171353` | Stable fold keys inside KNIME |
| KNIME Ensemble Learning Wrappers (`org.knime.features.ensembles`) | `5.12.0.v202605041104` | Supplies the Tree Ensemble nodes used to fit and score the single decision tree |

The installed KNIME Statistics Nodes feature (`5.12.0.v202604281126`) is available. The primary evaluation uses the base loops and aggregations above. Check the application version in **About KNIME Analytics Platform** and feature builds in **Installation Details**. Record platform version, feature builds, OS, architecture and bundled Java in the run record. Team 2 records the actual T06 dependencies. Team 3 records any modeling additions. Manifests and node definitions were inspected on this host. Workflow import and execution await the T06 export.

## Inputs, hashes and base case

Run from the repository root on macOS or Linux.

```sh
shasum -a 256 data/Activated_Stores.xlsx data/Italian_Stores.xlsx
```

| Workbook | SHA-256 computed from the local file | Sheet and contents |
|---|---|---|
| `data/Activated_Stores.xlsx` | `17ae67bcec8263bedcc1e20fe7f61638091349d442b922fb9f1ec541576a4796` | `default`, 170 rows excluding headers, 4 columns. Store code, coordinates and binary activation outcome. |
| `data/Italian_Stores.xlsx` | `f5b8cb8b68fe43499f4fb6c5793e8b40aacba9230f5aabdeee0bb66ed10a553f` | `default`, 480 unique stores, 36 columns. Store code, coordinates and catchment attributes such as population, income, schools and dental access. |

### Schema and integrity checks

- National workbook. All 36 headers are unique and all 480 rows have numeric values in all 36 fields. `Pdv Code` is a positive integer and unique. `Latitude` and `Longitude` are numeric and the pair is unique. Other columns describe catchment demographics, households, household income, schools, hygienists, distance from a dentist, water hardness and online consumption. Source definitions, units and observation dates are incomplete. A numeric cell type does not establish measurement units or vintage.
- Activation workbook. `Pdv Code`, `Latitude` and `Longitude` are numeric when populated. Their missing counts are 18, 31 and 38, respectively. There are 152 distinct populated IDs and 132 distinct complete coordinate pairs. `Outcome of Activation` is populated text throughout, with the only values `incremental sales` and `no incremental sales`. Neither sheet contained duplicate full rows or formulas.

### Exact reconciliation

1. Read both sheets with `Pdv Code` as an integer key and coordinates as doubles. Keep a temporary unique activation-row key for the audit. Separate populated IDs from blank IDs before joining.
2. Join populated IDs to national IDs. A missing coordinate does not block a valid ID match. Compare each available activation coordinate against the corresponding national value as a conflict check. Audit and resolve any unmatched ID or coordinate conflict. Coordinate fallback is limited to rows with blank IDs.
3. For blank IDs, require both coordinates and exactly one national match on the ordered pair `(Latitude, Longitude)`. Check multiplicity before accepting. Use the raw numbers at source precision, with no rounding, tolerance or nearest-neighbor rule.
4. Append the linked branches with the link method for audit. Require one match per activation row and 170 distinct resolved national IDs. Left join the labels back to the 480-ID national table, retaining national predictors and leaving the other 310 outcomes missing. Halt before modeling if these invariants fail. Keep link method outside the predictor allowlist.

An independent check read the Excel XML values as exact decimals and repeated the coordinate matching with doubles to check reader compatibility. The two representations gave the same 18 unique recoveries. There were zero ambiguous, unmatched, multiply linked or conflicting rows. Team 2 must reproduce these counts and verify reader settings in KNIME.

| Link method | Successful | Unsuccessful | Total |
|---|---:|---:|---:|
| Nonblank store code | 106 | 46 | 152 |
| Unique exact latitude and longitude | 2 | 16 | 18 |
| Total linked | 108 | 62 | 170 |

The approved project base case covers all **480** national stores, allows repeat activation, and assumes **no binding budget cap or retailer quota**. These are project assumptions. Escalate any new cap, retailer constraint or eligibility restriction before changing them. The assignment assumes €2,500 incremental sales per successful activation, €0 per unsuccessful activation and €1,500 spend per activated store. The independent reconstruction yields **108/170 = 63.53%** success, **€270,000** case-imputed incremental sales and **€255,000** activation spend. The **€15,000** historical net uses observed binary outcomes and the stipulated euros per outcome. The workbook contains no store-level euro results, contribution margins or other costs needed to estimate accounting profit. [Group assignment, pp. 1, 3](Business%20and%20Marketing%20Analytics%20-%20Group%20Assignment.pdf#page=3) · [Approved project decision rules](SPEC.md#decision-rules-and-assumptions-for-approval)

## Configure and reproduce the workflow

1. Put **Create File/Folder Variables** at the top of the workflow and label its base location `input_dir` in the workflow annotation. Select the local checkout's `data/` directory with the chooser. Define `activated_file` and `national_file` so their resolved paths end in `Activated_Stores.xlsx` and `Italian_Stores.xlsx`. Connect the variable port to both **Excel Reader** nodes, use the local file system and bind each reader's file path to its corresponding variable. At handoff, change the base location once and check both resolved paths. Select `default` and use the first row as headers. Preserve the source headers. Check inferred types against the schema above before joining.
2. Check both input hashes on each machine. On Windows, run `Get-FileHash -Algorithm SHA256 -Path 'data/Activated_Stores.xlsx','data/Italian_Stores.xlsx'` in PowerShell from the repository root. Keep the source files read-only. Point writers to a separate writable output directory such as `outputs/rerun/` for independent QA. Keep €2,500 and €1,500 as named values in a single workflow configuration.
3. Team 2 checks the readers before joining. Confirm 170 activation rows and 480 national rows. Keep the activation file's blank ID cells as missing and check populated IDs are whole numbers before converting both ID columns to the same integer type. Keep coordinates as doubles. After the exact join, check `outputs/join-audit.csv` has 170 data rows and `outputs/store-universe.csv` has 480. At T06, check `outputs/baseline-2026.csv` against the historical totals above.
4. Team 2 exports the `.knwf` snapshot at T06. Team 3 imports it into a fresh workspace, sets `input_dir`, resets and chooses **Execute all**. Check 170 linked outcomes, 310 unknowns and the €15,000 historical net before starting T08. Record the snapshot revision, runtime environment, hashes and results in the handoff. Team 3 then owns the editable workflow and applies the [T02 evaluation protocol](evaluation.md).
5. Team 4 imports the finance-approved T12 export into a fresh workspace and reruns it against the same inputs. Check the audit counts, 480 decisions, selected store IDs and both Size of Prize comparisons against the release artifacts. [Delivery plan](../tasks/plan.md) · [T15 checks](../tasks/todo.md#t15--reproduce-the-exported-workflow-in-a-clean-workspace)

## Verification checklist

| Status | Check |
|---|---|
| Confirmed | Four pairs and eight distinct members match the repository roster. |
| Confirmed | Both input hashes were computed from the local workbooks. A read-only inspection reproduced the schema, link counts and historical benchmark. |
| Confirmed | KNIME 5.12.0 and the listed feature builds were found in the local installed app. The runbook records a single configurable input directory and the approved base case. |
| Pending | Team 4 confirms all four named release roles. |
| Pending | A second teammate checks their KNIME version and feature builds against this runbook and records the result. |
| Downstream · T06 | Team 3 tests the actual configured reader paths and reproduces the join and benchmark in a clean KNIME workspace. |
| Downstream · T15 | Team 4 reproduces the finance-approved release candidate and records independent QA evidence. |
