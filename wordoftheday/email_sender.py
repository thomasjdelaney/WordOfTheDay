"""Module for formatting and sending Word of the Day emails."""

import logging
import smtplib
from dataclasses import dataclass
from email.mime.text import MIMEText
from typing import List

from wordoftheday.etymology_entry import EtymologyEntry
from wordoftheday.word_entry import WordEntry


@dataclass
class EmailConfig:
    """Configuration for email sending."""

    smtp_server: str
    smtp_port: int
    sender_email: str
    sender_password: str
    recipient_list: List[str]


def format_word_entry_email(word_entry: WordEntry, etymology_entry: EtymologyEntry) -> str:
    """Format a WordEntry into a concise email body.

    Args:
        word_entry: The WordEntry object containing word information
        etymology_entry: The EtymologyEntry object containing etymology information

    Returns:
        str: Formatted email body
    """
    email_body = [
        f"Word of the Day: {word_entry.word}",
        "",
        "DEFINITIONS:",
    ]

    for defn in word_entry.definitions:
        email_body.append(f"\n{defn.sense_number} {defn.definition_text}")
        if defn.examples:
            email_body.append("\nExamples:")
            for date, quote, cite in defn.examples:
                email_body.append(f"({date}):")
                email_body.append(f'"{quote}"')
                email_body.append(f"- {cite}\n")

    email_body.append(etymology_entry.format_for_email())
    return "\n".join(email_body)


def send_word_email(word_entry: WordEntry, etymology_entry: EtymologyEntry, config: EmailConfig) -> None:
    """Send formatted Word of the Day email.

    Args:
        word_entry: The WordEntry object containing word information
        etymology_entry: The EtymologyEntry object containing etymology information
        config: Email configuration settings

    Raises:
        smtplib.SMTPException: If email sending fails
    """
    email_body = format_word_entry_email(word_entry=word_entry, etymology_entry=etymology_entry)

    msg = MIMEText(email_body)
    msg["Subject"] = f"Word of the Day: {word_entry.word}"
    msg["From"] = config.sender_email
    msg["To"] = ", ".join(config.recipient_list)

    try:
        with smtplib.SMTP(config.smtp_server, config.smtp_port) as server:
            server.starttls()
            server.login(config.sender_email, config.sender_password)
            server.send_message(msg)
    except smtplib.SMTPException:
        logging.exception("Failed to send Word of the Day email")
        raise
