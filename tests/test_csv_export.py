"""Tests for app.db.csv_export."""

import csv
import tempfile
import unittest
from pathlib import Path

from app.db.csv_export import export_contacts_csv


class ExportContactsCsvTests(unittest.TestCase):
    def setUp(self):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        self.path = Path(temp_dir.name) / "export.csv"

    def read_rows(self):
        with open(self.path, encoding="utf-8-sig", newline="") as file:
            return list(csv.DictReader(file))

    def test_writes_header_and_rows_with_unicode_and_commas(self):
        contact = {"id": 1, "name": "Núñez, Ana", "phone": "123", "email": "a@b.co"}

        result = export_contacts_csv([contact], self.path)

        self.assertEqual(result, self.path)
        self.assertEqual(
            self.read_rows(),
            [{"id": "1", "name": "Núñez, Ana", "phone": "123", "email": "a@b.co"}],
        )

    def test_escapes_text_that_starts_like_a_formula(self):
        contact = {"id": 1, "name": "=SUM(A1)", "phone": "123", "email": "a@b.co"}

        export_contacts_csv([contact], self.path)

        self.assertEqual(self.read_rows()[0]["name"], "'=SUM(A1)")


if __name__ == "__main__":
    unittest.main()
