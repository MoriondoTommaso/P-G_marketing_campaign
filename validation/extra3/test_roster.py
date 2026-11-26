"""Check the figures a reader actually receives in the PDF (requires Poppler)."""
from pathlib import Path
import csv
import re
import statistics
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "docs/influencer-roster.pdf"


class RosterEvidence(unittest.TestCase):
    def test_reported_trend_reconciles_to_dated_post_tally(self):
        path = Path(__file__).with_name("instagram-posts-2026-11-26.csv")
        with path.open(encoding="utf-8") as source:
            rows = list(csv.DictReader(source))
        self.assertEqual(len(rows), len({r["post_url"] for r in rows}))
        eligible = [r for r in rows if r["location"] == "Italy"]
        self.assertEqual(len({r["handle"] for r in eligible}), 19)
        hits = [r for r in eligible if r["routine_in_caption"] == "1"]
        text = subprocess.check_output(["pdftotext", PDF, "-"], text=True)
        self.assertIn(f"{len(hits)} of {len(eligible)} captions", " ".join(text.split()))

    def test_instagram_shortlist_matches_public_snapshot(self):
        # Modash Italy fitness and skincare, 11 Nov 2026. Thousands except ER.
        snapshot = [
            ("vincenzo_cairo", 374.3, 8.98, 368.9),
            ("aisha.lyb", 128.5, 10.28, 244.4),
            ("la_elibeauty", 30.3, 5.98, 49.2),
        ]
        text = subprocess.check_output(["pdftotext", "-layout", PDF, "-"], text=True)
        self.assertIn("374.3", text, "Cairo's Instagram denominator is 374.3k, not 397k")
        positions = []
        for handle, followers, engagement, plays in snapshot:
            cells = [f"@{handle}", f"{followers:.1f}k", f"{engagement:.2f}%",
                     f"{plays:.1f}k", f"{plays / followers:.2f}"]
            row = re.search(r"\s+".join(map(re.escape, cells)) + r"\b", text)
            self.assertIsNotNone(row, f"Published metrics or plays/follower wrong for {handle}")
            positions.append(row.start())
        self.assertEqual(positions, sorted(positions), "Rows should descend by Instagram size")

    def test_native_tiktok_rows_reconcile_to_visible_post_counts(self):
        text = subprocess.check_output(["pdftotext", "-f", "4", "-l", "4", "-layout", PDF, "-"], text=True)
        groups = {}
        with Path(__file__).with_name("tiktok-profile-posts-2026-11-26.csv").open() as f:
            for row in csv.DictReader(f):
                groups.setdefault((row["handle"], int(row["followers"])), []).append(row)
        self.assertEqual(len(groups), 9)
        for (handle, followers), rows in groups.items():
            self.assertEqual(len(rows), len({r["post_id"] for r in rows}))
            mean = sum(int(r["play_count"]) for r in rows) / len(rows)
            self.assertRegex(text, rf"{followers:,}\s+{len(rows)}\s+{mean:,.0f}\b", handle)

    def test_trend_table_and_november_timing_reconcile_to_export(self):
        with Path(__file__).with_name("google-trends-timeseries-2026-11-26.csv").open() as f:
            _, _, header, *weeks = csv.reader(f)
        page = subprocess.check_output(["pdftotext", "-layout", "-f", "3", "-l", "3", PDF, "-"], text=True)
        for column, label in enumerate(header[1:], 1):
            term = label.split(":")[0]
            by_year = {y: [(w[0], int(w[column])) for w in weeks if w[0].startswith(str(y))]
                       for y in range(2022, 2026)}
            means = [statistics.mean(i for _, i in by_year[y]) for y in (2022, 2025)]
            self.assertRegex(page, rf"{re.escape(term)}\s+{means[0]:.1f}\s+{means[1]:.1f}\b")
            if term == "spazzolino elettrico":
                for series in by_year.values():
                    self.assertEqual(max(series, key=lambda x: x[1])[0][5:7], "11")

    def test_slide_ten_names_the_pilot_and_uses_the_roster_evidence(self):
        board = (ROOT / "presentation/storyboard.md").read_text()
        slides = re.findall(r"^\| (\d+) \| (.+)$", board, re.M)
        self.assertEqual([int(n) for n, _ in slides], list(range(1, 11)))
        panel = dict(slides)["10"]
        for evidence in ("@federica.scagnetti", "November", "#SorrisoSbloccato",
                         "14 days", "iO orders", "tagged landing sessions",
                         "attributed", "Extra 5", "../docs/influencer-roster.pdf"):
            with self.subTest(evidence=evidence):
                self.assertIn(evidence, panel)


if __name__ == "__main__":
    unittest.main()
