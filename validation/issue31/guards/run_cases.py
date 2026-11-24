"""Run native release controls and corrupt-input cases, using fresh destinations."""
import argparse
import os
import re
import signal
from pathlib import Path
import subprocess
import sys

from fixtures import CASES, ROOT, check, prepare


REVIEW_ERRORS = {
    "inverted-activation": r"activation (?:mismatch|membership)",
    "zero-spend": r"finance mismatch",
    "sensitivity-net": r"sensitivity mismatch",
    "finance-difference": r"finance difference",
}


def run(archive, scratch, case):
    dest = scratch / case
    prepare(archive, dest, case)
    log = dest/"native.log"
    # The macOS Eclipse launcher may keep an error dialog open even after the
    # workflow returned false. Stop only this fixture's private process group,
    # and only after the native API explicitly reported completion.
    with log.open("w") as out:
        proc = subprocess.Popen([sys.executable, "-B", ROOT/"validation/issue31/native/run.py",
                                 dest/"workspace/oral-b-italy", dest/"run"],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                start_new_session=True, text=True,
                                env={**os.environ, "JAVA_TOOL_OPTIONS":
                                     os.environ.get("JAVA_TOOL_OPTIONS", "")+" -Djava.awt.headless=true"})
        try:
            for line in proc.stdout:
                out.write(line)
                if line.strip() == "REVIEW_NATIVE_RESULT false":
                    break
        finally:
            if proc.poll() is None:
                os.killpg(proc.pid, signal.SIGTERM)
            proc.wait(timeout=15)
    trace = log.read_text()
    expected = case == "valid"
    if expected:
        assert proc.returncode == 0, log
    files = sorted(p.name for p in (dest/"output").iterdir())
    assert f"REVIEW_NATIVE_RESULT {str(expected).lower()}" in trace, (log, files)
    if not expected:
        # Duplicate training labels can be rejected even earlier by the native
        # learner-input RowID node; require the injected ID in that diagnostic.
        upstream_duplicate = case == "duplicate-label" and 'Encountered duplicate row ID "106570"' in trace
        assert "Release guard:" in trace or upstream_duplicate, f"unrelated workflow failure; inspect {log}"
        if case in REVIEW_ERRORS:
            assert re.search(r"Release guard: " + REVIEW_ERRORS[case] + r"\b",
                             trace, re.IGNORECASE), f"missing {case} diagnostic; inspect {log}"
    check(dest, case)
    print(f"{case}: native {'pass, exports reconciled' if expected else 'rejected before all writers'}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("scratch", type=Path)
    parser.add_argument("cases", nargs="*")
    args = parser.parse_args()
    for case in args.cases or CASES:
        if case not in CASES:
            parser.error(case)
        run(args.archive, args.scratch, case)
