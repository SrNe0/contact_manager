"""
User interface and menu functions.

This module handles all user interaction: displaying menus, prompting for
input, and reading user responses.
"""

from app.configs.settings import MENU_WIDTH


def show_menu():
    """
    Displays the main menu.
    """
    print("\n" + "=" * MENU_WIDTH)
    print("CONTACT MANAGER".center(MENU_WIDTH))
    print("=" * MENU_WIDTH)
    print("1. Add contact")
    print("2. View all contacts")
    print("3. Search contact")
    print("4. Update contact")
    print("5. Delete contact")
    print("6. Exit")
    print("=" * MENU_WIDTH)


def prompt_menu_option():
    """
    Prompts the user to select a menu option.

    Returns:
        str: The user's menu selection as a string.
    """
    return input("\nSelect option (1-6): ").strip()


def prompt_string(message):
    """
    Prompts the user for a string input.

    Args:
        message (str): Prompt message displayed to the user.

    Returns:
        str: The user's input, stripped of leading/trailing whitespace.
    """
    return input(message).strip()


def prompt_int(message):
    """
    Prompts the user for an integer until a valid integer is provided.

    Args:
        message (str): Prompt message displayed to the user.

    Returns:
        int: The validated integer provided by the user.
    """
    while True:
        raw = input(message).strip()
        try:
            return int(raw)
        except ValueError:
            print("Error: Please enter a valid integer.")


def prompt_confirmation(message):
    """
    Prompts the user for a yes/no confirmation.

    Args:
        message (str): Confirmation message displayed to the user.

    Returns:
        str: The user's response in lowercase and stripped.
    """
    return input(message).lower().strip()


def wait_for_enter():
    """
    Waits for the user to press Enter before continuing.
    """
    input("\nPress Enter to continue...")


def print_message(message):
    """
    Prints a message to the console.

    Args:
        message (str): The message to print.
    """
    print(message)


def print_error(message):
    """
    Prints an error message to the console.

    Args:
        message (str): The error message to print.
    """
    print(f"Error: {message}")
