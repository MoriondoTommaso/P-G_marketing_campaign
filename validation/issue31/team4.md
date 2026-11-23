# Independent release check (T13 / T15)

Use the **integrated candidate commit and SHA-256s** posted on issue #31, not
the earlier threshold-only run. Perform this check from a separate checkout
with a fresh KNIME workspace and an empty output folder. Record the actual
operator, KNIME version and commit.

1. Check out the pinned commit. Compute `shasum -a 256 workflows/oral-b-italy.knwf outputs/financial-summary.csv data/*.xlsx`.
   Compare the artifact hashes with the handoff and input hashes with the runbook.
2. Import `workflows/oral-b-italy.knwf`, set #34 to this checkout's `data`
   directory and #35 to the **empty** output folder, reset and Execute All.
   Verify that the release guard and all 13 CSV writers completed.
3. From the checkout run both commands below with the fresh folder, not `outputs`:

   ```sh
   python3 -B validation/issue31/reconcile.py /path/to/fresh/results
   python3 -B validation/T12/check.py /path/to/fresh/results
   ```

4. Complete the independent Team 4 finance worksheet using the fresh store-level
   outcomes and scores. Check the observed 2026 net (€15,000), conditional
   optimized forecast (€250,602.05), repeat forecast (€15,989.87), and
   equal-spend forecast difference (€153,433.21 at €255,000 per plan).
5. Report revision, hashes, 13-file comparison, financial differences, operator
   and accept/reject decision on T13 and T15. A producer rerun or a GitHub merge
   is not Team 4 sign-off. On any mismatch, retain the fresh output for diagnosis
   and identify the first differing file before considering another candidate.
