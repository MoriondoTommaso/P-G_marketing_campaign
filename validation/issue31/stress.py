"""Value the SAME 278-store commitment if every probability was optimistic."""
import csv
from decimal import Decimal as D
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[2]
with (root / "outputs/national-scores.csv").open() as stream:
    selected = [D(r["p_success"]) for r in csv.DictReader(stream)
                if r["recommend_activate"] == "1"]
out = csv.writer(sys.stdout, lineterminator="\n")
out.writerow(["absolute_haircut_pp", "committed_stores", "expected_successes",
              "spend_eur", "conditional_case_net_eur", "still_above_break_even"])
for pp in (0, 10, 20, 30, 40):
    stressed = [max(D(0), p - D(pp)/100) for p in selected]
    spend = len(stressed)*1500
    out.writerow([pp, len(stressed), f"{sum(stressed):.2f}", spend,
                  f"{2500*sum(stressed)-spend:.2f}", sum(p > D(".60") for p in stressed)])
