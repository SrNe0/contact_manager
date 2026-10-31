# Contact Manager CLI

![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)
![Dependencies: none](https://img.shields.io/badge/dependencies-none-brightgreen)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

A command-line contact management application built with Python using a layered architecture and safe JSON persistence.

## Quick Start

```bash
python -m app.main
```

Run this command from the project root.

## Demo

```text
==================================================
                 CONTACT MANAGER
==================================================
1. Add contact
2. View all contacts
3. Search contacts
4. Update contact
5. Delete contact
6. Export to CSV
7. Exit
==================================================

Select option (1-7): 3

--- SEARCH CONTACTS ---
Search by ID, name, phone or email: jo

[1] John Doe
    Phone: 1234567890
    Email: john@example.com
```

## Features

- **Add contact**: Create contacts with a name, phone, and email
- **View all contacts**: List all stored contacts
- **Search contacts**: Find contacts by exact ID or partial name, phone, or email
- **Update contact**: Change any field, or clear the phone or email with `-`
- **Delete contact**: Remove contacts with confirmation
- **Duplicate warning**: Confirm before saving a phone or email that is already in use
- **CSV export**: Write contacts to `contacts_export.csv` for spreadsheets
- **Safe persistence**: Atomic saves and automatic backups of damaged files

## Requirements

- Python 3.12 or higher
- No external dependencies (uses the Python standard library only)

## Running the Tests

```bash
python -m unittest discover -s tests -t .
```

## Data Storage

All contacts are stored in `contacts.json` in the project root, whichever directory you run the app from. The file is created on the first save and updated after each create, update, or delete operation.

| Situation | What the app does |
|-----------|-------------------|
| A save fails | Shows the error, undoes the change, and keeps the previous file intact |
| The file is damaged | Keeps it as `contacts.json.corrupt-<timestamp>` and warns you |
| Some records are damaged | Recovers the valid ones and keeps the original as a backup |
| The file cannot be read | Shows the error and closes without touching the file |

`contacts.json`, its backups, and `contacts_export.csv` hold personal data, so they are excluded from version control.

## Documentation

Comprehensive technical documentation is available in the `/docs` folder:

- **[Requirements Specification](docs/01_requirements.md)** (Spanish) - Functional and non-functional requirements, assumptions, constraints
- **[Architecture Documentation](docs/02_architecture.md)** (Spanish) - Layered architecture explanation, layer responsibilities, dependency rules
- **[Database Documentation](docs/03_database.md)** (Spanish) - JSON persistence layer, data structure, schema, rationale
- **[Backend Documentation](docs/04_backend.md)** (Spanish) - Business logic services, validation rules, CRUD operations, tests
- **[Frontend Documentation](docs/05_frontend.md)** (Spanish) - CLI interface, menu flow, user interaction patterns

### Diagrams

- **[Architecture Diagram](docs/diagrams/architecture.png)** - Layered architecture diagram

### Wireframes

- **[Main Menu Wireframes](docs/wireframes/main_menu.txt)** - ASCII wireframes for all screens

## Project Structure

```
root/
├── app/
│   ├── configs/          # Constants and settings
│   ├── models/           # Contact data structures
│   ├── db/               # JSON persistence and CSV export
│   ├── utils/            # Pure validators and console utilities
│   ├── helpers/          # Formatting helpers
│   ├── services/         # Pure business logic (CRUD)
│   ├── interface/        # CLI menus and interactive flows
│   └── main.py           # Application entry point
├── docs/                 # Technical documentation
├── tests/                # Automated tests
├── LICENSE               # MIT license
├── requirements.txt      # Python dependencies (none)
└── README.md             # This file
```

## Architecture

![Layered architecture](docs/diagrams/architecture.png)

The application follows a **layered architecture** pattern:

1. **Configuration Layer**: Constants and paths
2. **Model Layer**: Contact creation and normalization
3. **Database Layer**: JSON persistence and CSV export
4. **Utility Layer**: Pure validators and console control
5. **Helper Layer**: Display formatting
6. **Service Layer**: Business logic that never touches the console or files
7. **Interface Layer**: User interaction and the flows that connect services with storage
8. **Application Layer**: Main loop and entry point

Each layer has a single responsibility and depends only on lower layers.

## Code Style

- No classes in the application (functional approach)
- PEP 8 compliant, with type hints
- 4-space indentation
- Maximum line length: 88 characters
- Google-style docstrings for all public functions

## Validation

- **Name**: Required, cannot be empty
- **Phone**: Optional, must contain only digits (0-9) if provided
- **Email**: Optional, must have the form `name@domain.com` if provided

## License

This project is licensed under the [MIT License](LICENSE).
