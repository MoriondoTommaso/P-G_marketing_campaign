# T14 — Shopper actions for the funded stores

T14 / [#14](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/14) · Team 4 · status: delivered, peer trace pending.

**Current targeting for the storyboard — [Decision B](final-model-decision.md).** The [class activation list](../outputs/activation-list-class.csv) at `7fc7ff8` selects 108 past successes and 168 new stores. Joining those 276 IDs to the [store universe](../outputs/store-universe.csv) gives 64 North, 82 Centre and 130 South/islands; 103 have no nearby schools. Dentist-distance bands ≤25 / >25–100 / >100 contain 187 / 76 / 13 stores (source units). Use these candidate counts for planning, subject to #53. The original T14 analysis below documents the **historical RC3 tree list**, not Decision B.

**Inputs:** [T03 shopper evidence](shopper-evidence.md) · [T07 store insights](store-insights.md) with [`outputs/store-profiles.csv`](../outputs/store-profiles.csv) · [T11 funded list](../outputs/activation-list.csv) · [decision brief](model-review/pilot.md). The coverage table, the T07 tercile citations and the two financial figures below are recomputed and enforced by [`validation/T14/check.py`](../validation/T14/check.py); the remaining figures are quoted from the cited T03/T07 sources and await the peer trace on #14.

## What we can and cannot claim

- **The class personas were not identified in the supplied files** (T03 checked the assignment and case materials). No persona below is class-provided; the three shopper situations come from the T03 evidence-to-action matrix and are **team hypotheses**.
- No 2027 lineup or approved SKU wording is confirmed, so every message uses neutral descriptors only. A whitening descriptor is added only after the featured SKU and exact approved claim are confirmed.
- Store traits are descriptive 2026 history about catchment areas — associations, not causes (T07). Observed comparisons back the *store profiles*; the *consumer needs* remain hypotheses to validate with observed shelf tasks, intercepts or transaction data.

## The funded list the actions attach to

T11 funds **278 stores** — a model-implied planning scenario with **€417,000** spend and **€250,602.05** conditional forecast net, not an observed result ([decision brief](model-review/pilot.md)). Only the 2026 outcomes are observed. The list contains 100 of the 108 historical successes, 8 historical failures the model still rates above the 60% break-even, and 170 never-activated stores scored by refit.

## Selected-store coverage (T11 funded list × T07 profiles)

| Coverage metric | Funded stores |
|---|---|
| Funded stores, total | 278 |
| Latitude band North (>= 44.5) | 55 |
| Latitude band Centre (41.5 - 44.5) | 88 |
| Latitude band South / islands (< 41.5) | 135 |
| Dentist distance <= 25 (source units) | 194 |
| Dentist distance 25 - 100 (T07 gap range) | 84 |
| Dentist distance > 100 | 0 |
| Nr of Schools = 0 | 115 |
| Nr of Schools >= 1 | 163 |
| Held-out 2026 stores funded (successes + failures) | 108 |
| Held-out 2026 successes funded | 100 |
| Held-out 2026 failures funded | 8 |
| Refit-unseen stores funded | 170 |

## Actions

Each row ties a T03 shopper situation to an observed T07 store-profile comparison; the need, message, placement and measure follow the [T03 evidence-to-action matrix](shopper-evidence.md#evidence-to-action-matrix).

| Shopper situation | Supporting store profile | Consumer need | Message | In-store placement | Measure |
|---|---|---|---|---|---|
| A shopper at the main toothpaste fixture who has difficulty comparing variants (T03 situation 1). | All 278 funded stores are eligible; observed support is strongest in the 194 funded stores within 25 source units of a dentist, the profile where 2026 labelled success was high (T07 dentist terciles: 51 / 57 = 89% closest, 49 / 56 = 88% middle, 8 / 57 = 14% farthest). | Hypothesis: in catchments with easy dental access and presumed oral-care awareness (a T07 hypothesis, not a finding), a shopper deciding among variants wants a quicker way to find one that fits their routine. | “Find the Oral-B toothpaste that fits your routine.” with only approved variant descriptors. | Shelf-edge guide at the main toothpaste fixture, aligned with the relevant packs. | Share of timed variant-finding tasks completed within a limit fixed before the test; identical tasks and limit in both display conditions. |
| A shopper considering whether to trade up to a premium Oral-B option (T03 situation 2). | No supported store profile: no national trait in T07 speaks to premium willingness — Avg Income per Household does not separate successes from failures once the north/south split is removed (T07: score 0.38 overall, 0.54 inside the north). Do not target this action by profile. | Hypothesis: some shoppers want to understand how the available variants differ before considering a premium option. | “Compare Oral-B toothpaste options.” A whitening descriptor is added only after the featured SKU and exact approved claim are confirmed. | Small comparison card beside relevant toothpaste SKUs, prices clearly visible, only where the retailer permits it. | Premium Oral-B toothpaste units divided by all Oral-B toothpaste units, with the premium SKU list agreed before the test and total units tracked for substitution. |
| A shopper on a routine trip past the oral-care aisle (T03 situation 3). | 163 of 278 funded stores have at least one school nearby, and labelled success rises with schools (T07 schools terciles: 33 / 72 = 46% low, 48 / 53 = 91% high); 115 funded stores have none, a profile resting on only 27 labelled examples (T07 gap 2). | Hypothesis: school-dense catchments are busier family areas (a T07 hypothesis), so a routine-trip shopper may benefit from a replenishment reminder. | “Time to restock toothpaste?” | A retailer-approved secondary display near the oral-care aisle entrance. | Oral-B toothpaste units per store-week versus comparable usual-display stores, with a pre-period where available; POS counts cannot separate planned from unplanned buying, so state that limit. |

## Traits deliberately not used

- **Water hardness IDX** separates successes from failures (T07 score 0.17) but has no shopper-need mechanism we can articulate, so no action is built on it.
- **Online Consumption IYA** is excluded under the T07/runbook timing decision.
- **Income** and **geography alone** are not action bases: income only separates through the north/south confound, and the centre and south hold just 9 labelled failures, so regional success rates are weak evidence for any shopper claim.

## Framing: a bounded test, not a national rollout

Following the [decision brief](model-review/pilot.md), the 278-store list authorizes **pilot design only**. The in-store actions above should run as a **bounded pilot**: where feasible, randomize comparable funded stores to proposed versus usual displays, match observation windows, and record execution, stockouts, prices and promotions; analyze outcomes by assigned store and state the limits plainly if randomization is not possible. The pilot should deliberately include under-covered funded profiles — the 84 stores in the dentist-distance 25 – 100 gap range and the 115 stores with no schools nearby — because a pilot fills those evidence gaps faster than any additional desk analysis. Brand share is tracked only if the retailer supplies a consistent category denominator; store success labels cannot establish brand-share lift.

## How a peer verifies this (T14 verify step)

1. Trace each action's profile counts to [`outputs/store-profiles.csv`](../outputs/store-profiles.csv): the tercile citations are the `comparison = trait_tercile` rows for `Distance from a Dentist` and `Nr of Schools`.
2. Recompute the coverage table from [`outputs/activation-list.csv`](../outputs/activation-list.csv) joined to [`outputs/store-universe.csv`](../outputs/store-universe.csv); `python3 validation/T14/check.py` does exactly this and fails on any mismatch.
3. Confirm no class persona is asserted: the personas section states they were not identified in the supplied files, and every consumer need is labelled a hypothesis.
