import unittest
from unittest.mock import patch

import check_pair


class ForestEvidence(unittest.TestCase):
    def test_off_grid_score_cannot_pass_by_agreeing_across_workspaces(self):
        with patch.object(check_pair, "rows", side_effect=[[], [{
                "Pdv Code": "1251", "P (target=success)": "0.601", "model count": "100"}]]):
            with self.assertRaisesRegex(ValueError, "off-grid"):
                check_pair.scores(check_pair.Path("."), "refit")

    def test_bad_denominator_fails_even_with_an_exact_grid_score(self):
        with patch.object(check_pair, "rows", side_effect=[[], [{
                "Pdv Code": "1251", "P (target=success)": "0.60", "model count": "99"}]]):
            with self.assertRaisesRegex(ValueError, "100"):
                check_pair.scores(check_pair.Path("."), "refit")

    def test_widened_native_tie_is_sixty_votes(self):
        from check_pair import votes
        self.assertEqual(votes("0.6000000238418579", "100"), 60)
