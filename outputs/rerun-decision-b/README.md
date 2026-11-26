# Decision B — Independent Reproduction Evidence

Independent verification performed by Linda Carla Zorzoli — Team 4, on 27 November 2026.

This directory contains the seven CSV files independently regenerated using KNIME 5.12.1 LTS in a clean workspace.

## Verification results

- 480 unique national stores.
- 276 exact selected store IDs.
- 480/480 Random Forest probabilities matching the T52 reference.
- Expected incremental sales: €590,525.
- Activation spend: €414,000.
- Expected net: €176,525.
- Equal-budget advantage: €129,075.

All seven copied CSV files were verified byte-for-byte against the independently generated outputs.

See `docs/rerun.md` for the complete verification methodology, SHA-256 fingerprints and remaining release limitations.

Independent clean-run reproduction: PASS.

Formal release approval: pending.
