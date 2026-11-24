# Reading the Oral-B Italy workflow

Open `oral-b-italy.knwf`. At the left, set **input_dir** to the checkout's `data/`
and **output_dir** to an empty writable directory. The third settings node holds
the two euro assumptions. Double-click a numbered block to inspect its nodes;
the annotation at the top of each block explains its purpose.

| Block | Question it answers | Principal output |
|---|---|---|
| 01 Reconcile stores | Which national store belongs to each observed activation? | Join audit and 480-row universe |
| 02 Historical value | What did activating all 170 stores return? | 2026 baseline |
| 03 Assign fixed folds | Which fold holds out each labeled store? | Seeded, outcome-stratified mapping |
| 04 Validate models | What would each model predict without this store’s label? | Training-rate, logistic and shallow-tree probabilities |
| 05 Publish predictions | Which probabilities can we compare on the original five folds? | Baseline and held-out score files |
| 06 Decide funding | Does the unrounded score **exceed** break-even? | Ordinary decisions and separate exploratory audit |
| 07 Compare policies | What did each policy earn, how accurate was it, and how much support is there near 60%? | Fold, band and pooled comparison |

Inside **04**, follow *Split train and test* → *Impute training medians* →
*Learn feature mask*. The tree takes unscaled inputs. The logistic path adds
training-only centering and scaling. The two geographic refits are for
exploration only: neither latitude layout meets the minimums for validation.

Funding flags, realized euros, squared errors, medians used for imputation,
calibration flags and control comparisons use native KNIME nodes. The remaining
snippets handle the frozen ID/hash/ranking algorithm, numerically stable `log1p`,
null-safe standardization and composite row keys. The business rule is visible
in **06** as a Math Formula, with costs supplied by the shared settings node.

The native tree predictor exports a single-precision leaf frequency, widened
to double. For example, 6 successes in 10 rows becomes `0.6000000238418579`.
Blocks **04** and **09** restore the exact 55%, 60% and 65% boundary values
before passing tree scores to **any** downstream calculation. Their Rule
Engines match only the three binary32 encodings; they do not round neighboring
scores or modify logistic or baseline scores. With at most 170 labels, a
different leaf fraction is at least `1/(20 × 170)` away from one of these
boundaries, much farther than binary32 representation error. Thus a genuine
break-even tie stays unfunded and the prescribed ±5-point stress preserves
exact ties too. Recheck the denominator bound if the training population changes.

### Recheck the grouped workflow in Desktop

1. Run `python3 scripts/t08_validation.py prepare --run grouped` to prepare a
   fresh A/B workspace inside `validation/T08/local/grouped/`. B reverses the
   upstream store order. Run `python3 validation/T10/prepare_boundary.py` to
   create an isolated three-row fixture using the release funding and bin nodes.
2. In KNIME, open the `grouped/workspace` directory as a workspace and execute
   both `T08-A` and `T08-B` (each contains the **full** workflow). Import
   `validation/T10/local/boundary/Funding-boundary.knwf` and execute it.
3. From the repo root:
   ```sh
   python3 scripts/t08_validation.py check-rerun --run grouped
   python3 validation/T09/check.py validation/T08/local/grouped/results/A/held-out.csv
   python3 validation/T09/check.py validation/T08/local/grouped/results/B/held-out.csv
   python3 validation/T10/check.py validation/T08/local/grouped/results/A
   python3 validation/T10/check.py validation/T08/local/grouped/results/B
   python3 validation/T10/check_boundary.py validation/T10/local/boundary/boundary.csv
   ```
   The fixture checks scores immediately below, exactly at, and immediately
   above 60%. Its rows never enter the store exports.

**Verified on KNIME Desktop 5.12.0, 23 Nov 2026.** Both runs completed seven
iterations per learner and predictor, with no learner warnings or logged errors.
All A/B export hashes matched except for the deliberately reversed store
universe. The [saved run hashes and boundary rows](../validation/T10/grouped-evidence/)
are for release archive SHA-256
`71722cbe791a08a9d4f4cc1e18fe8b03c30aeb8174f185d676f557561f367219`.
