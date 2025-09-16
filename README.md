# Word of the Day

A Python application that scrapes the word of the day from the Oxford English Dictionary website, gathers information about the word, and presents it in a concise and readable form.

## Features

- Scrapes the Oxford English Dictionary website for the word of the day
- Gathers detailed information about each word
- Presents information in a clean, readable format

## Installation

This project uses Poetry for dependency management. To get started:

1. Clone the repository:
```bash
git clone https://github.com/yourusername/WordOfTheDay.git
cd WordOfTheDay
```

2. Install Poetry if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Install dependencies:
```bash
poetry install
```

## Requirements

- Python 3.12 or higher
- Poetry for dependency management

## Development

This project uses several development tools:

- `black` for code formatting
- `isort` for import sorting
- `mypy` for static type checking

To run the development tools:

```bash
# Format code
poetry run black .

# Sort imports
poetry run isort .

# Type checking
poetry run mypy .
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.