"""For each attainable training leaf, compare the release rule with exact arithmetic."""
from fractions import Fraction
from pathlib import Path
from struct import pack, unpack
from xml.etree import ElementTree as ET
from zipfile import ZipFile
import re
import unittest


class TreeBoundaries(unittest.TestCase):
    def test_all_leaf_sizes_and_both_predictors(self):
        with ZipFile(Path(__file__).resolve().parents[2] / "workflows/oral-b-italy.knwf") as z:
            for node in (601, 602):
                files = [n for n in z.namelist() if n.endswith(f"(#{node})/settings.xml")]
                self.assertEqual(len(files), 1, "Missing native tree boundary correction")
                rules = ET.fromstring(z.read(files[0])).find(".//{*}config[@key='rules']")
                aliases = {}
                for item in list(rules)[1:-1]:
                    match = re.fullmatch(r"\$P \(target=success\)\$ = ([\d.]+) => ([\d.]+)", item.get("value"))
                    aliases[float(match[1])] = float(match[2])
                for n in range(1, 171):
                    for k in range(n + 1):
                        exact = Fraction(k, n)
                        raw, = unpack("f", pack("f", exact))
                        p = aliases.get(raw, raw)
                        for boundary in (55, 60, 65):
                            self.assertEqual((p > boundary/100, p == boundary/100),
                                             (100*k > boundary*n, 100*k == boundary*n))


if __name__ == "__main__":
    unittest.main()
