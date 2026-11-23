# Team 3 handoff for T16 · Why the model would fund a store

Use [the editable SVG](slide-03.svg) or [the PNG](slide-03.png) in **storyboard slot 3**. The two panels answer different questions on one slide: *Which model earned more?* and *Why would it fund this store?* Use the right panel as speaker notes if the chart needs more room. No additional content slide is needed.

### Suggested narration (about 45 seconds)

> We judged the models on the same 170 historical stores. The tree would have funded 108, including 100 successes and eight failures. Logistic regression funded 104, with 96 successes and the same eight failures. Those four additional successes account for the tree’s €4,000 advantage. Now take store 15596. The tree had not seen its result. Its distance to a dentist placed it with ten training stores, eight of which succeeded. At an 80% score, the expected return was €500 after cost, so the rule would fund it. The store actually failed. That is why we judge a policy across stores and recommend testing it in a pilot.

### The decision path, in the workbook’s original scale

| Fold‑4 decision for store `15596` | Evidence |
|---|---|
| Which way through the tree? | The store’s `Distance from a Dentist` was **0.10465**. In the audited reconstruction the first split asked whether distance was **≤54.1245** (yes); the next asked whether it was **≤0.4482** (yes). Both are in **source units**, not stated to be metres or kilometres. These are one fold’s splits, not national eligibility cutoffs. |
| Where does 80% come from? | Of the **136 training stores**, ten landed in this leaf: eight successes and two failures. Store `15596` was one of the 34 **test** stores and did not contribute to those counts. KNIME exported `0.800000011920929`, shown as 80%. |
| What decision follows? | Under the case assumptions, success adds €2,500 in sales and any activation costs €1,500. Expected net was **+€500**; realized net for this failed activation was **−€1,500**. Distance describes the tree’s decision, not a cause of success. |

**Evidence trail.** The score and actual outcome are in [`outputs/held-out.csv`](../../outputs/held-out.csv); the input value and fold are in [`store-universe.csv`](../../outputs/store-universe.csv) and [`folds.csv`](../../outputs/folds.csv). The thresholds come from the [independent fold‑4 reconstruction](../../validation/T09/README.md), not a screenshot of the final 170-store refit. Converting the two `log1p(distance)` thresholds back with `exp(t) − 1` gives the values above. All 34 reconstructed fold‑4 probabilities agree with the KNIME export within `1e-7`; [`validation/T09/check.py`](../../validation/T09/check.py) also checks the 8/10 leaf directly.

**Chart source.** Filter [`outputs/model-comparison.csv`](../../outputs/model-comparison.csv) to `validation=ordinary` and `fold=pooled`; plot `net_eur` from zero. These are **retrospective policy results using observed 2026 labels and case economics**, not 2027 forecasts or measured incremental lift. The €4,000 margin exceeds the €2,500 model-selection tolerance. Geographic validation did not meet its minimum class counts; see the [model-choice note](../../docs/model-choice.md) for the pilot rationale.
