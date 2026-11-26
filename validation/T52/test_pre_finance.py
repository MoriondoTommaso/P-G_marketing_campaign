import unittest
from unittest.mock import patch

import check_pair


class ForestEvidence(unittest.TestCase):
    def test_class_archive_contains_no_java_snippet_nodes(self):
        from xml.etree import ElementTree as ET
        from zipfile import ZipFile
        from native_folds import ROOT
        with ZipFile(ROOT / "workflows/oral-b-italy-final.knwf") as archive:
            snippets = []
            for path in archive.namelist():
                if path.endswith("/settings.xml"):
                    node = ET.fromstring(archive.read(path))
                    factory = node.find("*[@key='factory']")
                    if factory is not None and any(term in factory.get("value", "").lower()
                                                   for term in ("javasnippet", "javascripting")):
                        snippets.append(path)
        self.assertEqual(snippets, [])

    def test_one_workspace_cannot_attest_to_two_native_runs(self):
        from pre_finance import compare_inputs
        from pathlib import Path
        with self.assertRaisesRegex(ValueError, "distinct"):
            compare_inputs(Path("."), Path("."))

    def test_replacing_one_funded_store_preserves_count_but_fails_membership(self):
        from check_pair import check_funded
        with self.assertRaisesRegex(ValueError, "funded IDs"):
            check_funded([{"store_id": "old-failure"}, {"store_id": "new-win"}],
                         {"old-success", "new-win"})

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
