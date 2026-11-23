# T11 — national funding plan

The chosen shallow tree supplies two distinct estimates: the **ordinary held-out**
score for each of the 170 historical activations, and a prediction for each of
310 unseen stores from a tree refitted on all 170 labels. Historical stores do
not get in-sample refit scores. The forecasts below mix two training sizes and
selectively observed histories; use them to plan a bounded pilot.

### Verified forecast (KNIME Desktop 5.12, 23 November 2026)

| Scenario | Score source | Selected | Spend | Forecast net |
|---|---|---:|---:|---:|
| Lower | Historical held out | 104 | €156,000 | €88,669.35 |
| Lower | Unseen refit | 170 | €255,000 | €161,778.85 |
| **Lower** | **All** | **274** | **€411,000** | **€250,448.20** |
| Base | Historical held out | 108 | €162,000 | €88,823.20 |
| Base | Unseen refit | 170 | €255,000 | €161,778.85 |
| **Base** | **All** | **278** | **€417,000** | **€250,602.05** |
| Upper | Historical held out | 108 | €162,000 | €89,323.20 |
| Upper | Unseen refit | 170 | €255,000 | €161,778.85 |
| **Upper** | **All** | **278** | **€417,000** | **€251,102.05** |

The base case has forecast incremental sales of €667,602.05. The local stress
test shifts only scores originally in `[0.55, 0.65]` by ±0.05; it is not a
confidence interval. **274 stores remain funded throughout.** The lower case
drops four historical IDs (`11439`, `2007563`, `28340`, `7717`); the upper
case adds none. `outputs/sensitivity.csv` records each scenario decision
and its change relative to base. Amounts above are displayed to cents only.

### Reproduce

1. Import `workflows/oral-b-italy.knwf` into Desktop, set the input and output
   folders at left, reset, and execute. Blocks 08–11 perform full-data preparation,
   refit/scoring, strict funding and decimal stress tests. The new exports are
   `national-scores.csv` (480 records), `activation-list.csv` (278) and
   `sensitivity.csv` (1,440); store IDs are text keys.
2. Import the isolated `validation/T11/funding-check.knwf`, point its output
   folder to the same fresh results folder, and execute. Its synthetic inputs
   cannot enter the funding list. At 59%, 60% and 61% the base net is −€25, €0
   and +€25 respectively, and only 61% funds. Shifting 55% up or 65% down
   yields an exact, unfunded 60% tie.
3. Run `python3 validation/T11/check.py path/to/fresh/results`. To check the
   release and the recorded boundary evidence instead, omit the path. The checker
   reconciles the 170/310 split, sorted selected rows, all row-level decisions,
   added/dropped ID sets and source/pooled scenario totals using decimal arithmetic.
