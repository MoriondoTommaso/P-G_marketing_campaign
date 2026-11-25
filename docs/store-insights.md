# Store insights: what separates successful stores, and where coverage is thin

See the [five-field provenance register and unresolved historical selection questions](model-review/pilot.md#what-team-2-can-verify) before using any trait prospectively.

T07 / [#7](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/7) · Team 2 · Deniz

**Input:** the final `outputs/store-universe.csv` from T05 (480 stores: 108 success, 62 failure, 310 never activated). The KNIME workflow was not touched.
**Output:** [`outputs/store-profiles.csv`](../outputs/store-profiles.csv), one row per trait × group, plus geography rows, tercile rows and Team 3's five model predictors by region.
**How it was calculated:** [`scripts/t07_store_profiles.py`](../scripts/t07_store_profiles.py). See [How the numbers were calculated](#how-the-numbers-were-calculated) at the end.

**Rules followed:**
- The 310 never-activated stores are **unknown**, never failure.
- Nothing from the activation file (coordinates, match method, codes) is used as a trait. Latitude and longitude below come from the national store file.
- No value was normalised, filled or removed.
- **Online Consumption IYA is not used as a driver.** We do not know whether it was measured before or after the 2026 campaign, so it could partly reflect the campaign itself. Team 2 agreed to keep it out of the model, the slides and Extra 2 (timing decision in [`docs/runbook.md`](runbook.md#online-consumption-iya-timing-decision)). Its numbers stay in `store-profiles.csv` for completeness only.
- **Units:** the unit of `Distance from a Dentist` is **not stated in the source** (it could be metres, kilometres or minutes), so all distances below are in source units. `Water hardness IDX` is an index whose base is not stated, so we only say higher or lower.
- Everything here is **descriptive history from 2026** about store catchment areas. It says nothing about individual shoppers, causes or market share. Any reason given for a pattern is a **hypothesis**, not a finding.

## How to read the numbers

For each trait we compare the 108 successes with the 62 failures by **median**. We also give one separation score:

> **Separation score** = the chance that a random successful store has a higher value than a random failed store.
> 0.50 means no difference. Near 1.0 means successes are higher. Near 0.0 means successes are lower.

The south is almost all successes (46 of 51 labelled stores below latitude 43°), so any trait that differs between north and south could look important just because of geography. To check this, we recompute the score **inside the north only** (latitude ≥ 43°: 62 successes, 57 failures). A trait that keeps its score there is not just a north/south effect.

## 1. Successes vs. failures (n = 108 vs. 62)

> The final KNIME workflow reproduces these medians (`outputs/eda-success-profile.csv`) and adds success rates by region and a within-region dentist check: see [`final-workflow.md`](final-workflow.md#eda-findings-170-activated-stores).

### Traits that clearly separate success from failure

| Trait | Median, successes | Median, failures | Direction | Score, all labelled | Score, north only | Hypothesis (not tested) |
|---|---|---|---|---|---|---|
| Distance from a Dentist (unit not stated in source) | 9.0 | 155.0 | Lower in successes | 0.12 | 0.09 | Areas with easy access to dental care may have more oral-care awareness, so a toothpaste activation finds more receptive shoppers. |
| Water hardness IDX (index, base not stated) | 40 | 89 | Lower in successes | 0.17 | 0.21 | Unclear. It may stand in for region or for other local factors we do not observe. |
| Nr of Schools | 4 | 2 | Higher in successes | 0.76 | 0.78 | More schools may point to busier areas with more families, so more shoppers pass the display. |
| Latitude | 43.6 | 45.7 | Lower (further south) | 0.24 | 0.31 | Regional differences in retailers or shopping habits. |
| Longitude | 12.6 | 9.7 | Higher (further east) | 0.70 | 0.74 | Same as above. The far north-west holds many failures. |

Success rate by tercile of the labelled stores (from `store-profiles.csv`, `comparison = trait_tercile`):

| Trait | Low third | Middle third | High third |
|---|---|---|---|
| Distance from a Dentist | 51 / 57 = **89%** | 49 / 56 = **88%** | 8 / 57 = **14%** |
| Water hardness IDX | 54 / 60 = **90%** | 41 / 58 = **71%** | 13 / 52 = **25%** |
| Nr of Schools | 33 / 72 = **46%** | 27 / 45 = **60%** | 48 / 53 = **91%** |

The overall 2026 rate is 108 / 170 = 64%. The break-even rate is 60%.

**Not used: Online Consumption IYA (timing unknown, not a driver).** In the 2026 data it is higher in successes (median 277.5 vs. 239.5, score 0.78; 0.71 inside the north). Because it may have been measured after the campaign, this could be partly an effect of the campaign rather than a trait of the store. We do not use it to explain success, and it stays out of the model, the slides and Extra 2.

### Traits that do **not** separate success from failure

These traits have a separation score between 0.38 and 0.56 overall:
- **Population and household size:** total population, male, female, every age band, marital status, total households, students, graduated and unoccupied population. They mostly measure the size of the area, and size alone does not tell successes from failures.
- **Nr of Hygienists:** median 1 in both groups (score 0.49).
- **Avg Income per Household:** median €18,269 in successes and €19,730 in failures. This is a moderate gap overall (0.38), but it disappears inside the north (0.54), so it looks like a north/south effect, not an income effect.
- **Households avg components:** no difference overall (0.53), with a weak reversal in the north (0.33).

## 2. Activated (170) vs. never activated (310)

### Geography

| Band (latitude) | Success | Failure | Never activated | Success rate among activated |
|---|---|---|---|---|
| North (≥ 44.5°) | 30 | 53 | 83 | 36% |
| Centre (41.5° – 44.5°) | 44 | 5 | 117 | 90% |
| South / islands (< 41.5°) | 34 | 4 | 110 | 89% |
| **Total** | **108** | **62** | **310** | **64%** |

With the two-band split from `docs/evaluation.md` (43°), the result is the same: the south has 46 successes, 5 failures and 167 never-activated stores, and the north has 62 / 57 / 143.

- **2026 activation leaned north.** Half the activated stores (83 of 170) are in the north band, but only 27% of the never-activated stores (83 of 310) are.
- **Most of the stores we would be scoring are in the centre and south** (227 of 310), where we have only **9 failures** in total. A model can learn "south = success", but it has almost no examples of a southern store that fails.

### Main traits

| Trait | Median, activated | Median, never activated | Comment |
|---|---|---|---|
| Distance from a Dentist | 15.6 | 48.5 | Different shape: see coverage gap 1 below |
| Nr of Schools | 3 | 0 | 157 never-activated stores have 0 schools nearby |
| Total Population | 138,666 | 83,563 | Never-activated stores serve smaller areas |
| Avg Income per Household | €19,090 | €17,734 | 5 never-activated stores fall outside the labelled range |
| Online Consumption IYA | 273.5 | 277 | Similar; timing unknown, not used |
| Water hardness IDX | 49 | 37 | Similar range; all never-activated stores fall inside the labelled range |

Never-activated stores **outside the range** of the activated stores: Longitude 18, Graduated population 8, Avg Income per Household 5, and a few on the population traits (full list in `store-profiles.csv`, column `never_activated_outside_labelled_range`). Being inside the range on each trait separately does not guarantee the combination of traits is covered.

### Team 3's five model predictors, region by region

`docs/evaluation.md` asks T07 to compare activated and never-activated stores on the model's predictors within each region. Rows `comparison = model_predictor_by_band` in `store-profiles.csv`. "Outside range" counts never-activated stores outside the range of the activated stores **in the same region**.

| Predictor | Region | Median, activated | Median, never activated | Never activated outside the region's range |
|---|---|---|---|---|
| Distance from a Dentist | North | 140.1 (n = 83) | 70.3 (n = 83) | 0 |
| | Centre | 3.5 (n = 49) | 65.8 (n = 117) | 0 |
| | South / islands | 5.7 (n = 38) | 22.4 (n = 110) | **35** (activated max is 28.5) |
| Avg Income per Household | North | €19,937 | €19,990 | 5 |
| | Centre | €19,626 | €18,281 | **16** |
| | South / islands | €15,555 | €13,112 | 2 |
| Total Population | North | 135,197 | 103,488 | 0 |
| | Centre | 139,226 | 86,741 | 12 |
| | South / islands | 135,544 | 60,227 | 4 |
| Nr of Hygienists | North | 1 | 0 | 10 |
| | Centre | 2 | 1 | 10 |
| | South / islands | 3 | 0 | 0 |
| Households avg components | North | 2.29 | 2.19 | 6 |
| | Centre | 2.32 | 2.45 | 6 |
| | South / islands | 2.51 | 2.56 | 5 |

- **Dentist distance is where the regions differ most.** In the centre and south, 2026 activated stores very close to a dentist (medians 3.5 and 5.7). The never-activated stores there are much further away (65.8 and 22.4). In the south, 35 of 110 never-activated stores are further from a dentist than any activated southern store.
- So the model will score many centre and south stores using a dentist distance it has only seen in the **north**, where most failures are. Their forecasts mix a "south" effect and a "far from a dentist" effect that the 2026 data cannot separate. This is a hypothesis about risk, not a measured error.

## 3. Data gaps (sent to Ele for Extra 2)

1. **Distance from a Dentist, middle range.** Between 25 and 100, there are **190 never-activated stores but only 13 activated ones** (7 success, 6 failure). Activated stores sit either very close (≤ 25: 100 stores) or very far (> 100: 57 stores). The pattern "close = success, far = failure" is not observed in the middle range, where most of the 2027 decisions are.
2. **Stores with no schools.** **157** never-activated stores have 0 schools. Only 27 activated stores do, and 25 of them failed. Any forecast for these stores rests on 27 examples.
3. **Few labelled failures in the centre and south.** There are only 5 failures in the centre band and 4 in the south / islands band, against 227 never-activated stores there. Success there may be overestimated.
4. **Size traits do not explain success.** Population, households and age bands do not separate the outcomes. We have **no store-level data**: store sales, footfall, store size or format, retailer, shelf space, competitor presence or price. The local census traits describe the area, not the store.
5. **Income is weak and confounded.** Income only separates the groups through the north/south split. Finer income data (by municipality) may help, but this is unproven.
6. **Water hardness is a strong signal with no explanation.** We do not know why it separates successes from failures. Region or local retail factors may be behind it (hypothesis).
7. **2026 activation was selective.** We do not know how stores were chosen in 2026, so the 170 may differ from the 310 in ways the data does not show.

## How to check this (T07 verify step)

1. Open `outputs/store-universe.csv`. Filter `success = 1` (108 rows) and `success = 0` (62 rows).
2. Take the median of `Distance from a Dentist` in each group. The result should be 9.0178 and 155.0148 (source units). Successes are closer to a dentist.
3. Count rows with `Latitude ≥ 44.5`: 30 successes, 53 failures, 83 blank.
4. Compare with `outputs/store-profiles.csv`: the medians are in the rows `comparison = success_vs_failure`, `trait = Distance from a Dentist`, and the band counts in the row `comparison = geography_region_band`, `group = North (lat >= 44.5)`.

## What this means for the model and the deck

- **Update, 25 Nov 2026:** the final submitted workflow *does* use **Water hardness IDX** and **Nr of Schools** (with Distance from a Dentist, Total Population and Avg Income per Household). This was recorded as an amendment, with a check that the result does not depend on the feature set: see [`final-workflow.md`](final-workflow.md#amendment-the-5-model-features). The next two bullets describe the earlier frozen protocol (RC3).
- **For Team 3:** the frozen model in `docs/evaluation.md` uses five predictors. Of these, only **Distance from a Dentist** clearly separates successes from failures (score 0.12, and 0.09 inside the north). **Income** separates them only through the north/south split (0.38 overall, 0.54 inside the north). **Total Population**, **Nr of Hygienists** and **Households avg components** do not separate them (0.49, 0.49 and 0.53).
- Two traits that separate strongly and hold inside the north are **not** in the model: **Water hardness IDX** (0.17) and **Nr of Schools** (0.76). **Online Consumption IYA** also separates them (0.78), but it is excluded under the timing decision and should not be added. We are not changing the model. The protocol is frozen, and any change would have to be agreed, recorded and justified as an amendment by Team 3 before rerunning, as `docs/evaluation.md` requires. Adding traits picked from the same 170 outcomes also risks overfitting.
- All of these are **associations from 2026**, not causes.
- Forecasts for never-activated stores in the dentist range 25–100, with 0 schools, or in the centre and south carry the most **extrapolation risk**. This belongs on the uncertainty slide (storyboard slide 8).
- A **bounded pilot** that deliberately includes some of these under-covered stores would fill the gaps faster than buying data alone.

## How the numbers were calculated

All numbers in this file and in `outputs/store-profiles.csv` come from one script, [`scripts/t07_store_profiles.py`](../scripts/t07_store_profiles.py), run on the KNIME export `outputs/store-universe.csv`. It only reads that file and writes `outputs/store-profiles.csv`. It does not change the data or the workflow.

From the repository root:

```bash
pip install pandas numpy
python scripts/t07_store_profiles.py
```

What it does, step by step:

1. Splits the 480 stores into success (108), failure (62) and never activated (310), using the `success` column.
2. For every trait, takes the count, mean, median, quartiles, minimum and maximum of each group.
3. Computes the **separation score**: it compares every successful store with every failed store (108 × 62 = 6,696 pairs) and counts how often the successful one has the higher value, with ties counted as half. This is the same number as the AUC of that single trait.
4. Repeats the score for the north only (latitude ≥ 43°).
5. Counts stores per latitude band, and the success rate in each third of the labelled stores for the four strongest traits (Online Consumption IYA is listed but not used, see above).
6. Compares Team 3's five model predictors between activated and never-activated stores inside each latitude band.

The counts and medians can also be checked by hand in Excel or with a KNIME **GroupBy** node on `outputs/store-universe.csv`.
