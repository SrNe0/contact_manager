"""Tests for app.utils.validators."""

import unittest

from app.utils.validators import (
    is_valid_email,
    is_valid_name,
    is_valid_phone,
    parse_contact_id,
)


class ValidatorTests(unittest.TestCase):
    def test_is_valid_name(self):
        self.assertTrue(is_valid_name("Ana"))
        self.assertFalse(is_valid_name(""))
        self.assertFalse(is_valid_name("   "))

    def test_is_valid_phone_accepts_ascii_digits_only(self):
        self.assertTrue(is_valid_phone("0123456789"))
        for phone in ("", "12a", "+57", "12 34", "٣٤", "²"):
            with self.subTest(phone=phone):
                self.assertFalse(is_valid_phone(phone))

    def test_is_valid_email(self):
        for email in ("ana@example.com", "a.b+c@mail.example.co"):
            with self.subTest(email=email):
                self.assertTrue(is_valid_email(email))
        for email in ("", "ana", "ana@", "@example.com", "ana@example", "a b@c.co",
                      "a@b@c.co", "ana@example."):
            with self.subTest(email=email):
                self.assertFalse(is_valid_email(email))

    def test_parse_contact_id(self):
        self.assertEqual(parse_contact_id("12"), 12)
        for raw_id in ("", "0", "-1", "1_2", "abc", "1.5", "٣"):
            with self.subTest(raw_id=raw_id):
                self.assertIsNone(parse_contact_id(raw_id))


if __name__ == "__main__":
    unittest.main()
