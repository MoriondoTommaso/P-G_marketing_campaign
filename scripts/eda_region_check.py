"""EDA checks behind docs/final-workflow.md (section "EDA findings").

Reproduces, from outputs/store-universe.csv:
1. success vs failure medians of the traits in the KNIME EDA branch (GroupBy #39);
2. success rate by region, with the same latitude rule as Rule Engine #40
   (North >= 44.5, Centre >= 41.5, South below);
3. the dentist-distance medians inside each region, to check that the dentist
   effect is not only a North/South effect.

Run from the repo root:  python3 scripts/eda_region_check.py   (needs pandas)
"""
import pandas as pd

u = pd.read_csv("outputs/store-universe.csv")
u["region"] = pd.cut(u["Latitude"], [-90, 41.5, 44.5, 90], right=False,
                     labels=["South", "Centre", "North"])
lab = u[u["success"].notna()]

traits = ["Distance from a Dentist", "Water hardness IDX", "Nr of Schools",
          "Avg Income per Household", "Total Population"]
print("1. Medians, success vs failure (170 stores)")
print(lab.groupby("target")[traits].median().round(1).T, "\n")

print("2. Success rate by region (activated stores) and never-activated stores")
rate = lab.groupby("region", observed=True)["success"].agg(["sum", "count", "mean"])
rate["never_activated"] = u[u["success"].isna()].groupby("region", observed=True).size()
print(rate.rename(columns={"sum": "successes", "count": "activated",
                           "mean": "rate"}).round(3), "\n")

print("3. Distance from a Dentist, median by region and outcome")
print(lab.groupby(["region", "target"], observed=True)["Distance from a Dentist"]
      .agg(["median", "count"]).round(1))
