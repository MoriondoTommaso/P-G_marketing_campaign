# T09 — held-out model verification

Run `python3 validation/T09/check.py` from the repository root to check the
release against the T08 folds, labels and baseline. For a fresh Desktop run:

1. Import `workflows/oral-b-italy.knwf` into a KNIME Desktop 5.12 workspace
   inside `validation/T09/local/`. Point **input_dir** (#34) to the checkout's
   `data/` and **output_dir** (#35) to an empty folder under `local/`.
2. Reset and **Execute All**. Inspect training inputs at #82 (tree) and #102
   (logistic): only the five numeric features and nominal `target`. Scoring
   inputs #110 and #106 exclude the target and carry store IDs as row keys.
3. Run `python3 validation/T09/check.py path/to/fresh/held-out.csv`.

**Verified 2026‑11‑23, KNIME Desktop 5.12.0:** The final run completed at
12:02 CET. Nodes #111–114 (the two learners and their predictors) each completed
five iterations. No convergence warning or median-setting error was logged.
GroupBy's “No grouping column included” warning is expected: its input is
one fold's training partition and the desired output is one row of statistics.
The loader initially warned about reader variables before the path nodes ran;
the runtime universe, audit, folds and baseline exports matched T08 byte for byte.

Each fold held out 34 of the 170 labeled stores. For fold 4, the 136 training IDs
and 34 test IDs were disjoint. In an independent Gini tree reconstruction with
the specified constraints, all 34 fold‑4 probabilities matched within `1e-7`.
The checker reproduces one leaf count: `15596` scores `8/10` from training labels.

`held-out.csv`: 171 lines including header, SHA‑256
`8f219d30eb60cd898b963865f5fca302d267386b663e335d4b60ed00bb2840c5`.
All five source fields were observed and nonconstant in each training partition;
their measurement dates are unknown, so these predictions are retrospective.
