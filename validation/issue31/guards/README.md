# Issue 31: verify before publishing

From the repository root:

```sh
python3 -B validation/issue31/guards/build.py input.knwf guarded.knwf
CANDIDATE=guarded.knwf python3 -B validation/issue31/guards/test_wiring.py
python3 -B validation/issue31/guards/run_cases.py guarded.knwf /absolute/new/scratch
```

Use the reset release candidate for `input.knwf`; it may already contain the
tree correction (#601–602). The builder retains writer IDs and data feeds and
moves all 13 writers into block 14. Each writer also depends on successful
execution of the same native validation node. Run with an empty output directory:
blocking a writer does not delete exports from previous runs.

* **Activation identity:** The original activation row ID survives the code
  and exact-coordinate joins. Unmatched left rows are retained. The gate compares
  the original and matched row sets, checks distinct store IDs and binary labels,
  and consumes the existing code/coordinate conflict audit. National IDs are
  checked against the original national reader, independently of joins.
* **OOF identity:** The baseline retains the held-out fold. Logistic and tree
  scores are tagged with the actual held-out iteration, without using fold as a
  predictor. Both within-fold joins require `(store_id, fold)` and retain unmatched
  rows; a native abort rejects missing scores. For ordinary folds 1–5, block 14
  compares all 510 finite model probabilities and model/store/fold identities
  with the assigned folds for the 170 distinct historical labels.
* **National identity:** Block 14 compares the actual 480 scored IDs against
  the original store set, rejects duplicates and invalid probabilities, and
  checks each ID's score source against its historical membership.
* **Empty input:** A singleton sentinel ensures the native check executes even
  when every evidence table is empty. The evidence uses KNIME-generated row IDs,
  integer-derived store IDs, and controlled model/source labels.

The test script uses KNIME 5.12 and the sibling `native/run.py` integration
runner. It localizes **copies** of both Excel inputs and makes fresh output
directories. The clean run must return true and match all 13 reference CSVs
byte for byte. Negative cases require an actual native rejection and an empty
output directory. To inspect or run an individual fixture:

```sh
python3 -B validation/issue31/guards/run_cases.py guarded.knwf /absolute/new/scratch wrong-fold
```

`fixtures.py prepare` also prepares the same cases for Desktop execution. On
the unguarded candidate, the `conflict` fixture writes all 13 CSVs despite
its deliberately inconsistent activation coordinates.

The eight negative cases cover an unmatched activation, a code/coordinate
conflict, a repeated label, a dropped OOF fold, a duplicated model/store pair
at unchanged cardinality, a shifted within-fold join key, a duplicated national
score branch, and an incorrect historical/unseen source. A duplicate historical
store can fail first at the existing RowID node; this is a valid rejection only
if its error identifies the injected duplicate and the output directory is empty.
