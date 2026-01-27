"""
Input validation utilities.

This module provides validation functions for user input.
"""


def prompt_phone_digits(message, allow_empty):
    """
    Prompts the user for a phone number containing only digits.

    Args:
        message (str): Prompt message displayed to the user.
        allow_empty (bool): If True, empty input is accepted and returned as "".

    Returns:
        str: Digits-only phone string, or "" if allowed and empty.
    """
    while True:
        phone = input(message).strip()

        if allow_empty and phone == "":
            return ""

        if phone.isdigit():
            return phone

        print("Error: Phone must contain digits only (0-9).")
