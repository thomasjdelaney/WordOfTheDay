"""Tests for email_sender module."""

import smtplib
from unittest.mock import Mock, patch

import pytest

from wordoftheday.email_sender import (
    EmailConfig,
    format_word_entry_email,
    send_word_email,
)
from wordoftheday.word_entry import Definition, WordEntry


@pytest.fixture
def sample_word_entry() -> WordEntry:
    """Create a sample WordEntry for testing.

    Returns:
        WordEntry: A sample word entry
    """
    return WordEntry(
        word="test",
        etymology="From Latin testum",
        definitions=[
            Definition(
                sense_number="1.",
                definition_text="A sample definition",
                date_range=("1500", ""),
                examples=[("1500", "A test quote", "Test Author")],
                subject_tags=["testing"],
            )
        ],
    )


@pytest.fixture
def email_config() -> EmailConfig:
    """Create a sample EmailConfig for testing.

    Returns:
        EmailConfig: A sample email configuration
    """
    return EmailConfig(
        smtp_server="smtp.test.com",
        smtp_port=587,
        sender_email="sender@test.com",
        sender_password="password123",
        recipient_list=["recipient@test.com"],
    )


def test_format_word_entry_email(sample_word_entry: WordEntry) -> None:
    """Test email formatting.

    Args:
        sample_word_entry: Fixture providing a sample WordEntry
    """
    email_body = format_word_entry_email(sample_word_entry)

    assert "Word of the Day: test" in email_body
    assert "From Latin testum" in email_body
    assert "1. A sample definition" in email_body
    assert "First recorded use (1500):" in email_body
    assert '"A test quote"' in email_body
    assert "- Test Author" in email_body


@patch("smtplib.SMTP")
def test_send_word_email(mock_smtp: Mock, sample_word_entry: WordEntry, email_config: EmailConfig) -> None:
    """Test email sending functionality.

    Args:
        mock_smtp: Mock SMTP server
        sample_word_entry: Fixture providing a sample WordEntry
        email_config: Fixture providing email configuration
    """
    send_word_email(sample_word_entry, email_config)

    mock_smtp.assert_called_once_with(email_config.smtp_server, email_config.smtp_port)
    mock_smtp_instance = mock_smtp.return_value.__enter__.return_value

    mock_smtp_instance.starttls.assert_called_once()
    mock_smtp_instance.login.assert_called_once_with(email_config.sender_email, email_config.sender_password)
    mock_smtp_instance.send_message.assert_called_once()


@patch("smtplib.SMTP")
def test_send_word_email_handles_error(
    mock_smtp: Mock, sample_word_entry: WordEntry, email_config: EmailConfig
) -> None:
    """Test email sending error handling.

    Args:
        mock_smtp: Mock SMTP server
        sample_word_entry: Fixture providing a sample WordEntry
        email_config: Fixture providing email configuration
    """
    mock_smtp.return_value.__enter__.return_value.send_message.side_effect = smtplib.SMTPException

    with pytest.raises(smtplib.SMTPException):
        send_word_email(sample_word_entry, email_config)
