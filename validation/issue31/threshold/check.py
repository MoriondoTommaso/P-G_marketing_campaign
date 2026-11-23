"""Compare native validation, production and stress CSVs to exact decimal economics."""
import csv
from decimal import Decimal as D
from pathlib import Path
import sys

P = dict(eleven_twentieths=D(".55"), six_tenths=D(".6"), thirteen_twentieths=D(".65"),
         below=D(".5999999"), above=D(".6000001"), decimal_tie=D(".6"))
SHIFT = dict(lower=D("-.05"),base=D(0),upper=D(".05"))


def check(directory):
    errors = []
    for name in ("validation","base","stress"):
        with (directory / (name + ".csv")).open(newline="") as stream:
            rows = list(csv.DictReader(stream))
        if sorted((r["case"],r["scenario"]) for r in rows) != sorted((c,s) for c in P for s in SHIFT):
            raise ValueError(f"{name}: missing, duplicate or unexpected test rows")
        for r in rows:
            case, scenario = r["case"],r["scenario"]
            p=P[case]
            q=p+SHIFT[scenario] if name=="stress" else p
            net=q*2500-1500
            if case=="six_tenths" and float(r["raw_probability"]) != 0.6000000238418579:
                raise ValueError("Native 6/10 input lost precision")
            expected = ({"probability":p, "funded":int(net>0), "realized_net_eur":1000*int(net>0),
                         "near_n":1, "low_n":int(p<=D(".6")), "high_n":int(p>D(".6"))}
                        if name=="validation" else {"p_success":p,"expected_net_eur":net,"recommend_activate":int(net>0)})
            if name=="stress":
                expected["scenario_p_success"]=q
            for k,v in expected.items():
                # #336 uses binary64 multiplication. Permit representation error
                # for non-zero net amounts; ties still require *exactly* zero.
                tol = D("1e-12") if (name,k)==("base","expected_net_eur") and v else 0
                if abs(D(r[k]) - v) > tol:
                    errors.append(f"{name} {case}/{scenario} {k}: expected {v}, got {r[k]}")
    if errors:
        raise SystemExit("\n".join(errors))
    print("PASS: 54 native rows; validation bins, funding, base and shifted net values agree.")


if __name__ == "__main__":
    check(Path(sys.argv[1]))
