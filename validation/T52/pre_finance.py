"""Compare independent native taps before handing the evidence to the Team 2 reviewer."""
import csv
import hashlib
import io
import math
from collections import Counter
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from check_pair import check_funded, scores, votes
from native_folds import ROOT, reverse_records, rows


def require(ok, message):
    if not ok:
        raise ValueError(message)


def compare_inputs(a, b):
    require(a.resolve() != b.resolve(), "original and reversed workspaces must be distinct")
    archive = ROOT / "workflows/oral-b-italy-final.knwf"
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    for run in (a,b):
        require((run/"candidate.sha256").read_text().strip()==digest, "wrong workflow revision")
    with TemporaryDirectory() as temp:
        for name in ("Activated_Stores.xlsx","Italian_Stores.xlsx"):
            path = Path("oral-b-italy-final/data/inputs")/name
            original = (ROOT/"data"/name).read_bytes()
            require((a/path).read_bytes()==original,f"{name}: original is not the supplied input")
            expected = Path(temp)/name
            expected.write_bytes(original)
            reverse_records(expected)
            with ZipFile(expected) as left, ZipFile(b/path) as right:
                require(sorted(left.namelist()) == sorted(right.namelist()) and
                        all(left.read(f)==right.read(f) for f in left.namelist()),
                        f"{name}: reverse workspace did not receive the reversed records")


def table(columns, records):
    stream = io.StringIO()
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(columns.split())
    writer.writerows(records)
    return stream.getvalue().encode()


def keyed(run, name, column):
    records = rows(run / f"{name}.csv")
    by_id = {r[column]: r for r in records}
    require(len(records) == len(by_id) and "" not in by_id, f"{name}: duplicate/missing ID")
    return by_id


def metrics(model, scope, cases):
    pos = [p for p,y in cases if y]
    neg = [p for p,y in cases if not y]
    tp, fp = sum(p > .6 for p in pos), sum(p > .6 for p in neg)
    auc = sum((p > n) + .5*(p == n) for p in pos for n in neg)/(len(pos)*len(neg))
    bins = [sum(low(p) and p <= hi for p,y in cases)
            for low,hi in ((lambda p:p >= .55,.60), (lambda p:p > .60,.65))]
    return (model,scope,len(cases),tp,fp,1000*tp-1500*fp,
            math.fsum((p-y)**2 for p,y in cases)/len(cases),auc,*bins)


def snapshot(run):
    linked, unseen = (keyed(run, n, "Pdv Code") for n in ("links", "unseen"))
    y = {i:int(r["success"]) for i,r in linked.items()}
    folds = {r["store_id"]:int(r["fold"]) for r in rows(ROOT / "outputs/folds.csv")}
    require(y.keys() == folds.keys() and Counter(y.values()) == {1:108,0:62}, "linked outcomes")
    require(len(unseen) == 310 and not y.keys() & unseen.keys(), "unseen cohort")
    require(Counter(r["match_method"] for r in linked.values()) == {"code":152,"coordinates":18},
            "linkage routes")
    for i,r in linked.items():
        require(r["outcome"] == ("incremental sales" if y[i] else "no incremental sales"), f"label {i}")
        require(r["act_code"] == i if r["match_method"] == "code" else
                not r["act_code"] and (r["act_lat"],r["act_lon"]) == (r["Latitude"],r["Longitude"]),
                f"linkage keys {i}")
    native = {m:scores(run,m) for m in ("forest","refit","tree","logistic")}
    for m, data in native.items():
        if m == "refit":
            require(data.keys() == unseen.keys(), "RF refit IDs")
        else:
            require({i:1+int(r[0]) for i,r in data.items()} == folds, f"{m} held-out IDs/folds")
    tree_new = keyed(run, "tree-refit", "Pdv Code")
    national = keyed(run, "national", "store_id")
    require(tree_new.keys() == unseen.keys() and national.keys() == y.keys() | unseen.keys(), "national IDs")
    rates = {k:sum(y[i] for i in y if folds[i]!=k)/sum(folds[i]!=k for i in y) for k in range(1,6)}
    oof, refit, trees, selections, fold_rows = [], [], [], [], []
    funded, cases = set(), {m:{} for m in ("baseline","tree","logistic","forest")}
    for i in sorted(national):
        source = "held_out_2026" if i in y else "refit_unseen"
        raw = native["forest" if i in y else "refit"][i]
        n = votes(raw[1],raw[2])
        flag = y[i] if i in y else int(n>60)
        record = national[i]
        require((record["score_source"], float(record["p_success"]), int(record["recommend_activate"])) ==
                (source,n/100,flag), f"score/decision mismatch {i}")
        if flag:
            funded.add(i)
        selections.append((i,source,n,flag))
        tree = float(native["tree"][i][1] if i in y else tree_new[i]["P (target=success)"])
        trees.append((i,source,tree,int(tree>.6)))
        if i in y:
            k = folds[i]
            fold_rows.append((i,k))
            for m,p in [("baseline",rates[k]),("tree",tree),("logistic",float(native["logistic"][i][1])),
                        ("forest",n/100)]:
                require(0 <= p <= 1, f"invalid {m} score {i}")
                cases[m][i] = (p,y[i])
                oof.append((i,k,y[i],m,p,raw[1] if m=="forest" else "",n if m=="forest" else "",
                            raw[2] if m=="forest" else ""))
        else:
            refit.append((i,source,raw[1],n,raw[2],n/100))
    check_funded(rows(run/"funded.csv"),funded)
    metric_rows = [metrics(m,k,[v for i,v in case.items() if k=="pooled" or folds[i]==k])
                   for m,case in cases.items() for k in [1,2,3,4,5,"pooled"]]
    return {
        "folds.csv":table("store_id fold",fold_rows),
        "links.csv":table("store_id success match_method",((i,y[i],linked[i]["match_method"]) for i in sorted(y))),
        "oof-scores.csv":table("store_id fold success model p_success raw_success success_votes model_count",oof),
        "rf-refit-votes.csv":table("store_id score_source raw_success success_votes model_count p_success",refit),
        "tree-benchmark.csv":table("store_id score_source tree_p_success tree_funded",trees),
        "model-metrics.csv":table("model fold n funded_successes funded_failures observed_net_eur brier auc n_55_60 n_above60_65",metric_rows),
        "selection.csv":table("store_id score_source success_votes recommend_activate",selections),
    }


if __name__ == "__main__":
    a,b,dest = map(Path,sys.argv[1:])
    compare_inputs(a,b)
    left,right = snapshot(a),snapshot(b)
    for name in left:
        require(left[name] == right[name], f"original/reversed mismatch in {name}")
    dest.mkdir(exist_ok=False)
    for name,data in sorted(left.items()):
        (dest/name).write_bytes(data)
        print(hashlib.sha256(data).hexdigest(),name)
