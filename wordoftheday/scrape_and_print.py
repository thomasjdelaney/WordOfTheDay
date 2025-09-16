"""Module for scraping the Oxford English Dictionary word of the day."""

import logging

import requests

from wordoftheday import PROJECT_ROOT
from wordoftheday.word_entry import WordEntry

OED_HOMEPAGE = "https://www.oed.com/"


def fetch_url(url: str) -> str:
    """Fetches the OED homepage content.

    Returns:
        str: The HTML content of the OED homepage.

    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    request_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        response = requests.get(url=url, headers=request_header)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.exception(f"Failed to fetch URL: {url}")
        raise
    return response.text


def extract_wotd_href(html: str) -> str:
    """Extracts the word of the day URL from the OED homepage HTML.

    Args:
        html: The HTML content of the OED homepage.

    Returns:
        str: The URL path for the word of the day.

    Raises:s
        ValueError: If the required markers are not found in the HTML.
    """

    def extract_between(text: str, start: str, end: str, error_msg: str) -> str:
        """Helper function to extract content between two markers.

        Args:
            text: The text to search in.
            start: The starting marker.
            end: The ending marker.
            error_msg: Error message if markers aren't found.

        Returns:
            str: The extracted content between markers.

        Raises:
            ValueError: If either marker is not found.
        """
        start_idx = text.find(start)
        if start_idx == -1:
            raise ValueError(error_msg)

        content_start = start_idx + len(start)
        end_idx = text.find(end, content_start)
        if end_idx == -1:
            raise ValueError(error_msg)

        return text[content_start:end_idx]

    try:
        # Extract the WOTD div content
        div_content = extract_between(html, '<div class="wotd">', "</div>", "WOTD section not found").strip()

        # Extract the href attribute
        href = extract_between(div_content, '<a href="', '"', "WOTD link not found")
    except ValueError as e:
        logging.exception("Failed to extract word of the day URL")
        href = ""
    return href


def get_word_of_the_day_url() -> str:
    """Gets the full URL for the word of the day.

    Returns:
        str: The full URL for the word of the day, or an empty string if not found.
    """
    wotd_url = ""
    try:
        homepage_html = fetch_url(url=OED_HOMEPAGE)
        wotd_path = extract_wotd_href(homepage_html)
        if wotd_path:
            wotd_url = f"{OED_HOMEPAGE.rstrip('/')}{wotd_path}"
    except Exception as e:
        logging.exception("Failed to get word of the day URL")
    return wotd_url


def main():
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
