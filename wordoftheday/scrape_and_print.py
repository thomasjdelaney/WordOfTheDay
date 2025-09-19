"""Module for scraping the Oxford English Dictionary word of the day."""

import logging

from wordoftheday import PROJECT_ROOT
from wordoftheday.scraping_functions import fetch_url, get_word_of_the_day_url
from wordoftheday.word_entry import WordEntry


def main() -> None:
    """Main function to fetch and print the word of the day."""
    wotd_url = get_word_of_the_day_url()
    if not wotd_url:
        logging.error("No word of the day URL found.")
        return

    try:
        wotd_html = fetch_url(url=wotd_url)
        word_entry = WordEntry.from_html(wotd_html)
        word_entry.print_summary()
        with open(
            PROJECT_ROOT / "wordoftheday" / "files" / f"wotd_response_{word_entry.word}.html", "w", encoding="utf-8"
        ) as file:
            file.write(wotd_html)
    except Exception as e:
        logging.exception("Failed to fetch or parse the word of the day.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
