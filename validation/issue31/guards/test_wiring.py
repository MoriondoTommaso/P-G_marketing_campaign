"""Fast structural regressions; the separate fixtures exercise the native nodes."""
import os
from pathlib import Path
import unittest
from zipfile import ZipFile
import xml.etree.ElementTree as E


class ExportGuards(unittest.TestCase):
    def setUp(self):
        candidate = os.environ.get("CANDIDATE", "workflows/oral-b-italy.knwf")
        self.z = ZipFile(candidate)
        self.addCleanup(self.z.close)

    def test_both_score_joins_match_fold_and_id(self):
        for i in (121, 122):
            p, = [p for p in self.z.namelist() if p.endswith(f"(#{i})/settings.xml")]
            r = E.fromstring(self.z.read(p))
            pairs = [[e.get("value") for e in crit.findall(".//{*}entry[@key='regularChoice']")]
                     for crit in r.find(".//{*}config[@key='matchingCriteria']")]
            self.assertEqual(pairs, [["store_id", "store_id"], ["fold", "fold"]])

    def test_all_exports_share_a_blocking_predecessor(self):
        writers = [p for p in self.z.namelist() if "/CSV Writer (#" in p and p.endswith("settings.xml")]
        self.assertEqual(len(writers), 13)
        parents = {p.rsplit("/", 2)[0] for p in writers}
        self.assertEqual(len(parents), 1, "release writers run on independent early branches")
        p, = parents
        r = E.fromstring(self.z.read(p + "/workflow.knime"))
        edges = [{v.get("key"): v.get("value") for v in e}
                 for e in r.find("./{*}config[@key='connections']")]
        import re
        ids = {re.search(r'CSV Writer \(#(\d+)\)', n)[1] for n in writers}
        deps = [e for e in edges if e['destID'] in ids and e["destPort"] == "0"]
        self.assertEqual(len(deps), 13)
        self.assertEqual(len({e["sourceID"] for e in deps}), 1)
        self.assertNotEqual(deps[0]["sourceID"], "-1")


if __name__ == "__main__":
    unittest.main()
