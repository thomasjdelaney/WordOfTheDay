"""Tests for scraping_functions module."""

import pytest
import requests
import responses

from wordoftheday.scraping_functions import fetch_url, get_word_of_the_day_url


@pytest.fixture
def mock_oed_homepage() -> str:
    """Returns mock OED homepage HTML content.

    Returns:
        str: Mock HTML content containing a word of the day link
    """
    return """
    <html>
        <body>
            <div class="wotd">
                <a href="/word-of-the-day/shrapnel">Word of the Day: shrapnel</a>
            </div>
        </body>
    </html>
    """


@pytest.fixture
def mock_wotd_response() -> str:
    """Returns mock word of the day page HTML content.

    Returns:
        str: Mock HTML content for a word definition page
    """
    return """
    <html>
        <body>
            <h1 class="headword-group">
                <span class="headword">shrapnel</span>
            </h1>
            <section id="etymology">
                <div class="etymology">From Henry Shrapnel (1761-1842)</div>
            </section>
        </body>
    </html>
    """


@responses.activate
def test_fetch_url(mock_wotd_response: str) -> None:
    """Test fetching URL content.

    Args:
        mock_wotd_response: Fixture providing mock HTML content
    """
    url = "https://www.oed.com/word-of-the-day/shrapnel"
    responses.add(responses.GET, url, body=mock_wotd_response, status=200)

    response = fetch_url(url)
    assert response == mock_wotd_response


@responses.activate
def test_fetch_url_handles_error() -> None:
    """Test fetch_url error handling."""
    url = "https://www.oed.com/invalid"
    responses.add(responses.GET, url, status=404)

    with pytest.raises(requests.RequestException):
        fetch_url(url)


@responses.activate
def test_get_word_of_the_day_url(mock_oed_homepage: str) -> None:
    """Test extracting word of the day URL.

    Args:
        mock_oed_homepage: Fixture providing mock homepage HTML
    """
    responses.add(responses.GET, "https://www.oed.com/", body=mock_oed_homepage, status=200)

    url = get_word_of_the_day_url()
    assert url == "https://www.oed.com/word-of-the-day/shrapnel"


@responses.activate
def test_get_word_of_the_day_url_no_word() -> None:
    """Test handling when no word of the day is found."""
    responses.add(responses.GET, "https://www.oed.com/", body="<html></html>", status=200)

    url = get_word_of_the_day_url()
    assert url is None
