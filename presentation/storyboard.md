# Storyboard: Oral-B Italy 2027 store activation

Rough outline for the 10-minute management deck on the 2027 Oral-B **toothpaste** in-store campaign in Italy (T04 / #4). Team 4 owns the final deck (T16). This outline reserves space; it does not fix the wording.

**Limits:** at most **10 content slides**, including the extras, plus **one separate contributions appendix**. Every number on a slide must come from the KNIME workflow or its exports. Label each figure as **history (2026)** or **forecast (2027)**.

Each slide title is an action title: a full sentence that states the conclusion. `[TBD]` marks a number that Team 3 or Team 4 fills in from KNIME.

| # | Working action title | What goes on the slide | Source | Owner | Time |
|---|---|---|---|---|---|
| 1 | Fund [TBD] stores in 2027 for a forecast net of €[TBD] | The decision in one line: which stores, how many, spend, forecast net. Show the recommendation and the case for a bounded pilot if validation does not support expansion. | `outputs/financial-summary.csv`, `outputs/activation-list.csv` | Team 4 | 1:00 |
| 2 | 2026 returned €15,000 net: 108 of 170 activations paid off | **History.** 170 activated, 108 successful (64%), €270,000 sales, €255,000 spend, €15,000 net. A store pays only when its success chance is above 60%: 59% → −€25, 60% → €0, 61% → +€25. | `outputs/baseline-2026.csv`, `outputs/finance-qa.xlsx` | Team 2 | 1:00 |
| 3 | The shallow tree earned the most in the 2026 backtest | Held-out net by model and one store’s decision: 8/10 training successes → 80% → +€500 expected net. [Slide artwork, speaker notes and evidence](model-evidence/README.md). | `outputs/model-comparison.csv`, `outputs/held-out.csv` | Team 3 | 1:00 |
| 4 | **Comparator A: Optimised list vs. repeating the 2026 list** | **Forecast.** Expected 2027 sales, spend and net for (a) the optimised list and (b) repeating the same 170 stores, under the same forecasting assumptions. Difference isolates targeting and scale. Also show optimised net minus the €15,000 realised in 2026, labelled forecast vs. history. | Size of Prize export (T12) | Team 3 | 1:00 |
| 5 | **Comparator B: Same-spend comparison** | **Forecast.** At the same spend as the 2026 list, how much more net does better targeting earn? Separates "better stores" from "more stores". | Size of Prize export (T12) | Team 3 | 0:45 |
| 6 | 2026 successes sat close to dentists, but most unscored stores sit where we have little evidence | Store traits that separate success from failure (direction, group sizes, explanations labelled as hypotheses). Map or table: activated vs. never-activated stores by region, showing that most never-activated stores are in the centre and south, where only 9 activations failed. | `outputs/store-profiles.csv`, `docs/store-insights.md` | Team 2 | 1:00 |
| 7 | **Shopper actions**: what to do in the selected stores | 2–3 in-store actions tied to the profiles of the selected stores. Each action traced to a profile count and a source; inferred needs labelled as hypotheses. | `docs/shopper-actions.md`, `docs/shopper-evidence.md` | Team 4 | 1:00 |
| 8 | **Uncertainty**: what could make the forecast wrong | Selective 2026 activation; north/south composition shift (south 46/5, north 62/57); never-activated stores further from a dentist than any activated store in their region; break-even sensitivity (stores near 60%); threshold sensitivity. Recommend a pilot where support is thin. | `docs/evaluation.md`, `docs/store-insights.md`, T11 sensitivity | Team 3 + Team 2 | 1:00 |
| 9 | Extra 2: Buy [source] first to fill [gap] | One slide: 3–4 candidate data sources (free and paid), the gap each fills, and how we would test it on the same 5 folds. No untested improvement claims. | `docs/additional-data.md` | Team 2 | 0:45 |
| 10 | Extras 3 + 5: Influencer shortlist and GenAI shopper experience | Half a slide each, or merge into slide 7 if space is short. | Team 1 and Team 3 extras | Teams 1 and 3 | 0:30 |
| A | **Appendix: Who did what** | One row per person (8 people), taken from the verified contribution logs. Not counted in the 10 content slides. | `docs/TEAM_ASSIGNMENTS_AND_CONTRIBUTIONS.md` | Team 4 | n/a |

**Total content time:** about 9:00, leaving one minute of slack inside the 10-minute slot.

## Space reserved (T04 acceptance)

| Required item | Slide |
|---|---|
| Optimised list vs. repeating the 2026 list | 4 |
| Same-spend comparison | 5 |
| Shopper actions | 7 |
| Uncertainty | 8 |
| Contributions appendix | A |

## Notes for Team 4

- If the extras do not fit, merge slide 10 into slide 7 rather than dropping the uncertainty slide.
- Slide 2 figures can be checked against `outputs/finance-qa.xlsx`, which is independent of KNIME.
- Keep history (2026) and forecast (2027) visually distinct, for example with a label in the corner of every chart.
