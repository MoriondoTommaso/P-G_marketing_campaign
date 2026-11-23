# Native funding threshold regression

The fixture starts at the tree predictor's output schema. Its six synthetic scores
include the widened IEEE binary32 values of 11/20, 6/10 and 13/20, an exact 0.6,
and controls 0.5999999 and 0.6000001. A separate raw column preserves the input.
The test exercises release nodes for validation decisions, calibration bins,
production decisions and all three stress scenarios. It does not train a tree.

The native Desktop 5.12 results are in `evidence/{red,green}`. In RC1 the 6/10
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
python3 -B validation/issue31/native/run.py \
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
