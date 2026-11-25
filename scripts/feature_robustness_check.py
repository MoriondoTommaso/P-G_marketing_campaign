"""Feature-set robustness check for the final KNIME workflow (25 Nov 2026).

Question: does the model's result depend on which 5 store traits we chose?
Method: same model family, 3 different feature sets, 20 repetitions of
stratified 5-fold cross-validation on the 170 labelled stores.
Decision rule: fund a store only if p > 0.60 (break-even, EUR 1,500 / EUR 2,500).
Net per store: +1,000 funded success, -1,500 funded failure, 0 not funded.

This is a scikit-learn approximation of the KNIME nodes, so absolute euros
differ slightly from KNIME (tree: EUR 88,000). Use it only to compare the three
feature sets with each other.

Run from the repo root:  python3 scripts/feature_robustness_check.py
Needs: pandas, scikit-learn.
"""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

u = pd.read_csv("outputs/store-universe.csv")
labelled = u[u["success"].notna()]
y = labelled["success"].astype(int).values

FINAL_5 = ["Water hardness IDX", "Nr of Schools", "Distance from a Dentist",
           "Total Population", "Avg Income per Household"]
PROTOCOL_5 = ["Total Population", "Avg Income per Household",
              "Households avg components", "Nr of Hygienists",
              "Distance from a Dentist"]
# Every store trait except the ID, the coordinates and Online Consumption IYA
# (IYA may be measured after the 2026 campaign: possible leakage).
EXCLUDED = {"store_id", "Latitude", "Longitude", "success", "target",
            "Online Consumption IYA"}
ALL_32 = [c for c in u.columns if c not in EXCLUDED]

FEATURE_SETS = {"final_5": FINAL_5, "all_32": ALL_32, "protocol_5": PROTOCOL_5}
MODELS = {
    "tree": lambda: DecisionTreeClassifier(min_samples_leaf=10, random_state=0),
    "forest": lambda: RandomForestClassifier(n_estimators=300, random_state=0),
    "logistic": lambda: make_pipeline(StandardScaler(),
                                      LogisticRegression(max_iter=3000)),
}


def net_eur(p):
    funded = p > 0.60
    return int((funded & (y == 1)).sum() * 1000 - (funded & (y == 0)).sum() * 1500)


rows = []
for seed in range(20):
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    for fs_name, cols in FEATURE_SETS.items():
        X = labelled[cols].values
        for m_name, make in MODELS.items():
            p = cross_val_predict(make(), X, y, cv=cv, method="predict_proba")[:, 1]
            rows.append((m_name, fs_name, roc_auc_score(y, p), net_eur(p)))

res = pd.DataFrame(rows, columns=["model", "features", "auc", "net_eur"])
summary = res.groupby(["model", "features"])[["auc", "net_eur"]].mean().round(3)
print(f"{len(ALL_32)} allowed traits")
print(summary)

tree = DecisionTreeClassifier(min_samples_leaf=10, random_state=0)
tree.fit(labelled[ALL_32].values, y)
imp = pd.Series(tree.feature_importances_, index=ALL_32)
print("\nTree trained on all allowed traits, share of its splits:")
print(imp[imp > 0].sort_values(ascending=False).round(3))
