MENU_WIDTH = 50
NOT_PROVIDED = "Not provided"
CONFIRM_YES_VALUES = {"yes", "y"}


def clear_screen():
    """
    Clears the console screen using ANSI escape codes.

    Note:
        Works in most terminals that support ANSI escape sequences.
    """
    print("\033[2J\033[H", end="")


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


def show_contact(contact):
    """
    Displays a single contact.

    Args:
        contact (dict): Contact information with keys: id, name, phone, email.
    """
    print(f"\nID: {contact['id']}")
    print(f"Name: {contact['name']}")
    print(f"Phone: {contact['phone']}")
    print(f"Email: {contact['email']}")
    print("-" * MENU_WIDTH)


def add_contact(contacts):
    """
    Adds a new contact.

    Args:
        contacts (list[dict]): Current contact list.

    Returns:
        list[dict]: Updated contact list.
    """
    print("\n--- ADD NEW CONTACT ---")

    name = input("Name: ").strip()
    if not name:
        print("Error: Name cannot be empty.")
        return contacts

    phone = prompt_phone_digits("Phone (digits only, optional): ", allow_empty=True)
    email = input("Email (optional): ").strip()

    new_contact = {
        "id": generate_id(contacts),
        "name": name,
        "phone": phone if phone else NOT_PROVIDED,
        "email": email if email else NOT_PROVIDED,
    }

    contacts.append(new_contact)
    print(f"\nContact '{name}' added successfully!")
    return contacts


def view_all_contacts(contacts):
    """
    Displays all contacts.

    Args:
        contacts (list[dict]): List of contacts.

    Returns:
        list[dict]: The contact list (unchanged).
    """
    print("\n--- ALL CONTACTS ---")

    if not contacts:
        print("No contacts found.")
        return contacts

    for contact in contacts:
        print(f"\n[{contact['id']}] {contact['name']}")
        print(f"    Phone: {contact['phone']}")
        print(f"    Email: {contact['email']}")

    return contacts


def search_contact(contacts):
    """
    Searches for a contact by ID and displays it if found.

    Args:
        contacts (list[dict]): List of contacts.

    Returns:
        list[dict]: The contact list (unchanged).
    """
    print("\n--- SEARCH CONTACT ---")

    if not contacts:
        print("No contacts available.")
        return contacts

    contact_id = prompt_int("Enter contact ID: ")
    index = find_contact_index_by_id(contacts, contact_id)

    if index == -1:
        print(f"Contact with ID {contact_id} not found.")
        return contacts

    show_contact(contacts[index])
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
    print("\n--- UPDATE CONTACT ---")

    if not contacts:
        print("No contacts available.")
        return contacts

    contact_id = prompt_int("Enter contact ID: ")
    index = find_contact_index_by_id(contacts, contact_id)

    if index == -1:
        print(f"Contact with ID {contact_id} not found.")
        return contacts

    print("\nCurrent information:")
    show_contact(contacts[index])

    print("\nEnter new values (press Enter to keep current):")

    new_name = input("Name: ").strip()
    if new_name:
        contacts[index]["name"] = new_name

    new_phone = prompt_phone_digits("Phone (digits only): ", allow_empty=True)
    if new_phone:
        contacts[index]["phone"] = new_phone

    new_email = input("Email: ").strip()
    if new_email:
        contacts[index]["email"] = new_email

    print("\nContact updated successfully!")
    return contacts


def delete_contact(contacts):
    """
    Deletes a contact by ID after user confirmation.

    Args:
        contacts (list[dict]): Current contact list.

    Returns:
        list[dict]: Updated contact list.
    """
    print("\n--- DELETE CONTACT ---")

    if not contacts:
        print("No contacts available.")
        return contacts

    contact_id = prompt_int("Enter contact ID: ")
    index = find_contact_index_by_id(contacts, contact_id)

    if index == -1:
        print(f"Contact with ID {contact_id} not found.")
        return contacts

    print("\nContact to delete:")
    show_contact(contacts[index])

    confirmation = input("Are you sure? (yes/no): ").lower().strip()
    if confirmation in CONFIRM_YES_VALUES:
        deleted = contacts.pop(index)
        print(f"\nContact '{deleted['name']}' deleted.")
        return contacts

    print("\nDeletion cancelled.")
    return contacts


def main():
    """
    Runs the Contact Manager program.
    """
    contacts = []

    menu_actions = {
        "1": add_contact,
        "2": view_all_contacts,
        "3": search_contact,
        "4": update_contact,
        "5": delete_contact,
        "6": None,
    }

    print("\nWelcome to Contact Manager!")

    while True:
        clear_screen()
        show_menu()

        option = input("\nSelect option (1-6): ").strip()

        if option == "6":
            print("\nThank you for using Contact Manager!")
            break

        action = menu_actions.get(option)
        if action is None:
            print("\nInvalid option. Please select 1-6.")
            input("\nPress Enter to continue...")
            continue

        contacts = action(contacts)
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
