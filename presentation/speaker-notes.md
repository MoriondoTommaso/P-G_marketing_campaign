# Presenter brief: what to say and what to show

**The story in one sentence:** Past results tell us whom to repeat; forest votes help us choose where to expand; a controlled pilot tells us whether the forecast holds.

| Slide | Speaker cue | Evidence / visual |
|---|---|---|
| 1 | “The full list is an opportunity estimate. Today’s decision is whether to test it.” Do not describe €414,000 as the pilot budget. | Three numbers from the [decision brief](../docs/final-model-decision.md). |
| 2 | “At €1,500 per activation and €2,500 per success, 60% is break-even. We observed 108 successes out of 170.” | [2026 baseline](../outputs/baseline-2026.csv). Show sales minus spend, not a second model chart. |
| 3 | “Each historical store was predicted by a model that did not train on it. The forest led the comparison. For next year we deliberately repeat prior successes even when their votes are low.” | [Model comparison](../validation/T52/review-data/model-metrics.csv), `fold=pooled`. The €90,000 is a backtest using votes, not last year's actual net. |
| 4 | “At forest probabilities the repeats contribute €78,050 net, and the new stores €98,475. The full list beats repeating the old list in the forecast, but also spends more.” | Use the four-row [finance table](../docs/final-model-decision.md#numbers-to-use-in-the-deck). Keep the actual and forecast baselines visibly separate. |
| 5 | “Now fix both lists at 170 stores. Rank eligible stores by forest probability, breaking ties by text store ID. Spend is identical; the forecast net gap is €129,075.” | Label both bars **forecast**. The same probabilities rank stores and value them; this is not an experiment. |
| 6 | “Dentist proximity distinguished historical successes, but it does not explain why a shopper buys. Transfer to 310 unactivated stores is uncertain.” | [Store insights](../docs/store-insights.md). Use three latitude bands and avoid inventing a unit for dentist distance. |
| 7 | “Try a shelf sign that groups products by need. Compare it with the current shelf; record whether shoppers find the intended product and whether sales change.” Keep wording neutral and SKU claims approved. | [Shopper actions](../docs/shopper-actions.md). Use one shelf sketch, not a list of personas. |
| 8 | “Agree the cap and minimum worthwhile return before launch. Assign comparable pools to Decision B or current practice within region and repeat/new groups; give both arms the same budget and outcome window.” | [Finance report](../docs/financial-report-class.pdf). Track incremental sales, activation spend and net per euro by arm. |
| 9 | “First ask whether existing retailer data covers our stores. Test only information available before the campaign; don’t pay for an unproven improvement.” | [Additional-data recommendation](../docs/additional-data.md). |
| 10 | “The creator pilot concerns iO, not the toothpaste calculation. The GenAI concept is a separate shopper experience. Neither adds a euro to this forecast.” Finish: “Can we agree the pilot cap and success criterion?” | [Creator evidence](../docs/influencer-roster.pdf). Credit the eight contributors in the appendix. |

**Likely questions**

- **Why not activate every store above 60%?** Decision B uses the threshold only for new stores; past outcomes decide repeat membership. All stores still use forest probabilities for forecast euros.
- **What does net mean?** Expected incremental toothpaste sales minus activation spend, before product costs and overhead. It is not accounting profit.
- **How sure is the €176,525?** It is a planning estimate. At full spend, at least 166 of 276 activations must succeed to break even or better. The equal-budget pilot is how we test the forecast.
- **Which store list should I use?** In [the workflow selection table](../validation/T52/review-data/selection.csv), filter `recommend_activate = 1`. Do not copy IDs from the older class export.
