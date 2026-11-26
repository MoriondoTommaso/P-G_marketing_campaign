# Decision after the independent review

> **Historical RC3 tree pilot.** For the confirmed 2027 policy use [Decision B](../final-model-decision.md) and the [current finance report and pilot instructions](../financial-report-class.html). The tree counts, leaf probabilities and stress tests below apply only to RC3.

**Authorize pilot design only.** The 278 stores are a model-implied planning scenario. Their €417,000 spend and €250,602.05 conditional case net are not a pilot budget, measured lift, or accounting profit. Only the 2026 outcomes are observed. Even the equal-spend comparison ranks and values both lists with the same scores.

### What could move the decision?

* **Transfer to new areas:** neither geographic split passed the prespecified class-support test. In the exploratory northern holdout the tree funded all 119 stores for −€23,500 case net. Pooled geographic Brier was 0.334 (ordinary folds: 0.081). Neither number estimates national prospective accuracy. The south represents 30% of labeled stores versus 54% of unactivated stores.
* **The refitted tree is exceptionally confident:** of the 170 new stores selected, 113 get a score of 1 from a leaf with 41/41 historical successes; 57 get 0.9423 from a leaf with 49/52. That implies 166.71 successes. Illustrative 95% Wilson intervals for the two historical proportions are 91.4–100% and 84.4–98.0%. These ignore leaf selection, dependence and geographic shift; they are not prediction intervals for new stores. Three held-out historical failures scored 100%.
* **Near break-even:** only four held-out tree scores fell in 55–65%, all above 60%. The prescribed ±5-point local stress leaves all 170 selected new stores untouched. In the [broad stress supplement](../../validation/issue31/broad-stress.csv), keep all 278 commitments and cut **every** score by 10, 20, 30 or 40 percentage points, flooring at zero. Conditional portfolio net falls to €181,102, €111,602, €42,102 and **−€27,398**, respectively. These are illustrative adverse assumptions, not fitted adjustments. Regenerate with `python3 validation/issue31/stress.py`.
* **Winner selection:** the same five folds compared and selected the tree. Its €4,000 lead corresponds to four funded successes, so selecting it may overstate its future advantage. Keep these five folds for the retrospective record. No calibration model has been fitted. Any future calibration must be fitted on separate training data or within inner folds and evaluated on untouched outer folds or prospective stores.

### Bounded prospective test

Before seeing outcomes, agree a maximum spend, duration, primary outcome definition and minimum sample size based on the smallest useful net difference. Freeze the tree, threshold and comparator. Within geographic bands and separately for new/repeat stores, randomly allocate comparable **pools** to tree targeting or current practice; give each policy the same activation budget. Record all eligible IDs, selections, actual spend, successes and failures. Compare realized case net per euro between arms with uncertainty; report each region and compare observed success to predicted probability. Decide the expansion criterion and stop rule in advance. Do not scale if support is thin or the interval includes material downside.

### What Team 2 can verify

The Italian store workbook supplies the following headers. Their interpretation below is descriptive; a header is not evidence of when the value was known.

| Workbook field | Meaning in this analysis | Unit or unresolved definition |
|---|---|---|
| Total Population | Population in the store area | People; catchment boundary unknown |
| Avg Income per Household | Mean household income | Reported in euros in T07; reference period and income basis unknown |
| Households avg components | Mean household size | Persons per household |
| Nr of Hygienists | Count of hygienists in the area | Persons; catchment definition unknown |
| Distance from a Dentist | Store-area dentist distance | Source units only; unit and distance method unknown |

For **each** field, the measurement date, reference date and availability before the 2026 activation are unverified. The historical list was selected; the selection criteria and inclusion probabilities are unknown. Team 2 should request the dated source dictionary and original selection brief. Until supplied, post-activation leakage and selection bias cannot be excluded: retain the retrospective-only qualification.
