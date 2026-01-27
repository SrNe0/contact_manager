"""
Contacts business logic service.

This module contains all CRUD operations and business logic for managing
contacts.
"""

from app.configs.settings import CONFIRM_YES_VALUES
from app.db.json_store import save_contacts
from app.helpers.formatters import format_contact, format_contact_list
from app.interface.menu import (
    print_error,
    print_message,
    prompt_confirmation,
    prompt_int,
    prompt_string,
)
from app.models.contact import create_contact
from app.utils.validators import prompt_phone_digits


def generate_id(contacts):
    """
    Generates a new unique ID for a contact.

    Uses max(existing_ids) + 1 to avoid duplicates after deletions.

    Args:
        contacts (list[dict]): Current list of contacts.

    Returns:
        int: A new unique contact ID.
    """
    if not contacts:
        return 1
    return max(contact["id"] for contact in contacts) + 1


def find_contact_index_by_id(contacts, contact_id):
    """
    Finds the index of a contact by its ID.

    Args:
        contacts (list[dict]): List of contacts.
        contact_id (int): Contact ID to search for.

    Returns:
        int: Index of the contact if found, otherwise -1.
    """
    for index, contact in enumerate(contacts):
        if contact["id"] == contact_id:
            return index
    return -1


def add_contact(contacts):
    """
    Adds a new contact.

    Prompts the user for contact information and adds it to the list.

    Args:
        contacts (list[dict]): Current contact list.

    Returns:
        list[dict]: Updated contact list.
    """
    print_message("\n--- ADD NEW CONTACT ---")

    name = prompt_string("Name: ")
    if not name:
        print_error("Name cannot be empty.")
        return contacts

    phone = prompt_phone_digits("Phone (digits only, optional): ", allow_empty=True)
    email = prompt_string("Email (optional): ")

    new_contact = create_contact(generate_id(contacts), name, phone, email)
    contacts.append(new_contact)
    save_contacts(contacts)

    print_message(f"\nContact '{name}' added successfully!")
    return contacts


def view_all_contacts(contacts):
    """
    Displays all contacts.

    Args:
        contacts (list[dict]): List of contacts.

    Returns:
        list[dict]: The contact list (unchanged).
    """
    print_message("\n--- ALL CONTACTS ---")

    if not contacts:
        print_message("No contacts found.")
        return contacts

    print_message(format_contact_list(contacts))
    return contacts


def search_contact(contacts):
    """
    Searches for a contact by ID and displays it if found.

    Args:
        contacts (list[dict]): List of contacts.

    Returns:
        list[dict]: The contact list (unchanged).
    """
    print_message("\n--- SEARCH CONTACT ---")

    if not contacts:
        print_message("No contacts available.")
        return contacts

    contact_id = prompt_int("Enter contact ID: ")
    index = find_contact_index_by_id(contacts, contact_id)

    if index == -1:
        print_message(f"Contact with ID {contact_id} not found.")
        return contacts

    print_message(format_contact(contacts[index]))
    return contacts


def update_contact(contacts):
    """
    Updates an existing contact by ID.

    The user may press Enter to keep the current value of each field.

    Args:
        contacts (list[dict]): Current contact list.

    Returns:
        list[dict]: Updated contact list.
    """
    print_message("\n--- UPDATE CONTACT ---")

    if not contacts:
        print_message("No contacts available.")
        return contacts

    contact_id = prompt_int("Enter contact ID: ")
    index = find_contact_index_by_id(contacts, contact_id)

    if index == -1:
        print_message(f"Contact with ID {contact_id} not found.")
        return contacts

    print_message("\nCurrent information:")
    print_message(format_contact(contacts[index]))

    print_message("\nEnter new values (press Enter to keep current):")

    new_name = prompt_string("Name: ")
    if new_name:
        contacts[index]["name"] = new_name

    new_phone = prompt_phone_digits("Phone (digits only): ", allow_empty=True)
    if new_phone:
        contacts[index]["phone"] = new_phone

    new_email = prompt_string("Email: ")
    if new_email:
        contacts[index]["email"] = new_email

    save_contacts(contacts)
    print_message("\nContact updated successfully!")
    return contacts


def delete_contact(contacts):
    """
    Deletes a contact by ID after user confirmation.

    Args:
        contacts (list[dict]): Current contact list.

    Returns:
        list[dict]: Updated contact list.
    """
    print_message("\n--- DELETE CONTACT ---")

    if not contacts:
        print_message("No contacts available.")
        return contacts

    contact_id = prompt_int("Enter contact ID: ")
    index = find_contact_index_by_id(contacts, contact_id)

    if index == -1:
        print_message(f"Contact with ID {contact_id} not found.")
        return contacts

    print_message("\nContact to delete:")
    print_message(format_contact(contacts[index]))

    confirmation = prompt_confirmation("Are you sure? (yes/no): ")
    if confirmation in CONFIRM_YES_VALUES:
        deleted = contacts.pop(index)
        save_contacts(contacts)
        print_message(f"\nContact '{deleted['name']}' deleted.")
        return contacts

    print_message("\nDeletion cancelled.")
    return contacts
