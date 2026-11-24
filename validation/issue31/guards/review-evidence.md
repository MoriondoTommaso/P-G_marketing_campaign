# Release-table regression tests

Run each mutation against a reset archive in a fresh destination. A passing
negative test requires `REVIEW_NATIVE_RESULT false`, a diagnostic for the
affected release table or metric, and an empty output directory.

```sh
scratch=$(mktemp -d)
git show 96fcb4a:workflows/oral-b-italy.knwf > "$scratch/rc2.knwf"
for case in inverted-activation zero-spend sensitivity-net finance-difference; do
  python3 -B validation/issue31/guards/run_cases.py "$scratch/rc2.knwf" "$scratch/red" "$case"
done
```

RC2 SHA-256: `056955825012242cb1a5b6befe14537dcf86d55b15571ef2c0af9611de3afcf8`.
For the fixed workflow, use its archive and a new `$scratch/green` destination.
Run `valid` as a control to reconcile all 13 exports with their references.

## RC2: reproduced with KNIME 5.12

All four native executions returned `true` and published 13 files each; each
regression test failed as intended. The exported data confirms each mutation:

| Case | Corrupt value published by RC2 |
| --- | --- |
| `inverted-activation` (#340) | Activation list contains 202 stores instead of 278. First store `100046` has `recommend_activate=0`. |
| `zero-spend` (#531) | `optimized_forecast` spends €0 on 278 stores instead of €417,000. |
| `sensitivity-net` (#349) | Store `100046`, base scenario: expected net €0 instead of −€1,500. All 1,440 rows remain. |
| `finance-difference` (#550) | `optimized_forecast` versus repeat is €234613.1819242835 instead of €234612.1819242835; sales, spend, and net remain correct. |

## RC3: verified with KNIME 5.12

Archive SHA-256: `8ffc1942669c6c266dc91a146d1f9ecfefa4573ba7878e4bc28f6400e83fc394`.
Each native run returned `false` and left **zero files** in its fresh output
directory. All four regression tests passed.

| Case | Observed native diagnostic |
| --- | --- |
| `inverted-activation` | `Release guard: activation mismatch 23848` |
| `zero-spend` | `Release guard: finance mismatch optimized_forecast` |
| `sensitivity-net` | `Release guard: sensitivity mismatch 22999 lower` |
| `finance-difference` | `Release guard: finance difference optimized_forecast` |
