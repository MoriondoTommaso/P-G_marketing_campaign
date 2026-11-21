# Store insights: what separates successful stores, and where coverage is thin

T07 / [#7](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/7) · Team 2 · Deniz

**Input:** the final `outputs/store-universe.csv` from T05 (480 stores: 108 success, 62 failure, 310 never activated). The KNIME workflow was not touched.
**Output:** [`outputs/store-profiles.csv`](../outputs/store-profiles.csv), one row per trait × group, plus geography and tercile rows.

**Rules followed:**
- The 310 never-activated stores are **unknown**, never failure.
- Nothing from the activation file (coordinates, match method, codes) is used as a trait. Latitude and longitude below come from the national store file.
- No value was normalised, filled or removed.
- Everything here is **descriptive history from 2026**. Any reason given for a pattern is a **hypothesis**, not a finding.

## How to read the numbers

For each trait we compare the 108 successes with the 62 failures by **median**. We also give one separation score:

> **Separation score** = the chance that a random successful store has a higher value than a random failed store.
> 0.50 means no difference. Near 1.0 means successes are higher. Near 0.0 means successes are lower.

The south is almost all successes (46 of 51 labelled stores below latitude 43°), so any trait that differs between north and south could look important just because of geography. To check this, we recompute the score **inside the north only** (latitude ≥ 43°: 62 successes, 57 failures). A trait that keeps its score there is not just a north/south effect.

## 1. Successes vs. failures (n = 108 vs. 62)

### Traits that clearly separate success from failure

| Trait | Median, successes | Median, failures | Direction | Score, all labelled | Score, north only | Hypothesis (not tested) |
|---|---|---|---|---|---|---|
| Distance from a Dentist | 9.0 | 155.0 | Lower in successes | 0.12 | 0.09 | Shoppers near a dentist are more likely to get a recommendation for an electric toothbrush. |
| Water hardness IDX | 40 | 89 | Lower in successes | 0.17 | 0.21 | Unclear. It may stand in for region or for other local factors we do not observe. |
| Online Consumption IYA | 277.5 | 239.5 | Higher in successes | 0.78 | 0.71 | Areas that buy more online may adopt tech-led oral care sooner. |
| Nr of Schools | 4 | 2 | Higher in successes | 0.76 | 0.78 | More schools suggest denser areas with families and more shopper traffic. |
| Latitude | 43.6 | 45.7 | Lower (further south) | 0.24 | 0.31 | Regional retail or shopper differences. |
| Longitude | 12.6 | 9.7 | Higher (further east) | 0.70 | 0.74 | Same as above. The far north-west holds many failures. |

Success rate by tercile of the labelled stores (from `store-profiles.csv`, `comparison = trait_tercile`):

| Trait | Low third | Middle third | High third |
|---|---|---|---|
| Distance from a Dentist | 51 / 57 = **89%** | 49 / 56 = **88%** | 8 / 57 = **14%** |
| Water hardness IDX | 54 / 60 = **90%** | 41 / 58 = **71%** | 13 / 52 = **25%** |
| Online Consumption IYA | 26 / 61 = **43%** | 38 / 55 = **69%** | 44 / 54 = **81%** |
| Nr of Schools | 33 / 72 = **46%** | 27 / 45 = **60%** | 48 / 53 = **91%** |

The overall 2026 rate is 108 / 170 = 64%. The break-even rate is 60%.

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
| Online Consumption IYA | 273.5 | 277 | Similar |
| Water hardness IDX | 49 | 37 | Similar range; all never-activated stores fall inside the labelled range |

Never-activated stores **outside the range** of the activated stores: Longitude 18, Graduated population 8, Avg Income per Household 5, and a few on the population traits (full list in `store-profiles.csv`, column `never_activated_outside_labelled_range`). Being inside the range on each trait separately does not guarantee the combination of traits is covered.

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
2. Take the median of `Distance from a Dentist` in each group. The result should be 9.0178 and 155.0148. Successes are closer to a dentist.
3. Count rows with `Latitude ≥ 44.5`: 30 successes, 53 failures, 83 blank.
4. Compare with the rows in `outputs/store-profiles.csv` for `trait = Distance from a Dentist` and `comparison = geography_region_band`.

## What this means for the model and the deck

- Team 3's model will probably lean on dentist distance, water hardness, online consumption, schools and geography. These are **associations from 2026**, not causes.
- Forecasts for never-activated stores in the dentist range 25–100, with 0 schools, or in the centre and south carry the most **extrapolation risk**. This belongs on the uncertainty slide (storyboard slide 8).
- A **bounded pilot** that deliberately includes some of these under-covered stores would fill the gaps faster than buying data alone.
