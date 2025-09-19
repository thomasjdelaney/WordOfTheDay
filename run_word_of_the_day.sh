#!/bin/bash

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please copy .env.template to .env and fill in your values."
    exit 1
fi

# Load environment variables from .env file
export $(cat .env | grep -v '^#' | xargs)

# Activate poetry environment and run the script
poetry run python -m wordoftheday.scrape_and_print

# Unset environment variables for security
unset SMTP_SERVER
unset SMTP_PORT
unset SENDER_EMAIL
unset SENDER_PASSWORD
unset RECIPIENT_LIST