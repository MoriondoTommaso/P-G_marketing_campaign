# Final decisions: Oral-B Italy 2027

**Ask:** Approve a capped pilot of Decision B against current practice at equal spend. The **276-store planning list** would cost **€414,000** and generate **€176,525 forecast net**. The pilot budget is a separate decision; the team is not asking to spend the full amount now.

| Decision | What we chose |
|---|---|
| Which stores? | Repeat all **108** stores that succeeded in 2026. For the **310** previously unactivated stores, fund only those with **61–100 success votes**: **168** qualify. A 60-vote tie breaks even and is out. |
| Which model? | Use the five-feature Random Forest with 100 trees. On the same 170 held-out historical stores, its retrospective net was **€90,000**, versus **€86,000** for the tree and **€84,500** for logistic regression. Keep those two as comparisons. |
| How are euros valued? | Use forest probabilities for **both** cohorts. A past success earns a repeat place, not a guaranteed sale. Expected net per activation = €2,500 × success probability − €1,500. Repeat stores contribute **€78,050**; new stores **€98,475**. |
| How should the campaign run? | Test a simple shelf guide by shopper need and a short routine demonstration. Measure purchase and campaign return against current practice. Treat store traits as associations, not shopper diagnoses. |
| What data and extras? | Seek existing store-level oral-care sales history before buying data. Keep OpenStreetMap counts out of the five-feature model. Treat the iO creator and GenAI concepts as separate tests; no revenue from them is in the toothpaste forecast. |
| When to expand? | Set budget, duration, outcome window and minimum worthwhile return before launch. Expand only if observed pilot results meet that criterion. |

### Numbers to use in the deck

| Scenario | Stores | Incremental sales | Spend | Net |
|---|---:|---:|---:|---:|
| 2026 actual, at case values | 170 | €270,000 | €255,000 | €15,000 |
| 2027 forecast: repeat the same 170 | 170 | €268,000 | €255,000 | €13,000 |
| 2027 forecast: top 170 in Decision B | 170 | €397,075 | €255,000 | €142,075 |
| **2027 forecast: full Decision B list** | **276** | **€590,525** | **€414,000** | **€176,525** |

The full plan is **+€161,525 vs 2026 actual** and **+€163,525 vs repeating the 170**; both comparisons spend €159,000 more. At the **same €255,000 budget**, the forecast advantage is **+€129,075**. None of these differences is observed lift.

**Source of record for the deck:** [store IDs, votes and funding flags](../validation/T52/review-data/selection.csv) and [pooled model results](../validation/T52/review-data/model-metrics.csv) from the [snippet-free workflow](../workflows/oral-b-italy-final.knwf), archive revision `a345811`. Filter `recommend_activate = 1` for the exact list. The older `outputs/*-class.csv` package uses four different membership decisions; do not use it for slide figures. These calculations are for presentation planning; independent finance sign-off is pending.
