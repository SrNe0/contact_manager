# Contact Manager CLI

A command-line contact management application built with Python using a layered architecture and JSON persistence.

## Quick Start

```bash
python -m app.main
```

## Features

- **Add contact**: Create new contacts with name, phone, and email
- **View all contacts**: List all stored contacts
- **Search contact**: Find a contact by ID
- **Update contact**: Modify existing contact information
- **Delete contact**: Remove contacts with confirmation
- **JSON Persistence**: Contacts are automatically saved to `contacts.json`

## Requirements

- Python 3.7 or higher
- No external dependencies (uses Python standard library only)

## Data Storage

All contacts are stored in `contacts.json` in the root directory.
This file is created automatically on first run and updated after each
create, update, or delete operation.

## Documentation

Comprehensive technical documentation is available in the `/docs` folder:

- **[Requirements Specification](docs/01_requirements.md)** (Spanish) - Functional and non-functional requirements, assumptions, constraints
- **[Architecture Documentation](docs/02_architecture.md)** (Spanish) - Layered architecture explanation, layer responsibilities, dependency rules
- **[Database Documentation](docs/03_database.md)** (Spanish) - JSON persistence layer, data structure, schema, rationale
- **[Backend Documentation](docs/04_backend.md)** (Spanish) - Business logic services, validation rules, CRUD operations
- **[Frontend Documentation](docs/05_frontend.md)** (Spanish) - CLI interface, menu flow, user interaction patterns

### Diagrams

- **[Architecture Diagram](docs/diagrams/architecture.png)** - Layered
architecture diagram

### Wireframes

- **[Main Menu Wireframes](docs/wireframes/main_menu.txt)** - ASCII wireframes for all screens

## Project Structure

```
root/
├── app/
│   ├── configs/          # Constants and settings
│   ├── models/           # Contact data structures
│   ├── db/               # JSON persistence layer
│   ├── interface/        # CLI user interface
│   ├── services/         # Business logic (CRUD)
│   ├── utils/            # Reusable utilities
│   ├── helpers/          # Formatting helpers
│   └── main.py           # Application entry point
├── docs/                 # Technical documentation
├── contacts.json         # Data file (auto-created)
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Architecture

The application follows a **layered architecture** pattern:

1. **Configuration Layer**: Constants and settings
2. **Model Layer**: Data structure definitions
3. **Database Layer**: JSON file persistence
4. **Utility Layer**: Console operations and validators
5. **Helper Layer**: Display formatting
6. **Interface Layer**: User interaction and I/O
7. **Service Layer**: Business logic and CRUD operations
8. **Application Layer**: Main loop and entry point

Each layer has a single responsibility and depends only on lower layers.

## Code Style

- No classes (functional programming approach)
- PEP 8 compliant
- 4-space indentation
- Maximum line length: 88 characters
- Comprehensive docstrings for all public functions

## Validation

- **Name**: Required, cannot be empty
- **Phone**: Optional, must contain only digits (0-9) if provided
- **Email**: Optional, no format validation

## License

This project is provided as-is for educational purposes.
