"""Independently reconcile KNIME decision rows and their published summaries."""
import csv
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(sys.argv.pop(1)) if len(sys.argv) > 1 else ROOT / "outputs"
MODELS = ("baseline", "logistic", "tree")


def rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def supported_partition(test, train):
    """Each tuple is (successes, failures), not (successes, total)."""
    return sum(test) >= 20 and min(test) >= 5 and sum(train) >= 40 and min(train) >= 10


class Decisions(unittest.TestCase):
    def test_holdout_must_have_a_supported_training_complement(self):
        self.assertFalse(supported_partition((62, 57), (46, 5)))
        self.assertFalse(supported_partition((34, 4), (74, 58)))
        self.assertFalse(supported_partition((5, 5), (30, 10)))
        self.assertFalse(supported_partition((15, 5), (10, 10)))
        self.assertTrue(supported_partition((15, 5), (30, 10)))

    def test_decisions_and_comparisons(self):
        self.assertTrue((OUT / "held-out-decisions.csv").is_file(), "Missing T10 decision export")
        scores = {r["store_id"]: r for r in rows(OUT / "held-out.csv")}
        self.assertEqual(scores, {r["store_id"]: r for r in rows(ROOT / "outputs/held-out.csv")})
        decisions = rows(OUT / "held-out-decisions.csv")
        self.assertEqual(len(decisions), 510)
        self.assertEqual({(r["store_id"], r["model"]) for r in decisions},
                         {(sid, m) for sid in scores for m in MODELS})
        for r in decisions:
            sid, model = r["store_id"], r["model"]
            src = scores[sid]
            self.assertEqual((r["fold"], r["success"]), (src["fold"], src["success"]))
            p, y = float(r["probability"]), int(r["success"])
            self.assertEqual(p, float(src[model + "_probability"]))
            self.assertEqual(int(r["funded"]), int(p > .60))
            self.assertEqual(int(r["realized_net_eur"]), (2500*y-1500) if p > .60 else 0)

        table = rows(OUT / "model-comparison.csv")
        self.assertEqual(len(table), 27)  # (5 folds + pooled + 2 bands + pooled) × 3 paths
        self.check_summary(table, "ordinary", decisions, ("1","2","3","4","5","pooled"))
        self.check_spatial(table, scores)

    def check_spatial(self, table, scores):
        # QA taps the spatial decision port; this is never a national or ordinary export.
        audit = OUT / "spatial-decisions.csv"
        if OUT.resolve() == ROOT / "outputs" and not audit.is_file():
            audit = Path(__file__).with_name("spatial-decisions.csv")
        self.assertTrue(audit.is_file(), "Missing spatial decision audit")
        spatial = rows(audit)
        self.assertEqual(len(spatial), 510)
        self.assertEqual({(r["store_id"],r["model"]) for r in spatial},
                         {(sid,m) for sid in scores for m in MODELS})
        u=rows(OUT / "store-universe.csv")
        self.assertEqual(sorted(u, key=lambda r:r["store_id"]),
                         sorted(rows(ROOT / "outputs/store-universe.csv"), key=lambda r:r["store_id"]))
        for boundaries in ((41.5,44.5), (43.0,)):
            band_by_id = {r["store_id"]:sum(float(r["Latitude"]) >= cut for cut in boundaries)
                          for r in u if r["store_id"] in scores}
            def counts(ids):
                labels = [int(scores[s]["success"]) for s in ids]
                return sum(labels), len(labels)-sum(labels)
            failed = []
            for k in range(len(boundaries)+1):
                test = {s for s,b in band_by_id.items() if b == k}
                if not supported_partition(counts(test), counts(scores.keys()-test)):
                    failed.append(k)
            self.assertEqual(failed, [0, 2] if len(boundaries)==2 else [1])
        group={x["store_id"]:"south" if float(x["Latitude"])<43 else "north" for x in u}
        for band,n,success in [("south",51,46),("north",119,62)]:
            ids=[s for s in scores if group[s]==band]
            self.assertEqual((len(ids),sum(int(scores[s]["success"]) for s in ids)),(n,success))
        for r in spatial:
            band = {"6":"south","7":"north"}[r["fold"]]
            self.assertEqual(band,group[r["store_id"]])
            r["fold"]=band
            self.assertEqual(r["success"],scores[r["store_id"]]["success"])
            p=float(r["probability"])
            self.assertTrue(0<=p<=1)
            if r["model"]=="baseline":
                self.assertAlmostEqual(p,62/119 if band=="south" else 46/51)
            self.assertEqual(int(r["funded"]),int(p>.60))
            self.assertEqual(int(r["realized_net_eur"]),int(p>.60)*(2500*int(r["success"])-1500))
        self.check_summary(table,"spatial_exploratory",spatial,("south","north","pooled"))

    def check_summary(self, table, design, decisions, folds):
        summary={(r["fold"],r["model"]):r for r in table if r["validation"]==design}
        self.assertEqual(set(summary),{(f,m) for f in folds for m in MODELS})
        for fold in folds:
            for model in MODELS:
                r = summary[fold, model]
                ds = [x for x in decisions if x["model"]==model and (fold=="pooled" or x["fold"]==fold)]
                n = len(ds)
                hits = sum(int(x["funded"])*int(x["success"]) for x in ds)
                funded = sum(int(x["funded"]) for x in ds)
                net = 2500*hits-1500*funded
                all_net = sum(2500*int(x["success"])-1500 for x in ds)
                baseline_net = sum(int(x["realized_net_eur"]) for x in decisions
                                   if x["model"] == "baseline" and (fold == "pooled" or x["fold"] == fold))
                for key,expected in {"test_n":n,"funded":funded,"funded_success":hits,
                                     "funded_failure":funded-hits,"sales_eur":2500*hits,"spend_eur":1500*funded,
                                     "net_eur":net,"all_net_eur":all_net,"none_net_eur":0,
                                     "baseline_net_eur":baseline_net, "delta_all":net-all_net,
                                     "delta_none":net,"delta_baseline":net-baseline_net}.items():
                    self.assertEqual(int(r[key]),expected,(fold,model,key))
                brier=sum((float(x["probability"])-int(x["success"]))**2 for x in ds)/n
                self.assertTrue(math.isclose(float(r["brier"]),brier,abs_tol=1e-12))
                for band,lo,hi in [("near",.55,.65),("low",.55,.60),("high",.60,.65)]:
                    part=[x for x in ds if (lo<float(x["probability"]) if band=="high" else lo<=float(x["probability"])) and float(x["probability"])<=hi]
                    self.assertEqual(int(r[band+"_n"]),len(part))
                    self.assertEqual(int(r[band+"_success"]),sum(int(x["success"]) for x in part))
                    self.assertEqual(r[band+"_status"],"empty" if not part else "sparse" if len(part)<10 else "observed")
                    for suffix,values in [("pred",[float(x["probability"]) for x in part]),("obs",[int(x["success"]) for x in part]),("gap",[int(x["success"])-float(x["probability"]) for x in part])]:
                        if part:self.assertAlmostEqual(float(r[band+"_"+suffix]),sum(values)/len(part))
                        else:self.assertEqual(r[band+"_"+suffix],"")
        self.assertEqual(int(summary["pooled","baseline"]["all_net_eur"]),15000)


if __name__=="__main__":
    unittest.main()
