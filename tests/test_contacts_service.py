"""Tests for app.services.contacts_service."""

import copy
import unittest

from app.configs.settings import NOT_PROVIDED
from app.services.contacts_service import (
    add_contact,
    delete_contact,
    find_contact_by_id,
    find_duplicates,
    generate_id,
    search_contacts,
    update_contact,
)

CONTACTS = [
    {"id": 1, "name": "Ana Gómez", "phone": "3001112222", "email": "ana@example.com"},
    {"id": 3, "name": "Luis Peña", "phone": NOT_PROVIDED, "email": "luis@example.com"},
    {"id": 12, "name": "Marta Ruiz", "phone": "3123", "email": NOT_PROVIDED},
]


class ServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.contacts = copy.deepcopy(CONTACTS)

    def assert_input_unchanged(self):
        self.assertEqual(self.contacts, CONTACTS)


class GenerateIdTests(ServiceTestCase):
    def test_first_id_is_one(self):
        self.assertEqual(generate_id([]), 1)

    def test_uses_highest_id_plus_one_despite_gaps(self):
        self.assertEqual(generate_id(self.contacts), 13)


class FindContactByIdTests(ServiceTestCase):
    def test_found(self):
        self.assertEqual(find_contact_by_id(self.contacts, 3)["name"], "Luis Peña")

    def test_not_found(self):
        self.assertIsNone(find_contact_by_id(self.contacts, 99))


class SearchContactsTests(ServiceTestCase):
    def ids(self, query):
        return [contact["id"] for contact in search_contacts(self.contacts, query)]

    def test_partial_match_ignores_case(self):
        self.assertEqual(self.ids("gÓm"), [1])

    def test_matches_phone_and_email(self):
        self.assertEqual(self.ids("1112"), [1])
        self.assertEqual(self.ids("LUIS@"), [3])

    def test_matches_exact_id_and_phone_digits(self):
        self.assertEqual(self.ids("12"), [1, 12])
        self.assertEqual(self.ids("3"), [1, 3, 12])

    def test_placeholder_never_matches(self):
        self.assertEqual(self.ids("provided"), [])

    def test_empty_query_returns_nothing(self):
        self.assertEqual(self.ids("   "), [])


class FindDuplicatesTests(ServiceTestCase):
    def test_finds_same_phone(self):
        result = find_duplicates(self.contacts, phone="3123")
        self.assertEqual([contact["id"] for contact in result], [12])

    def test_finds_same_email_ignoring_case(self):
        result = find_duplicates(self.contacts, email="LUIS@EXAMPLE.COM")
        self.assertEqual([contact["id"] for contact in result], [3])

    def test_empty_values_do_not_match_missing_fields(self):
        self.assertEqual(find_duplicates(self.contacts), [])

    def test_excludes_the_contact_being_updated(self):
        result = find_duplicates(self.contacts, phone="3123", exclude_id=12)
        self.assertEqual(result, [])


class AddContactTests(ServiceTestCase):
    def test_returns_new_list_and_contact(self):
        new_contacts, contact = add_contact(self.contacts, "Eva", "55", "eva@a.co")

        self.assertEqual(contact["id"], 13)
        self.assertEqual(new_contacts[-1], contact)
        self.assertEqual(len(new_contacts), 4)
        self.assert_input_unchanged()

    def test_optional_fields_use_placeholder(self):
        _, contact = add_contact(self.contacts, "Eva")
        self.assertEqual(contact["phone"], NOT_PROVIDED)
        self.assertEqual(contact["email"], NOT_PROVIDED)

    def test_rejects_invalid_fields(self):
        invalid = [("", "", ""), ("  ", "", ""), ("Eva", "12a", ""), ("Eva", "", "x")]
        for name, phone, email in invalid:
            with self.subTest(name=name, phone=phone, email=email):
                with self.assertRaises(ValueError):
                    add_contact(self.contacts, name, phone, email)
        self.assert_input_unchanged()


class UpdateContactTests(ServiceTestCase):
    def test_none_keeps_current_values(self):
        _, contact = update_contact(self.contacts, 1, name="Ana G")

        self.assertEqual(contact["name"], "Ana G")
        self.assertEqual(contact["phone"], "3001112222")
        self.assertEqual(contact["email"], "ana@example.com")
        self.assert_input_unchanged()

    def test_empty_values_clear_optional_fields(self):
        _, contact = update_contact(self.contacts, 1, phone="", email="")
        self.assertEqual(contact["phone"], NOT_PROVIDED)
        self.assertEqual(contact["email"], NOT_PROVIDED)

    def test_keeps_position_in_list(self):
        new_contacts, _ = update_contact(self.contacts, 3, name="Luis")
        self.assertEqual([contact["id"] for contact in new_contacts], [1, 3, 12])
        self.assertEqual(new_contacts[1]["name"], "Luis")

    def test_rejects_invalid_fields(self):
        for fields in ({"name": ""}, {"phone": "abc"}, {"email": "abc"}):
            with self.subTest(fields=fields):
                with self.assertRaises(ValueError):
                    update_contact(self.contacts, 1, **fields)
        self.assert_input_unchanged()

    def test_unknown_id_raises(self):
        with self.assertRaises(LookupError):
            update_contact(self.contacts, 99, name="X")


class DeleteContactTests(ServiceTestCase):
    def test_returns_new_list_and_deleted_contact(self):
        new_contacts, deleted = delete_contact(self.contacts, 3)

        self.assertEqual(deleted["name"], "Luis Peña")
        self.assertEqual([contact["id"] for contact in new_contacts], [1, 12])
        self.assert_input_unchanged()

    def test_unknown_id_raises(self):
        with self.assertRaises(LookupError):
            delete_contact(self.contacts, 99)


if __name__ == "__main__":
    unittest.main()
