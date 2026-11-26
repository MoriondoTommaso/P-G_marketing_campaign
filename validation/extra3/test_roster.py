"""Check the figures a reader actually receives in the PDF (requires Poppler)."""
from pathlib import Path
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "outputs/Roaster_Influencers.pdf"


class RosterEvidence(unittest.TestCase):
    def test_instagram_shortlist_matches_public_snapshot(self):
        # Modash Italy skincare, 11 Nov 2026. Values in thousands except ER.
        snapshot = [
            ("aisha.lyb", 128.5, 10.28, 244.4),
            ("vincenzo_cairo", 374.3, 8.98, 368.9),
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
        self.assertEqual(positions, sorted(positions), "Rows should descend by Instagram ER")


if __name__ == "__main__":
    unittest.main()
