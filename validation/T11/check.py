"""Reconcile the KNIME national list and local stress scenarios by store ID."""
import csv
from collections import Counter
from decimal import Decimal as D
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(sys.argv.pop(1)) if len(sys.argv) > 1 else ROOT / "outputs"
VALUE, COST, TIE = D(2500), D(1500), D(".60")


def rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class Funding(unittest.TestCase):
    def test_knime_boundary_fixture(self):
        path = (Path(__file__).with_name("funding-check.csv") if OUT.resolve() == ROOT / "outputs"
                else OUT / "funding-check.csv")
        self.assertTrue(path.is_file(), "Missing T11 Desktop boundary evidence")
        cases = rows(path)
        self.assertEqual(len(cases), 15)
        by_case = {(D(r["p_success"]), r["scenario"]): r for r in cases}
        for p in map(D, [".55", ".59", ".60", ".61", ".65"]):
            for s, step in [("lower", D("-.05")), ("base", D(0)), ("upper", D(".05"))]:
                r = by_case[p, s]
                self.assertEqual(D(r["base_net_eur"]), p*VALUE-COST)
                self.assertEqual(int(r["base_recommend_activate"]), int(p > TIE))
                self.assertEqual(D(r["scenario_p_success"]), p+step)
                self.assertEqual(D(r["expected_net_eur"]), (p+step)*VALUE-COST)
                self.assertEqual(int(r["recommend_activate"]), int(p+step > TIE))

    def test_national_and_stress_decisions(self):
        self.assertTrue((OUT / "national-scores.csv").is_file(), "Missing T11 national-scores.csv")
        scores = rows(OUT / "national-scores.csv")
        universe = {r["store_id"]: r for r in rows(OUT / "store-universe.csv")}
        historical = {r["store_id"]: D(r["tree_probability"]) for r in rows(OUT / "held-out.csv")}
        for name in ("store-universe.csv", "held-out.csv"):
            self.assertEqual((OUT/name).read_bytes(), (ROOT/"outputs"/name).read_bytes())
        self.assertEqual(len(scores), 480)
        self.assertEqual([r["store_id"] for r in scores], sorted(universe))
        self.assertEqual(set(historical), {i for i, r in universe.items() if r["success"] != ""})
        self.assertEqual(Counter(r["score_source"] for r in scores), {"held_out_2026": 170, "refit_unseen": 310})
        selected = []
        by_id = {r["store_id"]: r for r in scores}
        for r in scores:
            i = r["store_id"]
            p = D(r["p_success"])
            self.assertTrue(p.is_finite() and 0 <= p <= 1)
            self.assertEqual(r["score_source"], "held_out_2026" if i in historical else "refit_unseen")
            if i in historical:
                self.assertEqual(p, historical[i])
            self.assertLess(abs(D(r["expected_net_eur"]) - (VALUE*p-COST)), D("1e-10"))
            self.assertEqual(int(r["recommend_activate"]), int(p > TIE))
            if p > TIE:
                selected.append(r)
        self.assertEqual(rows(OUT / "activation-list.csv"), selected)
        stress = rows(OUT / "sensitivity.csv")
        shifts = {"lower": D("-.05"), "base": D(0), "upper": D(".05")}
        self.assertEqual(len(stress), 1440)
        self.assertEqual({(r["scenario"],r["store_id"]) for r in stress},
                         {(s,i) for s in shifts for i in universe})
        self.assertEqual(Counter(r["scenario"] for r in stress), {s:480 for s in shifts})
        for r in stress:
            base = by_id[r["store_id"]]
            p = D(base["p_success"])
            in_band = D(".55") <= p <= D(".65")
            q = min(D(1), max(D(0), p + shifts[r["scenario"]])) if in_band else p
            before, after = p > TIE, q > TIE
            self.assertEqual(D(r["scenario_p_success"]), q)
            self.assertEqual(D(r["p_success"]), p)
            self.assertEqual(int(r["base_recommend_activate"]), int(before))
            self.assertEqual(r["score_source"], base["score_source"])
            self.assertEqual(int(r["recommend_activate"]), int(after))
            self.assertLess(abs(D(r["expected_net_eur"]) - (VALUE*q-COST)), D("1e-10"))
            self.assertEqual(r["change"], ("retained" if before else "added") if after
                             else ("dropped" if before else "not_selected"))
        base_ids = {r["store_id"] for r in selected}
        all_sets = []
        print("scenario | score source | funded stores | spend EUR | forecast net EUR")
        for scenario in shifts:
            ss = [r for r in stress if r["scenario"] == scenario]
            funded = {r["store_id"] for r in ss if int(r["recommend_activate"])}
            self.assertEqual(funded-base_ids, {r["store_id"] for r in ss if r["change"]=="added"})
            self.assertEqual(base_ids-funded, {r["store_id"] for r in ss if r["change"]=="dropped"})
            for source in ("held_out_2026", "refit_unseen", "pooled"):
                active = [r for r in ss if r["store_id"] in funded and source in ("pooled",r["score_source"])]
                net = sum((D(r["expected_net_eur"]) for r in active), D(0))
                self.assertEqual(net, VALUE*sum((D(r["scenario_p_success"]) for r in active), D(0))
                                 - COST*len(active))
                print(scenario, source, len(active), COST*len(active), f"{net:.2f}", sep=" | ")
            all_sets.append(funded)
        print("Always funded:", len(set.intersection(*all_sets)),
              "| Marginal decisions:", len(set.union(*all_sets)-set.intersection(*all_sets)))


if __name__ == "__main__":
    unittest.main()
