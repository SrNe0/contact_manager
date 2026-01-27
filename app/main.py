"""
Contact Manager (CLI) - Main Entry Point.

A local CRUD application that manages contacts with JSON persistence using
a layered architecture. This module intentionally avoids classes (OOP) and
uses functions only.

Features:
- Create: Add a contact
- Read: List contacts, search by ID
- Update: Edit contact fields
- Delete: Remove a contact
- Persistence: Automatic JSON file storage
"""

from app.configs.settings import EXIT_OPTION
from app.db.json_store import load_contacts
from app.interface.menu import (
    print_message,
    prompt_menu_option,
    show_menu,
    wait_for_enter,
)
from app.services.contacts_service import (
    add_contact,
    delete_contact,
    search_contact,
    update_contact,
    view_all_contacts,
)
from app.utils.console import clear_screen


def main():
    """
    Runs the Contact Manager program.

    Loads contacts from JSON file on startup and provides an interactive
    menu for CRUD operations. Changes are automatically saved to the JSON file.
    """
    contacts = load_contacts()

    menu_actions = {
        "1": add_contact,
        "2": view_all_contacts,
        "3": search_contact,
        "4": update_contact,
        "5": delete_contact,
        "6": None,
    }

    print_message("\nWelcome to Contact Manager!")

    while True:
        clear_screen()
        show_menu()

        option = prompt_menu_option()

        if option == str(EXIT_OPTION):
            print_message("\nThank you for using Contact Manager!")
            break

        action = menu_actions.get(option)
        if action is None:
            print_message("\nInvalid option. Please select 1-6.")
            wait_for_enter()
            continue

        contacts = action(contacts)
        wait_for_enter()


if __name__ == "__main__":
    main()
