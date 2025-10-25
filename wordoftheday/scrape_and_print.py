"""Module for scraping and emailing the Oxford English Dictionary word of the day."""

import logging
import os

from wordoftheday import PROJECT_ROOT
from wordoftheday.email_sender import EmailConfig, send_word_email
from wordoftheday.etymology_entry import EtymologyEntry
from wordoftheday.scraping_functions import fetch_url, get_word_of_the_day_url
from wordoftheday.word_entry import WordEntry


def main() -> None:
    """Main function to fetch word of the day and send email."""
    try:
        # Get email configuration from environment variables
        email_config = EmailConfig(
            smtp_server=os.environ["SMTP_SERVER"],
            smtp_port=int(os.environ["SMTP_PORT"]),
            sender_email=os.environ["SENDER_EMAIL"],
            sender_password=os.environ["SENDER_PASSWORD"],
            recipient_list=os.environ["RECIPIENT_LIST"].split(","),
        )

        # Fetch and parse word of the day
        wotd_url = get_word_of_the_day_url()
        if not wotd_url:
            logging.error("No word of the day URL found.")
            return

        etymology_url = f"{wotd_url}?tab=etymology"
        etymology_html = fetch_url(url=etymology_url)
        etymology_entry = EtymologyEntry.from_html(html_content=etymology_html)
        wotd_html = fetch_url(url=wotd_url)
        word_entry = WordEntry.from_html(html_content=wotd_html)
        word_entry.print_summary()

        # Save HTML response
        with open(
            PROJECT_ROOT / "wordoftheday" / "files" / f"wotd_response_{word_entry.word}.html", "w", encoding="utf-8"
        ) as file:
            file.write(wotd_html)

        # Send email
        send_word_email(word_entry=word_entry, etymology_entry=etymology_entry, config=email_config)
        logging.info(f"Successfully sent Word of the Day email for: {word_entry.word}")

    except Exception:
        logging.exception("Failed to process word of the day")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
