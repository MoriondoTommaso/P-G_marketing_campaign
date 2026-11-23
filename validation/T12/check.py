"""Independently reconstruct the five financial policies from store-level rows."""
import csv
from decimal import Decimal as D
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(sys.argv.pop(1)) if len(sys.argv) > 1 else ROOT / "outputs"


def rows(name):
    with (OUT / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class Finance(unittest.TestCase):
    def test_release_summary(self):
        self.assertTrue((OUT / "financial-summary.csv").is_file(), "Missing T12 financial-summary.csv")
        national = rows("national-scores.csv")
        held_out = {r["store_id"]: D(r["tree_probability"]) for r in rows("held-out.csv")}
        self.assertEqual(len({r["store_id"] for r in national}), 480)
        ranked = sorted(national, key=lambda r: (-D(r["p_success"]), r["store_id"]))
        funded = [r for r in ranked if D(r["p_success"]) > D(".60")]
        repeat = [r for r in ranked if r["store_id"] in held_out]
        self.assertEqual({r["store_id"] for r in rows("activation-list.csv")}, {r["store_id"] for r in funded})
        self.assertEqual(len(repeat), 170)
        self.assertTrue(all(D(r["p_success"]) == held_out[r["store_id"]] for r in repeat))
        n, h = len(funded), len(repeat)
        k = min(n, h)
        matched = abs(n-h) >= 17 or n < h
        def forecast(stores):
            sales = 2500 * sum((D(r["p_success"]) for r in stores), D(0))
            spend = 1500 * len(stores)
            return len(stores), sales, spend, sales-spend
        actual, = rows("baseline-2026.csv")
        history = tuple(D(actual[c]) for c in ("activated","sales_eur","spend_eur","net_eur"))
        self.assertEqual(history, (170,270000,255000,15000))
        expected = {"actual_2026": history, "optimized_forecast": forecast(funded),
                    "repeat_forecast": forecast(repeat)}
        if matched:
            expected.update(matched_optimized=forecast(funded[:k]), matched_repeat=forecast(repeat[:k]))
        report = rows("financial-summary.csv")
        self.assertCountEqual([r["policy"] for r in report], expected.keys())
        for r in report:
            policy = r["policy"]
            self.assertEqual(int(r["store_count"]), expected[policy][0])
            for field, amount in zip(("sales_eur","spend_eur","net_eur"), expected[policy][1:]):
                self.assertLess(abs(D(r[field])-amount), D("0.00001"), (policy, field))
            deltas = {
                "vs_2026_actual_eur": expected[policy][-1]-history[-1] if policy=="optimized_forecast" else None,
                "vs_repeat_forecast_eur": expected[policy][-1]-expected["repeat_forecast"][-1] if policy=="optimized_forecast" else None,
                "matched_net_difference_eur": expected[policy][-1]-expected["matched_repeat"][-1] if policy=="matched_optimized" and k else None,
            }
            for field, amount in deltas.items():
                if amount is None:
                    self.assertEqual(r[field], "", (policy, field))
                else:
                    self.assertLess(abs(D(r[field])-amount), D("0.00001"), field)
        print(f"Verified {n} optimized, {h} repeat, 2026 actual; matched comparison: {matched}, k={k}.")


if __name__ == "__main__":
    unittest.main()
