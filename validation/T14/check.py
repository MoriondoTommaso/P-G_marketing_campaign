"""Trace T14 shopper actions to T07 profile counts and T11 selected-store coverage.

Recomputes every coverage figure in docs/shopper-actions.md from the store-level
exports, re-derives the quoted T07 tercile citations from outputs/store-profiles.csv,
and enforces the wording rules: hypothesis-labelled needs, neutral copy, no
unconfirmed persona or SKU claims.
"""
import csv
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(sys.argv.pop(1)) if len(sys.argv) > 1 else ROOT / "outputs"
DOC = ROOT / "docs" / "shopper-actions.md"

# Neutral T03 message copy that must appear verbatim in the actions table.
MESSAGES = [
    "Find the Oral-B toothpaste that fits your routine.",
    "Compare Oral-B toothpaste options.",
    "Time to restock toothpaste?",
]
ACTION_COLUMNS = ["Shopper situation", "Supporting store profile", "Consumer need",
                  "Message", "In-store placement", "Measure"]
COVERAGE_LABELS = [
    "Funded stores, total",
    "Latitude band North (>= 44.5)",
    "Latitude band Centre (41.5 - 44.5)",
    "Latitude band South / islands (< 41.5)",
    "Dentist distance <= 25 (source units)",
    "Dentist distance 25 - 100 (T07 gap range)",
    "Dentist distance > 100",
    "Nr of Schools = 0",
    "Nr of Schools >= 1",
    "Held-out 2026 stores funded (successes + failures)",
    "Held-out 2026 successes funded",
    "Held-out 2026 failures funded",
    "Refit-unseen stores funded",
]
TERCILE_CITES = [
    ("Distance from a Dentist", "(-inf, 6.64]"),
    ("Distance from a Dentist", "(6.64, 107.006]"),
    ("Distance from a Dentist", "(107.006, inf]"),
    ("Nr of Schools", "(-inf, 2.0]"),
    ("Nr of Schools", "(5.0, inf]"),
]


def rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def coverage(activation, universe):
    """Recompute the funded-list coverage figures the document must quote."""
    funded = {r["store_id"]: r for r in activation}
    uni = {r["store_id"]: r for r in universe}
    assert set(funded) <= set(uni)

    def lat(i):
        return float(uni[i]["Latitude"])

    def dentist(i):
        return float(uni[i]["Distance from a Dentist"])

    def band(i):
        return ("North" if lat(i) >= 44.5
                else "Centre" if lat(i) >= 41.5 else "South")

    def schools(i):
        return int(float(uni[i]["Nr of Schools"]))

    hist = [i for i in funded if funded[i]["score_source"] == "held_out_2026"]
    hist_success = [i for i in hist if uni[i]["success"] == "1"]
    hist_failure = [i for i in hist if uni[i]["success"] == "0"]
    assert len(hist_success) + len(hist_failure) == len(hist), "Unknown outcome on the funded list"
    return {
        "Funded stores, total": len(funded),
        "Latitude band North (>= 44.5)": sum(band(i) == "North" for i in funded),
        "Latitude band Centre (41.5 - 44.5)": sum(band(i) == "Centre" for i in funded),
        "Latitude band South / islands (< 41.5)": sum(band(i) == "South" for i in funded),
        "Dentist distance <= 25 (source units)": sum(dentist(i) <= 25 for i in funded),
        "Dentist distance 25 - 100 (T07 gap range)": sum(25 < dentist(i) <= 100 for i in funded),
        "Dentist distance > 100": sum(dentist(i) > 100 for i in funded),
        "Nr of Schools = 0": sum(schools(i) == 0 for i in funded),
        "Nr of Schools >= 1": sum(schools(i) >= 1 for i in funded),
        "Held-out 2026 stores funded (successes + failures)": len(hist),
        "Held-out 2026 successes funded": len(hist_success),
        "Held-out 2026 failures funded": len(hist_failure),
        "Refit-unseen stores funded": len(funded) - len(hist),
    }


def tercile_citations(profile_rows):
    """Build the 'successes / n = pct%' strings the document quotes from T07."""
    terciles = {(r["trait"], r["group"]): r for r in profile_rows
                if r["comparison"] == "trait_tercile"}
    out = {}
    for trait, group in TERCILE_CITES:
        r = terciles[(trait, group)]
        n, s = int(r["n"]), int(r["n_success"])
        out[(trait, group)] = f"{s} / {n} = {round(100 * s / n)}%"
    return out


class ShopperActions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = DOC.read_text(encoding="utf-8") if DOC.is_file() else None
        cls.activation = rows(OUT / "activation-list.csv")
        cls.universe = rows(OUT / "store-universe.csv")
        if OUT.resolve() != (ROOT / "outputs").resolve():
            for name in ("activation-list.csv", "store-universe.csv"):
                self_file = OUT / name
                repo_file = ROOT / "outputs" / name
                assert self_file.read_bytes() == repo_file.read_bytes(), \
                    f"{name} differs from the repository export"
        cls.coverage = coverage(cls.activation, cls.universe)
        cls.terciles = tercile_citations(rows(ROOT / "outputs" / "store-profiles.csv"))
        summary = {r["policy"]: r for r in rows(OUT / "financial-summary.csv")}
        opt = summary["optimized_forecast"]
        cls.spend = f"€{float(opt['spend_eur']):,.0f}"
        cls.net = f"€{float(opt['net_eur']):,.2f}"

    def test_document_exists(self):
        self.assertIsNotNone(self.doc, f"Missing {DOC}")

    def test_coverage_table_matches_funded_list(self):
        for label in COVERAGE_LABELS:
            expected = self.coverage[label]
            pattern = re.escape(label) + r"\s*\|\s*(\d+)\s*\|"
            m = self.doc and re.search(pattern, self.doc)
            self.assertTrue(m, f"Coverage row '{label}' not found in the document")
            self.assertEqual(int(m.group(1)), expected,
                             f"'{label}': document says {m.group(1)}, data says {expected}")
        # Band, dentist, school and score-source bins must partition the list.
        total = self.coverage["Funded stores, total"]
        self.assertEqual(sum(self.coverage[l] for l in COVERAGE_LABELS[1:4]), total)
        self.assertEqual(sum(self.coverage[l] for l in COVERAGE_LABELS[4:7]), total)
        self.assertEqual(sum(self.coverage[l] for l in COVERAGE_LABELS[7:9]), total)
        self.assertEqual(self.coverage[COVERAGE_LABELS[12]], total - self.coverage[COVERAGE_LABELS[9]])
        self.assertEqual(self.coverage[COVERAGE_LABELS[10]] + self.coverage[COVERAGE_LABELS[11]],
                         self.coverage[COVERAGE_LABELS[9]])

    def test_tercile_citations_match_store_profiles(self):
        for (trait, group), cite in self.terciles.items():
            self.assertIn(cite, self.doc,
                          f"T07 citation '{cite}' ({trait}, {group}) missing or wrong")

    def test_financial_figures_match_t12_summary(self):
        self.assertIn(self.spend, self.doc,
                      f"Funded-list spend {self.spend} not quoted correctly")
        self.assertIn(self.net, self.doc,
                      f"Funded-list forecast net {self.net} not quoted correctly")

    def test_action_table_structure(self):
        table_lines = [ln for ln in self.doc.splitlines() if ln.startswith("|")]
        header_idx = [i for i, ln in enumerate(table_lines)
                      if all(c in ln for c in ACTION_COLUMNS)]
        self.assertTrue(header_idx, "Actions table with the six required columns not found")
        body = table_lines[header_idx[0] + 2:]  # skip header and separator row
        data = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in body]
        self.assertGreaterEqual(len(data), 3, "Fewer than three shopper actions")
        need_col = ACTION_COLUMNS.index("Consumer need")
        msg_col = ACTION_COLUMNS.index("Message")
        prof_col = ACTION_COLUMNS.index("Supporting store profile")
        for row_no, row in enumerate(data):
            self.assertGreaterEqual(len(row), len(ACTION_COLUMNS),
                                    f"Action {row_no + 1} is missing columns")
            self.assertIn("ypothesis", row[need_col],
                          f"Action {row_no + 1}: consumer need is not labelled as a hypothesis")
            self.assertIn("T07", row[prof_col],
                          f"Action {row_no + 1}: store profile is not traced to T07")
        for row_no, message in enumerate(MESSAGES):
            self.assertIn(message, data[row_no][msg_col],
                          f"Action {row_no + 1}: neutral T03 message not used verbatim")

    def test_wording_rules(self):
        # Class personas were never supplied; the document must say so.
        self.assertIn("not identified in the supplied files", self.doc)
        # Bounded-test framing with randomisation where feasible (T03 handoff).
        self.assertIn("bounded", self.doc.lower())
        self.assertTrue(re.search(r"randomi[sz]", self.doc, re.I),
                        "Randomised comparison not addressed")
        # Any whitening mention must stay conditional on SKU/claim confirmation.
        for line in self.doc.splitlines():
            if "hitening" in line:
                self.assertIn("confirm", line.lower(),
                              "Whitening wording used without its confirmation caveat")
        # Every action's need is a hypothesis; the doc must not present
        # individual shopper preferences as observed.
        self.assertNotIn("shopper prefers", self.doc.lower())
        # Inputs must be cited for the peer trace.
        for source in ("shopper-evidence.md", "store-insights.md",
                       "store-profiles.csv", "activation-list.csv", "pilot.md"):
            self.assertIn(source, self.doc, f"Source {source} is not cited")


if __name__ == "__main__":
    print("T14 shopper-actions trace:",
          f"{len(rows(OUT / 'activation-list.csv'))} funded stores")
    unittest.main()
