"""Tests for app.db.json_store."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from app.db.json_store import load_contacts, save_contacts

ANA = {"id": 1, "name": "Ana", "phone": "123", "email": "ana@example.com"}


class JsonStoreTestCase(unittest.TestCase):
    def setUp(self):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        self.dir = Path(temp_dir.name)
        self.path = self.dir / "contacts.json"

    def backups(self):
        return list(self.dir.glob("contacts.json.corrupt-*"))


class LoadContactsTests(JsonStoreTestCase):
    def test_missing_file_returns_empty_list_without_warning(self):
        self.assertEqual(load_contacts(self.path), ([], None))

    def test_valid_file_loads_without_warning(self):
        self.path.write_text(json.dumps([ANA]), encoding="utf-8")
        self.assertEqual(load_contacts(self.path), ([ANA], None))
        self.assertEqual(self.backups(), [])

    def test_invalid_data_is_preserved_in_a_backup(self):
        damaged = {
            "invalid JSON": b'[{"id": 1, "name": "Ana"',
            "not a list": b'{"id": 1}',
            "invalid encoding": b"\xff\xfe\x00",
        }
        for label, content in damaged.items():
            with self.subTest(label):
                self.path.write_bytes(content)

                contacts, warning = load_contacts(self.path)

                self.assertEqual(contacts, [])
                self.assertIn("damaged", warning)
                self.assertFalse(self.path.exists())
                backups = self.backups()
                self.assertEqual(len(backups), 1)
                self.assertEqual(backups[0].read_bytes(), content)
                backups[0].unlink()

    def test_partly_damaged_file_recovers_valid_records_and_keeps_original(self):
        content = json.dumps([ANA, {"id": 2}, "bad"])
        self.path.write_text(content, encoding="utf-8")

        contacts, warning = load_contacts(self.path)

        self.assertEqual(contacts, [ANA])
        self.assertIn("2 damaged record(s)", warning)
        self.assertEqual(json.loads(self.path.read_text(encoding="utf-8")), [ANA])
        self.assertEqual(self.backups()[0].read_text(encoding="utf-8"), content)

    def test_repairable_records_load_without_backup(self):
        self.path.write_text('[{"name": "Ana"}]', encoding="utf-8")

        contacts, warning = load_contacts(self.path)

        self.assertEqual(contacts[0]["id"], 1)
        self.assertIsNone(warning)
        self.assertEqual(self.backups(), [])

    def test_read_failure_raises_instead_of_starting_empty(self):
        self.path.write_text("[]", encoding="utf-8")
        with mock.patch("builtins.open", side_effect=PermissionError("denied")):
            with self.assertRaises(OSError):
                load_contacts(self.path)


class SaveContactsTests(JsonStoreTestCase):
    def test_round_trip_keeps_unicode(self):
        contact = {**ANA, "name": "Ñandú Martínez"}
        save_contacts([contact], self.path)

        self.assertEqual(load_contacts(self.path), ([contact], None))
        self.assertIn("Ñandú", self.path.read_text(encoding="utf-8"))

    def test_failed_write_keeps_original_and_removes_temp_file(self):
        save_contacts([ANA], self.path)
        original = self.path.read_bytes()

        with mock.patch("os.replace", side_effect=PermissionError("denied")):
            with self.assertRaises(OSError):
                save_contacts([], self.path)

        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual([item.name for item in self.dir.iterdir()], [self.path.name])

    def test_unserializable_data_never_touches_the_file(self):
        save_contacts([ANA], self.path)
        original = self.path.read_bytes()

        with self.assertRaises(TypeError):
            save_contacts([{"id": 1, "name": object()}], self.path)

        self.assertEqual(self.path.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
