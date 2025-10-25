"""Tests for word_entry module."""

import pytest

from wordoftheday.word_entry import WordEntry


@pytest.fixture
def sample_html() -> str:
    """Returns sample HTML for testing.

    Returns:
        str: Sample HTML content for word definition page
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
            <section id="meaning_and_use">
                <div class="tab-content">
                    <div class="tab-content-body">
                        <div id="meanings">
                            <ol class="s4-list">
                                <li class="item sense">
                                    <div class="item-enumerator">1.</div>
                                    <div class="definition">A type of artillery shell</div>
                                    <div class="daterange-container">1806-</div>
                                    <div class="tags">
                                        <a class="tag">military</a>
                                        <a class="tag">historical</a>
                                    </div>
                                    <ol class="quotation-container">
                                        <li class="quotation">
                                            <div class="quotation-date">1806</div>
                                            <blockquote class="quotation-text">The shells burst with great effect.</blockquote>
                                            <cite class="citation-text">Military Journal</cite>
                                        </li>
                                    </ol>
                                </li>
                            </ol>
                        </div>
                    </div>
                </div>
            </section>
        </body>
    </html>
    """


def test_word_entry_creation(sample_html: str) -> None:
    """Test creating WordEntry from HTML.

    Args:
        sample_html: Fixture providing sample HTML content
    """
    entry = WordEntry.from_html(sample_html)

    assert entry.word == "shrapnel"
    assert len(entry.definitions) == 1

    definition = entry.definitions[0]
    assert definition.sense_number == "1."
    assert definition.definition_text == "A type of artillery shell"
    assert definition.date_range == ("1806", "")
    assert definition.subject_tags == ["military", "historical"]
    assert len(definition.examples) == 1

    date, quote, cite = definition.examples[0]
    assert date == "1806"
    assert quote == "The shells burst with great effect."
    assert cite == "Military Journal"


def test_word_entry_missing_sections() -> None:
    """Test handling of HTML with missing sections."""
    minimal_html = """
        <html>
            <h1 class="headword-group">
                <span class="headword">test</span>
            </h1>
            <section id="meaning_and_use">
                <div class="tab-content">
                    <div class="tab-content-body">
                        <div id="meanings">
                            <ol class="s4-list">
                                <li class="item sense">
                                    <div class="definition">A simple test</div>
                                </li>
                            </ol>
                        </div>
                    </div>
                </div>
            </section>
        </html>
        """

    entry = WordEntry.from_html(minimal_html)
    assert entry.word == "test"
    assert len(entry.definitions) == 1
    assert entry.definitions[0].definition_text == "A simple test"


def test_word_entry_invalid_html() -> None:
    """Test handling of invalid HTML."""
    with pytest.raises(ValueError):
        WordEntry.from_html("<html></html>")


def test_definition_without_examples() -> None:
    """Test handling definition without examples."""
    html = """
        <html>
            <h1 class="headword-group">
                <span class="headword">test</span>
            </h1>
            <section id="meaning_and_use">
                <div class="tab-content">
                    <div class="tab-content-body">
                        <div id="meanings">
                            <ol class="s4-list">
                                <li class="item sense">
                                    <div class="item-enumerator">1.</div>
                                    <div class="definition">A definition without examples</div>
                                </li>
                            </ol>
                        </div>
                    </div>
                </div>
            </section>
        </html>
        """

    entry = WordEntry.from_html(html)
    assert len(entry.definitions) == 1
    assert entry.definitions[0].examples == []
