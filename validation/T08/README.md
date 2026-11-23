# T08 Desktop validation

`workflows/oral-b-italy.knwf` is the release workflow. `outputs/folds.csv` and
`outputs/baseline-oof.csv` are its release exports. This directory preserves the
five CSV Writer outputs from each verified Desktop run in `evidence/A/` and
`evidence/B/`. A used the original store order; B reversed it at Sorter #21.

From the repository root, verify the saved runs without KNIME or external files:

```sh
python3 scripts/t08_validation.py check
```

To execute fresh runs with KNIME Desktop 5.12:

1. Run `python3 scripts/t08_validation.py prepare`. It unpacks the release
   workflow twice, binds the readers to this checkout's `data/` and binds all
   writers to `validation/T08/local/results/A/` or `B/`.
2. Choose `validation/T08/local/workspace/` as the KNIME workspace. Open `T08-A`
   and `T08-B` and **Execute All** in each.
3. Run `python3 scripts/t08_validation.py check-rerun`.

The `local/` directory is checkout-specific. The saved evidence, release
artifacts, and validation script are versioned. Neither check uses Downloads,
a temporary directory, or another workspace.
