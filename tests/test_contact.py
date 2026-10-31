"""Tests for app.models.contact."""

import unittest

from app.configs.settings import NOT_PROVIDED
from app.models.contact import create_contact, normalize_contact, normalize_contacts


class CreateContactTests(unittest.TestCase):
    def test_keeps_provided_fields(self):
        contact = create_contact(1, "Ana", "123", "ana@example.com")
        self.assertEqual(
            contact,
            {"id": 1, "name": "Ana", "phone": "123", "email": "ana@example.com"},
        )

    def test_empty_optional_fields_use_placeholder(self):
        contact = create_contact(1, "Ana", "", "")
        self.assertEqual(contact["phone"], NOT_PROVIDED)
        self.assertEqual(contact["email"], NOT_PROVIDED)


class NormalizeContactTests(unittest.TestCase):
    def test_fills_missing_optional_fields(self):
        contact = normalize_contact({"id": 3, "name": "Ana"})
        self.assertEqual(contact["phone"], NOT_PROVIDED)
        self.assertEqual(contact["email"], NOT_PROVIDED)

    def test_converts_numeric_text_id_and_numeric_phone(self):
        contact = normalize_contact({"id": "7", "name": "Ana", "phone": 123})
        self.assertEqual(contact["id"], 7)
        self.assertEqual(contact["phone"], "123")

    def test_unusable_ids_become_zero(self):
        for raw_id in (None, "abc", -1, 0, True, 1.5, "0"):
            with self.subTest(raw_id=raw_id):
                contact = normalize_contact({"id": raw_id, "name": "Ana"})
                self.assertEqual(contact["id"], 0)

    def test_rejects_records_without_a_usable_name(self):
        for raw in ("text", 5, None, {}, {"name": ""}, {"name": "  "}, {"name": 5}):
            with self.subTest(raw=raw):
                self.assertIsNone(normalize_contact(raw))


class NormalizeContactsTests(unittest.TestCase):
    def test_counts_dropped_records(self):
        contacts, dropped = normalize_contacts([{"id": 1, "name": "Ana"}, "bad", {}])
        self.assertEqual([contact["name"] for contact in contacts], ["Ana"])
        self.assertEqual(dropped, 2)

    def test_assigns_new_ids_to_missing_and_duplicated_ids(self):
        contacts, dropped = normalize_contacts(
            [
                {"name": "NoId"},
                {"id": 5, "name": "First"},
                {"id": 5, "name": "Second"},
            ]
        )
        self.assertEqual([contact["id"] for contact in contacts], [6, 5, 7])
        self.assertEqual(dropped, 0)


if __name__ == "__main__":
    unittest.main()
