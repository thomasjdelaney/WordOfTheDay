# Word of the Day

A Python application that scrapes the word of the day from the Oxford English Dictionary website, gathers information about the word, and presents it in a concise and readable form.

## Configuration

1. Copy the environment template:
```bash
cp .env.template .env
```

2. Edit `.env` with your email settings:
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-specific-password  # For Gmail, use App Password
RECIPIENT_LIST=recipient1@example.com,recipient2@example.com
```

Note for Gmail users:
- Enable 2-factor authentication in your Google Account
- Generate an App Password under Security settings
- Use the App Password in your .env file

## GitHub Actions Setup

To run the script automatically every day:

1. Go to your repository Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `SMTP_SERVER` (e.g., smtp.gmail.com)
   - `SMTP_PORT` (e.g., 587)
   - `SENDER_EMAIL` (your email address)
   - `SENDER_PASSWORD` (your app password)
   - `RECIPIENT_LIST` (comma-separated email addresses)

The workflow will run daily at 06:00 UTC. You can adjust the schedule by modifying the cron expression in `.github/workflows/daily-word.yml`.

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