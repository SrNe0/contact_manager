"""
JSON persistence layer.

This module handles loading and saving contacts to a JSON file.
No business logic is included here.
"""

import json
import os

from app.configs.settings import JSON_FILE_PATH


def load_contacts():
    """
    Loads contacts from the JSON file.

    Returns:
        list[dict]: List of contact dictionaries. Returns an empty list if
                    the file does not exist or contains invalid JSON.
    """
    if not os.path.exists(JSON_FILE_PATH):
        return []

    try:
        with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            print(f"Warning: {JSON_FILE_PATH} does not contain a list.")
            return []
    except json.JSONDecodeError:
        print(f"Error: {JSON_FILE_PATH} contains invalid JSON. Starting fresh.")
        return []
    except Exception as error:
        print(f"Error loading contacts: {error}")
        return []


def save_contacts(contacts):
    """
    Saves contacts to the JSON file.

    Args:
        contacts (list[dict]): List of contact dictionaries to save.

    Returns:
        bool: True if save was successful, False otherwise.
    """
    try:
        with open(JSON_FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(contacts, file, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        print(f"Error saving contacts: {error}")
        return False
