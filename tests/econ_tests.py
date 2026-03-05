import csv
import json
import os
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF_PATH = os.path.join(BASE_DIR, "ref.json")
ECON_DIR = os.path.join(BASE_DIR, "econ")

with open(REF_PATH) as f:
    REF_DATA = json.load(f)


class TestEconCsvFormat(unittest.TestCase):
    """Validate that econ CSV files have consistent column counts across all rows."""

    def test_consistent_column_count(self):
        bad = []
        for report in REF_DATA["econ"]["reports"]:
            year = report["year"]
            path = os.path.join(ECON_DIR, f"{year}.csv")
            if not os.path.isfile(path):
                bad.append(f"{year}.csv: file not found")
                continue
            with open(path, newline="") as f:
                reader = csv.reader(f)
                header = next(reader)
                expected = len(header)
                for row_num, row in enumerate(reader, start=2):
                    if len(row) != expected:
                        bad.append(
                            f"{year}.csv row {row_num}: expected {expected} columns, got {len(row)}"
                        )
        self.assertEqual(bad, [], f"Column count mismatches: {bad}")
