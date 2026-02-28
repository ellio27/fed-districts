import json
import os
import re
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF_PATH = os.path.join(BASE_DIR, "ref.json")
SHAPES_DIR = os.path.join(BASE_DIR, "shapes")

with open(REF_PATH) as f:
    REF_DATA = json.load(f)

STATES = REF_DATA["shapes"]["states"]
DISTRICT_PATTERN = re.compile(r"^[0-9]{2}\.geojson$")


class TestDistrictNaming(unittest.TestCase):
    """All district files must be named XX.geojson where XX is two digits."""

    def test_all_districts_follow_naming_convention(self):
        bad = []
        for st, entry in STATES.items():
            for year in entry.get("years", []):
                folder = os.path.join(SHAPES_DIR, str(year), st)
                if not os.path.isdir(folder):
                    continue
                for fname in os.listdir(folder):
                    if fname.endswith(".geojson") and not DISTRICT_PATTERN.match(fname):
                        bad.append(f"{st}/{year}/{fname}")
        self.assertEqual(bad, [], f"Files with incorrect naming: {bad}")


class TestYearFolders(unittest.TestCase):
    """Each year in a state's entry must have a corresponding folder with district files."""

    def test_every_year_has_folder(self):
        missing = []
        for st, entry in STATES.items():
            for year in entry.get("years", []):
                folder = os.path.join(SHAPES_DIR, str(year), st)
                if not os.path.isdir(folder):
                    missing.append(f"{st}/{year}")
        self.assertEqual(missing, [], f"Missing folders: {missing}")

    def test_every_folder_has_districts(self):
        empty = []
        for st, entry in STATES.items():
            for year in entry.get("years", []):
                folder = os.path.join(SHAPES_DIR, str(year), st)
                if not os.path.isdir(folder):
                    continue
                geojson = [f for f in os.listdir(folder) if f.endswith(".geojson")]
                if len(geojson) == 0:
                    empty.append(f"{st}/{year}")
        self.assertEqual(empty, [], f"Folders with no district files: {empty}")


class TestDistrictCount(unittest.TestCase):
    """Counting only the most recent year per state, there should be 435 total districts."""

    def test_435_total_districts(self):
        total = 0
        counts = {}
        for st, entry in STATES.items():
            years = entry.get("years", [])
            if not years:
                continue
            latest = max(years)
            folder = os.path.join(SHAPES_DIR, str(latest), st)
            if not os.path.isdir(folder):
                continue
            n = len([f for f in os.listdir(folder) if f.endswith(".geojson")])
            counts[st] = n
            total += n
        self.assertEqual(
            total,
            435,
            f"Expected 435 districts, found {total}. Per-state counts: {counts}",
        )


if __name__ == "__main__":
    unittest.main()
