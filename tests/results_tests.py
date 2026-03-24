import csv
import json
import os
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF_PATH = os.path.join(BASE_DIR, "ref.json")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

with open(REF_PATH) as f:
    REF_DATA = json.load(f)

YEARS = REF_DATA["results"]["years"]


class TestResultsFilesExist(unittest.TestCase):
    """Each entry in ref.json results/years must have corresponding CSV files."""

    def test_all_result_files_exist(self):
        missing = []
        for entry in YEARS:
            year = entry["year"]
            for typ in entry["types"]:
                path = os.path.join(RESULTS_DIR, str(year), f"{typ}.csv")
                if not os.path.isfile(path):
                    missing.append(f"{year}/{typ}.csv")
        self.assertEqual(missing, [], f"Missing results files: {missing}")


class TestResultsDistrictCount(unittest.TestCase):
    """Each house.csv and president.csv must contain exactly 435 district entries."""

    def test_435_districts_per_file(self):
        bad = []
        for entry in YEARS:
            year = entry["year"]
            for typ in entry["types"]:
                path = os.path.join(RESULTS_DIR, str(year), f"{typ}.csv")
                if not os.path.isfile(path):
                    continue
                with open(path, newline="") as f:
                    reader = csv.reader(f)
                    next(reader)  # skip header
                    row_count = sum(1 for _ in reader)
                if row_count != 435:
                    bad.append(f"{year}/{typ}.csv: expected 435 rows, got {row_count}")
        self.assertEqual(bad, [], f"Incorrect district counts: {bad}")
