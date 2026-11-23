"""Check the T09 Desktop export against the accepted labels, folds and baseline."""
import csv
import math
from pathlib import Path
import sys
import unittest
import xml.etree.ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[2]
RELEASE = ROOT / "outputs"
OUTPUT = Path(sys.argv.pop(1)) if len(sys.argv) > 1 else RELEASE / "held-out.csv"


def rows(path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


class HeldOutExport(unittest.TestCase):
    def test_fold_four_success_probability_at_audited_leaf(self):
        # Independently reconstructed Gini tree, fixed T08 mapping. This leaf
        # contains the stores below both successive dentist-distance splits.
        scores = {r["store_id"]: r for r in rows(OUTPUT)}
        folds = {r["store_id"]: int(r["fold"]) for r in rows(RELEASE / "folds.csv")}
        stores = rows(RELEASE / "store-universe.csv")
        cutoff = 0.370320514  # log1p(distance), midpoint to displayed precision
        leaf = [r for r in stores if math.log1p(float(r["Distance from a Dentist"])) <= cutoff]
        training = [int(r["success"]) for r in leaf if r["store_id"] in folds
                    and folds[r["store_id"]] != 4]
        self.assertIn("15596", {r["store_id"] for r in leaf})
        self.assertEqual(folds["15596"], 4)
        self.assertEqual((sum(training), len(training)), (8, 10))
        self.assertAlmostEqual(float(scores["15596"]["tree_probability"]),
                               sum(training) / len(training), places=6)

    def test_training_medians_can_load_without_defaults(self):
        with ZipFile(ROOT / "workflows/oral-b-italy.knwf") as archive:
            settings = ET.fromstring(archive.read("oral-b-italy/GroupBy (#71)/settings.xml"))
        model = settings.find("./{*}config[@key='model']")
        for field in ("population", "income", "household_size", "hygienists", "dentist_distance"):
            method = model.find(f"./{{*}}config[@key='aggregationOperatorSettings']/"
                                f"{{*}}config[@key='Median_V3.4_{field}']/{{*}}entry[@key='medianMethod']")
            self.assertIsNotNone(method, f"KNIME cannot load the median settings for {field}")
            self.assertEqual(method.get("value"), "Mean of middle values")

    def test_three_scores_per_labeled_store(self):
        self.assertTrue(OUTPUT.is_file(), f"T09 workflow did not write {OUTPUT.name}")
        scores = rows(OUTPUT)
        labels = {r["store_id"]: int(r["success"]) for r in rows(RELEASE / "store-universe.csv")
                  if r["success"] != ""}
        baseline = {r["store_id"]: r for r in rows(RELEASE / "baseline-oof.csv")}
        self.assertEqual(len(scores), 170)
        self.assertEqual({r["store_id"] for r in scores}, labels.keys())
        self.assertEqual(labels.keys(), baseline.keys())
        for r in scores:
            sid = r["store_id"]
            with self.subTest(store=sid):
                self.assertEqual(int(r["success"]), labels[sid])
                self.assertEqual(r["fold"], baseline[sid]["fold"])
                self.assertAlmostEqual(float(r["baseline_probability"]),
                                       float(baseline[sid]["baseline_probability"]), places=12)
                for model in ("logistic", "tree"):
                    p = float(r[f"{model}_probability"])
                    self.assertTrue(math.isfinite(p) and 0 <= p <= 1)


if __name__ == "__main__":
    unittest.main()
