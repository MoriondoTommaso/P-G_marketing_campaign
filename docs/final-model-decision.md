# Confirmed store-selection policy: Decision B

On 26 November 2026 the campaign owner confirmed **Decision B** for [#51](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/51). The five-feature Random Forest scores all 480 stores. **Use the observed 2026 result to select repeat stores, and forest votes to select new stores.**

| Store cohort | Include in the 2027 planning list if… | Probability used to forecast euros |
|---|---|---|
| 170 stores activated in 2026 | The activation succeeded in 2026, regardless of the vote count. | Out-of-fold forest success votes ÷ 100. A past success is not a 100% forecast. |
| 310 not previously activated | At least 61 of 100 trees vote for success. A 60-vote tie is out. | Success votes ÷ 100 from the forest refitted on all 170 labeled stores. |

At [`7fc7ff8`](https://github.com/MoriondoTommaso/P-G_marketing_campaign/tree/7fc7ff8), the [activation list](../outputs/activation-list-class.csv) contains **108 repeats and 168 new stores**: 276 in total, **€414,000 spend** and **€182,250 forecast net**. Expected net per funded store is always `€2,500 × p − €1,500`. The ±5-point sensitivity changes scores in the original 55–65% band; repeat membership stays fixed. The €90,500 retrospective result evaluates the forest's vote rule on held-out 2026 stores, **not** Decision B using those stores' already-known outcomes.

**Acceptance is by store ID, not count.** Applying the vote threshold to everyone would also select 276 stores, but swap seven repeats in each direction and forecast €191,200. Under Decision B, repeat `8914` is in (past success, 52 votes) and repeat `23781` is out (past failure, 98 votes). New store `3330` is out at 60 votes. The complete expected ID set is the union of historical success IDs and new-store IDs with 61–100 success votes.

**Handoff:** #51 resolves the business policy. [#52](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/52) tracks workflow verification; [#53](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/53) tracks independent financial sign-off; [#49](https://github.com/MoriondoTommaso/P-G_marketing_campaign/issues/49) tracks the audit. This amendment supersedes the all-store funding rule in the [original RF release plan](https://github.com/MoriondoTommaso/P-G_marketing_campaign/blob/0e35db52845d135ae86a7ca39b9c5f38b6d3797f/docs/final-model-decision.md). The remaining verification requirements stand. Use these figures for bounded pilot planning, not as proven national returns.
