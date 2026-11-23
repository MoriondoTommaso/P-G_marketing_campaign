# T12-RC1 — Team 4 finance handoff

**Historical RC1 handoff.** Issue #31 requires a corrected candidate and a fresh independent rerun before delivery. The 278-store list is a [planning scenario, not a national rollout recommendation](model-review/pilot.md). RC1 artifacts are pinned
to commit `8b5fd515e25399e79d59a1c1d643d1afa7c676fb`, based on T11 at
`96925fd`. RC1 is the first T12 candidate. A later change to the workflow,
inputs or financial export requires a new candidate identifier, hashes and
an explicit notice to Team 4 that the earlier candidate is superseded.

## What Team 4 should reconcile

These figures come from the verified RC1 Desktop export and were independently
recomputed from the unchanged T11 store scores. Only the 2026 row is observed.
All forecast policies use the same probability wherever a store appears.

| Policy | Stores | Sales | Spend | Net |
|---|---:|---:|---:|---:|
| 2026 actual | 170 | €270,000.00 | €255,000.00 | €15,000.00 |
| Optimized forecast | 278 | €667,602.05 | €417,000.00 | €250,602.05 |
| Repeat-170 forecast | 170 | €270,989.87 | €255,000.00 | €15,989.87 |
| Matched optimized forecast | 170 | €424,423.08 | €255,000.00 | €169,423.08 |
| Matched repeat forecast | 170 | €270,989.87 | €255,000.00 | €15,989.87 |

- **Optimized forecast minus realized 2026 net: €235,602.05.** This is forecast
  versus history, not measured incremental lift.
- **Optimized forecast minus repeat-170 forecast: €234,612.18.** This compares
  two plans under the same economics and includes a €162,000 spend difference.
- **At equal spend: €153,433.21 forecast net difference.** The 108-store count
  difference exceeds the 17-store trigger. Rank by unrounded probability
  descending, then text store ID ascending; take the best 170 eligible national
  stores versus the best 170 historical stores. The latter is the entire repeat
  list here. The ranking gives the model-implied advantage by construction,
  not independent evidence of targeting lift. It does not change the base list.

## Artifacts and verification

| RC1 artifact (repository path) | SHA-256 |
|---|---|
| `workflows/oral-b-italy.knwf` | `79d2d4dc83b166bda9f804e151c32418f29cdb2f69cf91774006552287e1e9d8` |
| `outputs/financial-summary.csv` | `11a33bd099dba704063b4698631bc300c508521c9f6f3320ce59fb23cecb80dd` |

On 23 November 2026, KNIME Desktop 5.12 completed the financial-summary writer
at 19:57 CET. All 12 upstream CSVs matched the previous release/evidence. The
post-run export was packaged without cached data from the executed workspace:
all 330 archive members matched the candidate after restoring only the local
input/output paths to their release defaults. The two editor color-rendering
errors in the Desktop log did not prevent execution or affect the reconciled CSV.

Use `outputs/national-scores.csv`,
`outputs/activation-list.csv`, `outputs/held-out.csv` and
`outputs/baseline-2026.csv` for independent reconciliation. Core calculations
retain full precision; this document rounds to cents only.

In a fresh KNIME workspace, set input directory #34 and output directory #35,
reset the workflow, and **Execute All**. Run
`python3 validation/T12/check.py <fresh-output-directory>` from the checkout.
Before running, verify both **committed** artifact digests with
`shasum -a 256 workflows/oral-b-italy.knwf outputs/financial-summary.csv`.
After running, compare the fresh summary with the pinned CSV and report the
revision, hashes and any variance on #12. This handoff does not imply Team 4
has already verified or accepted the candidate.
