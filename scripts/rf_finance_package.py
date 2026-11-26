"""Finance package for the Random Forest release (issue #51).

Reads only the store-level release files written by the final KNIME workflow
(outputs/national-scores-class.csv) and the 2026 baseline
(outputs/baseline-2026.csv), and writes:

  outputs/financial-summary-class.csv  - plan vs 2026 actual vs repeat-170,
                                          equal-spend (matched-count) comparison,
                                          cohort subtotals and stress totals
  outputs/sensitivity-class.csv        - per-store base / lower / upper scenarios

Rules (docs/evaluation.md): expected net = 2500 * p - 1500; fund only if p > 0.60
(forest: more than 60 of 100 votes); stress band = original p in [0.55, 0.65],
shifted by -0.05 / +0.05 with decimal arithmetic; equal spend uses k = min(N, 170),
ranking by descending p with ascending text store_id for ties.

Run from the repository root:  python3 scripts/rf_finance_package.py
"""
import csv
from decimal import Decimal

SALES, COST = Decimal(2500), Decimal(1500)
THRESHOLD, BAND_LO, BAND_HI, SHIFT = Decimal("0.60"), Decimal("0.55"), Decimal("0.65"), Decimal("0.05")


def read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def net(p):
    return SALES * p - COST


def totals(rows):
    n = len(rows)
    sales = sum((SALES * r["p"] for r in rows), Decimal(0))
    spend = COST * n
    return n, sales, spend, sales - spend


def ranked(rows):
    return sorted(rows, key=lambda r: (-r["p"], r["store_id"]))


def main():
    stores = read("outputs/national-scores-class.csv")
    for r in stores:
        r["p"] = Decimal(r["p_success"])
        votes = r["p"] * 100
        assert votes == votes.to_integral_value(), f"not a vote share: {r['store_id']} {r['p_success']}"
        assert int(r["recommend_activate"]) == int(r["p"] > THRESHOLD), f"funding flag mismatch: {r['store_id']}"
    assert len(stores) == 480 and len({r["store_id"] for r in stores}) == 480

    base = read("outputs/baseline-2026.csv")[0]
    actual = (int(base["activated"]), Decimal(base["sales_eur"]), Decimal(base["spend_eur"]), Decimal(base["net_eur"]))

    repeat = [r for r in stores if r["score_source"] == "held_out_2026"]
    optimized = [r for r in stores if r["recommend_activate"] == "1"]
    assert len(repeat) == 170

    rep_t, opt_t = totals(repeat), totals(optimized)
    k = min(len(optimized), 170)
    m_opt, m_rep = totals(ranked(optimized)[:k]), totals(ranked(repeat)[:k])

    rows = [
        ("actual_2026", actual, "", "", ""),
        ("matched_optimized", m_opt, "", "", m_opt[3] - m_rep[3]),
        ("matched_repeat", m_rep, "", "", ""),
        ("optimized_forecast", opt_t, opt_t[3] - actual[3], opt_t[3] - rep_t[3], ""),
        ("repeat_forecast", rep_t, "", "", ""),
    ]
    for src in ("held_out_2026", "refit_unseen"):
        rows.append((f"optimized_forecast_{src}", totals([r for r in optimized if r["score_source"] == src]), "", "", ""))

    # stress scenarios
    sens, scen_rows = [], {}
    for name, shift in (("base", Decimal(0)), ("lower", -SHIFT), ("upper", SHIFT)):
        chosen = []
        for r in sorted(stores, key=lambda r: r["store_id"]):
            in_band = BAND_LO <= r["p"] <= BAND_HI
            p = r["p"] + shift if in_band else r["p"]
            p = min(max(p, Decimal(0)), Decimal(1))
            flag = int(p > THRESHOLD)
            was = int(r["recommend_activate"])
            change = {(1, 1): "retained", (0, 0): "not_selected", (1, 0): "dropped", (0, 1): "added"}[(was, flag)]
            sens.append([r["store_id"], r["p_success"], r["score_source"], f"{net(r['p']):.2f}", was,
                         name, str(p), f"{net(p):.2f}", flag, change])
            if flag:
                chosen.append({**r, "p": p})
        scen_rows[name] = totals(chosen)
    for name in ("lower", "upper"):
        rows.append((f"stress_{name}", scen_rows[name], "", "", ""))
    assert scen_rows["base"] == opt_t

    with open("outputs/financial-summary-class.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["policy", "store_count", "sales_eur", "spend_eur", "net_eur",
                    "vs_2026_actual_eur", "vs_repeat_forecast_eur", "matched_net_difference_eur"])
        for name, (n, sales, spend, nt), a, b, c in rows:
            w.writerow([name, n, sales, spend, nt, a, b, c])

    with open("outputs/sensitivity-class.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["store_id", "p_success", "score_source", "base_net_eur", "base_recommend_activate",
                    "scenario", "scenario_p_success", "expected_net_eur", "recommend_activate", "change"])
        w.writerows(sens)

    print(f"optimized: {opt_t[0]} stores, spend {opt_t[2]}, net {opt_t[3]}")
    print(f"vs 2026 actual: {opt_t[3] - actual[3]}; vs repeat-170 forecast: {opt_t[3] - rep_t[3]}")
    print(f"equal spend (k={k}): optimized {m_opt[3]} vs repeat {m_rep[3]} -> {m_opt[3] - m_rep[3]}")
    for name in ("lower", "upper"):
        n, _, spend, nt = scen_rows[name]
        changed = [s[0] for s in sens if s[5] == name and s[9] in ("added", "dropped")]
        print(f"stress {name}: {n} stores, spend {spend}, net {nt}, changed IDs {changed}")


if __name__ == "__main__":
    main()
