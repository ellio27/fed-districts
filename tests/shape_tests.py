import json
import os
import re
import unittest
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF_PATH = os.path.join(BASE_DIR, "ref.json")
SHAPES_DIR = os.path.join(BASE_DIR, "shapes")

with open(REF_PATH) as f:
    REF_DATA = json.load(f)

STATES = REF_DATA["shapes"]["states"]
DISTRICT_PATTERN = re.compile(r"^[0-9]{2}\.geojson$")

ALL_50 = {
    "al", "ak", "az", "ar", "ca", "co", "ct", "de", "fl", "ga",
    "hi", "id", "il", "in", "ia", "ks", "ky", "la", "me", "md",
    "ma", "mi", "mn", "ms", "mo", "mt", "ne", "nv", "nh", "nj",
    "nm", "ny", "nc", "nd", "oh", "ok", "or", "pa", "ri", "sc",
    "sd", "tn", "tx", "ut", "vt", "va", "wa", "wv", "wi", "wy",
}


def get_year_folders(state):
    """Return sorted list of year ints that have a folder for this state."""
    years = []
    if not os.path.isdir(SHAPES_DIR):
        return years
    for name in os.listdir(SHAPES_DIR):
        state_dir = os.path.join(SHAPES_DIR, name, state)
        if os.path.isdir(state_dir):
            try:
                years.append(int(name))
            except ValueError:
                pass
    return sorted(years)


class TestRefJson(unittest.TestCase):
    """Validate the structure and content of ref.json."""

    def test_all_50_states_present(self):
        missing = ALL_50 - set(STATES.keys())
        extra = set(STATES.keys()) - ALL_50
        self.assertEqual(missing, set(), f"Missing states: {missing}")
        self.assertEqual(extra, set(), f"Extra states: {extra}")

    def test_entries_have_required_fields(self):
        bad = []
        for st, entries in STATES.items():
            for i, entry in enumerate(entries):
                for field in ("firstCongress", "enacted", "districts", "source"):
                    if field not in entry:
                        bad.append(f"{st}[{i}] missing '{field}'")
        self.assertEqual(bad, [], f"Entries missing required fields: {bad}")

    def test_districts_are_positive_ints(self):
        bad = []
        for st, entries in STATES.items():
            for i, entry in enumerate(entries):
                districts = entry.get("districts")
                if not isinstance(districts, int) or districts < 1:
                    bad.append(f"{st}[{i}]: districts={districts}")
        self.assertEqual(bad, [], f"Invalid district values: {bad}")

    def test_435_total_districts(self):
        """Sum of districts from the current (first) entry per state should be 435."""
        total = 0
        counts = {}
        for st, entries in STATES.items():
            if entries:
                districts = entries[0]["districts"]
                counts[st] = districts
                total += districts
        self.assertEqual(
            total,
            435,
            f"Expected 435 districts, found {total}. Per-state counts: {counts}",
        )

    def test_firstCongress_after_enacted(self):
        """firstCongress year must be after the enacted date for every entry."""
        bad = []
        for st, entries in STATES.items():
            for i, entry in enumerate(entries):
                enacted = entry.get("enacted")
                first_congress = entry.get("firstCongress")
                if enacted is None or first_congress is None:
                    continue
                enacted_date = date.fromisoformat(enacted)
                # firstCongress is a year (int); the congress starts Jan 3
                congress_start = date(first_congress, 1, 3)
                if congress_start <= enacted_date:
                    bad.append(
                        f"{st}[{i}]: firstCongress {first_congress} "
                        f"is not after enacted {enacted}"
                    )
        self.assertEqual(bad, [], f"firstCongress not after enacted: {bad}")

    def test_entries_in_reverse_chronological_order(self):
        """Entries for each state must be ordered by firstCongress descending."""
        bad = []
        for st, entries in STATES.items():
            years = [e["firstCongress"] for e in entries]
            if years != sorted(years, reverse=True):
                bad.append(f"{st}: {years}")
        self.assertEqual(bad, [], f"Entries not in reverse chronological order: {bad}")


class TestDistrictNaming(unittest.TestCase):
    """All district files must be named XX.geojson where XX is two digits."""

    def test_all_districts_follow_naming_convention(self):
        bad = []
        for year_name in os.listdir(SHAPES_DIR):
            year_path = os.path.join(SHAPES_DIR, year_name)
            if not os.path.isdir(year_path):
                continue
            for st in os.listdir(year_path):
                st_path = os.path.join(year_path, st)
                if not os.path.isdir(st_path):
                    continue
                for fname in os.listdir(st_path):
                    if fname.endswith(".geojson") and not DISTRICT_PATTERN.match(fname):
                        bad.append(f"{year_name}/{st}/{fname}")
        self.assertEqual(bad, [], f"Files with incorrect naming: {bad}")


class TestYearFolders(unittest.TestCase):
    """Each state in ref.json must have at least one year folder with district files."""

    def test_every_state_has_folder(self):
        missing = []
        for st in STATES:
            years = get_year_folders(st)
            if not years:
                missing.append(st)
        self.assertEqual(missing, [], f"States with no shape folders: {missing}")

    def test_every_folder_has_districts(self):
        empty = []
        for st in STATES:
            for year in get_year_folders(st):
                folder = os.path.join(SHAPES_DIR, str(year), st)
                geojson = [f for f in os.listdir(folder) if f.endswith(".geojson")]
                if len(geojson) == 0:
                    empty.append(f"{st}/{year}")
        self.assertEqual(empty, [], f"Folders with no district files: {empty}")

    def test_firstCongress_years_match_folders(self):
        """Each entry's firstCongress value should have a matching year folder and vice versa."""
        mismatched = []
        for st, entries in STATES.items():
            entry_years = sorted(e["firstCongress"] for e in entries)
            folder_years = get_year_folders(st)
            if entry_years != folder_years:
                mismatched.append(
                    f"{st}: firstCongress={entry_years}, folders={folder_years}"
                )
        self.assertEqual(
            mismatched, [], f"firstCongress/folder mismatches: {mismatched}"
        )


class TestDistrictCount(unittest.TestCase):
    """For each state, the latest year folder's file count should match the current districts."""

    def test_latest_folder_file_count_matches_districts(self):
        mismatched = []
        for st, entries in STATES.items():
            if not entries:
                continue
            districts = entries[0]["districts"]
            years = get_year_folders(st)
            if not years:
                continue
            latest = max(years)
            folder = os.path.join(SHAPES_DIR, str(latest), st)
            n = len([f for f in os.listdir(folder) if f.endswith(".geojson")])
            if n != districts:
                mismatched.append(f"{st}: {districts} districts but {n} files in {latest}/")
        self.assertEqual(
            mismatched, [], f"File count mismatches: {mismatched}"
        )

    def test_435_total_files_on_disk(self):
        """Counting only the latest year folder per state, total files should be 435."""
        total = 0
        counts = {}
        for st in STATES:
            years = get_year_folders(st)
            if not years:
                continue
            latest = max(years)
            folder = os.path.join(SHAPES_DIR, str(latest), st)
            n = len([f for f in os.listdir(folder) if f.endswith(".geojson")])
            counts[st] = n
            total += n
        self.assertEqual(
            total,
            435,
            f"Expected 435 district files, found {total}. Per-state: {counts}",
        )


if __name__ == "__main__":
    unittest.main()
