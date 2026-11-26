# What the Random Forest uses to rank stores

The forest can be explained without relying on training-set split counts. In a new KNIME 5.12.1 diagnostic, the final class workflow's 100-tree forest was fitted on four of the five store-ID folds (`20261120`) at a time. The unmodified held-out predictions matched the [independent review](model-selection-2026-11-26.md) at all 170 store IDs: Brier 0.06462 and €90,500 observed case net.

For each fitted forest, one feature at a time was shuffled among the stores in its **test fold only**. The forest was not refitted. Twenty permutations per feature were scored; each reported change compares all 170 held-out stores with the unshuffled predictions. The funding rule was strictly more than 60 of 100 success votes. Random permutations used ascending numeric store IDs and Python `random.Random(2026 + 100 * fold + repeat).shuffle(...)` with one-based folds and repeats 0–19.

| Feature shuffled | Mean increase in Brier (worse) | Mean loss of case net at the funding threshold |
|---|---:|---:|
| Distance from a Dentist | 0.19222 | €60,150 |
| Nr of Schools | 0.02685 | €3,275 |
| Water hardness IDX | 0.01332 | €4,550 |
| Avg Income per Household | 0.00299 | €3,700 |
| Total Population | 0.00179 | €175 |

**Interpretation for managers:** dentist distance is the strongest signal the forest uses on these historical stores. School count and water hardness also help its probability estimates. The order of secondary predictors changes when measured by funding decisions rather than probability error. The loss figures are not additive, budgets, causal effects, or the value of changing a store's attributes. Shuffling can break geographic and other correlations; these tests neither isolate causal drivers nor validate transfer.

This resolves the question of whether the forest can support a clear feature story. It does not change the [geographic net-value comparison](model-selection-2026-11-26.md#model-evidence).

## Does the forest gain anything from the other four features?

Shuffling measures what the fitted forest relies on. To test what it gains from including the features, separate native forests were **retrained** with (a) dentist distance only, (b) the other four only, and (c) all five. The same 170 stores, held-out partitions, fixed learner settings and `>60/100` vote rule were used for each comparison. Values are ROC-AUC / Brier / observed case net.

| Predictors in forest | Five ID folds (`20261120`) | Leave one geographic cell out, 15 km training exclusion |
|---|---|---|
| Dentist only | 0.929 / 0.104 / €78,000 | 0.911 / 0.123 / €73,500 |
| Other four only | 0.883 / 0.109 / €75,500 | 0.756 / 0.199 / €55,500 |
| All five | **0.941 / 0.065 / €90,500** | **0.931 / 0.084 / €82,000** |

The four features collectively help this forest under both designs. The one-feature forest is **not** the submitted tree: the latter is pruned, and made €86,000 and €83,500 respectively on these splits. Running a complex model on one feature need not reproduce an effective simple threshold.

There is also a direct test of the tree's coarse ranking: among the 211 success–failure pairs in the same ID validation fold with *identical* tree probabilities, the forest ranked the successful store higher in 155, lower in 45 and tied 11. These overlapping pairs describe ranking within tree ties, not 211 independent observations or a profit estimate.

## Does logistic regression corroborate the feature story?

KNIME's full logistic model z-scored each predictor using its training fold. In **all five ID-fold fits**, dentist distance had the largest absolute coefficient and school count the second largest. The modelled logit is **failure**: greater dentist distance was associated with higher failure odds, and higher school count with lower failure odds, conditional on the other variables. One fit warned at the class workflow's 100-epoch cap. Repeating with a 5,000-epoch cap gave no convergence warnings and preserved both rankings and signs (distance +2.28 to +3.78, schools −3.09 to −1.46). Removing dentist distance and retraining logistic reduced ID-fold net from €84,500 to €73,500. Conversely, dentist-only logistic earned €86,500 on that split despite worse Brier (0.099 vs 0.084). Ranking, probability accuracy and the decision at one threshold are different objectives.

Logistic is a cross-check using another model on the **same labels**, not independent data. Its coefficient magnitudes are not RF importance percentages. These results support an association and a useful simpler benchmark; they do not imply that changing dentist access or school count would cause campaign sales.
