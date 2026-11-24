# Native funding threshold regression

## Trained 6/10 leaf: held-out prediction

The production Tree Ensemble Learner (#322) trains on 20 labeled rows. At
`population=100` six targets are `success` and four are `failure`; at
`population=200` all ten are `failure`. The other four features are constant.
With one tree, full sampling without replacement, minimum node size 20 and
minimum child size 10, the only useful split separates those two groups.
A separate, unlabeled Table Creator supplies one `population=101` row to the
soft-voting Tree Ensemble Predictor (#327). Neither input table contains a score.
Both nodes use their release model settings unchanged. One CSV writer taps the
predictor directly; the other records the release funding calculation.

| Native KNIME 5.12 run | Raw P(success) | Policy P(success) | Expected net (€) | Funded | Checker |
|---|---:|---:|---:|---:|---|
| RC1 `c23610a` | 0.6000000238418579 | 0.6000000238418579 | 0.000059604644775390625 | 1 | red (exit 1) |
| PR32 `96fcb4a` | 0.6000000238418579 | 0.6 | 0 | 0 | green (exit 0) |

Both workflows executed successfully. See `evidence/trained-red/` and
`evidence/trained-green/` for the native CSVs and checker output. Reproduce from
the repository root, first with `mode=red`, then with `mode=green`:

```sh
D=validation/issue31/threshold
mode=red
f=Issue31-trained-$mode
python3 -B "$D/fixture.py" --trained "$mode"
unzip -qo "$D/local/$f.knwf" -d "$D/local/engine"
JAVA_TOOL_OPTIONS=-Djava.awt.headless=true python3 -B validation/issue31/native/run.py \
  "$D/local/engine/$f" "$D/local/new-runtime-$f"
python3 -B "$D/check_trained.py" "$D/local/$f"
```

Use a new runtime directory for each invocation. The trained fixture reads both
release archives from the pinned git revisions above.

## Injected-score policy controls

The original fixture starts at the tree predictor's output schema. Its six synthetic scores
include the widened IEEE binary32 values of 11/20, 6/10 and 13/20, an exact 0.6,
and controls 0.5999999 and 0.6000001. A separate raw column preserves the input.
The test exercises release nodes for validation decisions, calibration bins,
production decisions and all three stress scenarios. It does not train a tree.

The native Desktop 5.12 results are in `evidence/{red,green}`. In RC1 the injected 6/10
base row was funded at an expected net of €0.000059604644775390625; corrected
production and stress both report zero net and no funding. The upper scenario
on 11/20 is another zero-net tie. All 54 corrected output rows pass `check.py`.
The isolated native runner independently reproduced both versions, with all six
CSVs byte-identical to Desktop. The full release run returned
`REVIEW_NATIVE_RESULT true` for archive SHA-256
`13994e7f3bedf2209c70f73ff7d64a9322c22db8ca577cd0d211d33763cf8e47`.
Its 13 exports matched the reviewed references (`evidence/full-export-sha256.txt`).

From the repository root, run the commands below once per mode (red first,
then green) with KNIME 5.12 installed. Red reads the RC1 archive from git;
green reads the current release, including #601 and #602. The archives have
machine-local output paths, so generate them on the execution machine.

```sh
D=validation/issue31/threshold
mode=red  # then mode=green
python3 -B "$D/fixture.py" "$mode"
unzip -qo "$D/local/Issue31-$mode.knwf" -d "$D/local/engine"
JAVA_TOOL_OPTIONS=-Djava.awt.headless=true python3 -B validation/issue31/native/run.py \
  "$D/local/engine/Issue31-$mode" "$D/local/runtime-$mode"
python3 -B "$D/check.py" "$D/local/Issue31-$mode"
```

Alternatively, import each archive into KNIME Desktop and choose **Execute all**,
then run the same checker. The workflow execution must succeed for both versions;
the checker must return 1 for red and 0 for green. For a second headless run,
provide a new scratch directory to `run.py`.

To execute the full corrected release and reconcile its outputs independently
(choose a new `run` name each time):

```sh
D=validation/issue31/threshold
run=full
python3 -B "$D/full.py" "$run"
JAVA_TOOL_OPTIONS=-Djava.awt.headless=true python3 -B validation/issue31/native/run.py \
  "$D/local/$run/oral-b-italy" "$D/local/$run/runtime"
python3 -B validation/issue31/reconcile.py "$D/local/$run/outputs"
```
