"""
Contact model functions.

This module provides functions to create and normalize contact dictionaries.
No classes are used; contacts are represented as dictionaries.
"""

from app.configs.settings import NOT_PROVIDED


def create_contact(contact_id, name, phone, email):
    """
    Creates a new contact dictionary.

    Args:
        contact_id (int): Unique identifier for the contact.
        name (str): Contact name.
        phone (str): Contact phone number.
        email (str): Contact email address.

    Returns:
        dict: A dictionary representing a contact with keys: id, name, phone,
              email.
    """
    return {
        "id": contact_id,
        "name": name,
        "phone": phone if phone else NOT_PROVIDED,
        "email": email if email else NOT_PROVIDED,
    }


def normalize_contact(contact):
    """
    Ensures a contact dictionary has all required fields.

    Args:
        contact (dict): Contact dictionary to normalize.

    Returns:
        dict: Normalized contact dictionary.
    """
    return {
        "id": contact.get("id", 0),
        "name": contact.get("name", ""),
        "phone": contact.get("phone", NOT_PROVIDED),
        "email": contact.get("email", NOT_PROVIDED),
    }
