"""Module for parsing Oxford English Dictionary HTML responses."""

from dataclasses import dataclass
from typing import Optional, cast

from bs4 import BeautifulSoup, Tag


@dataclass
class Definition:
    """Represents a single definition with its examples and metadata."""

    sense_number: str  # e.g., "1.", "1.a.", "2.", etc.
    definition_text: str
    date_range: Optional[tuple[str, str]]  # e.g., ("1806", "")
    examples: list[tuple[str, str, str]]  # list of (date, quote, citation)
    subject_tags: list[str]  # e.g., ["weaponry", "historical"]


@dataclass
class WordEntry:
    """Represents a complete dictionary entry for a word."""

    word: str
    etymology: str
    definitions: list[Definition]

    @staticmethod
    def _format_etymology_section(etymology_section: Tag) -> str:
        """Formats the etymology section for display."""
        if etymology_section:
            etymology_div = etymology_section.find("div", class_="etymology")
            etymology = etymology_div.text.strip() if etymology_div else ""
            # if the etymology ends in the string 'Show Less', remove it
            if etymology.endswith("Show less"):
                etymology = etymology[: -len("Show less")].strip()
            if etymology.startswith("< "):
                etymology = etymology[2:].strip()
        else:
            etymology = ""
        return etymology

    @staticmethod
    def _get_definition_from_sense(sense: Tag) -> Optional[Definition]:
        """Extracts a Definition object from a sense Tag. Returns None if not possible."""
        # Get sense number
        sense_num_div = sense.find("div", class_="item-enumerator")
        sense_num = sense_num_div.text.strip() if sense_num_div else ""

        # Get definition text
        def_div = sense.find("div", class_="definition")
        if not def_div:
            return None
        def_text = def_div.text.strip() if def_div else ""

        # Get date range
        date_div = sense.find("div", class_="daterange-container")
        date_range = None
        if date_div:
            dates = date_div.text.strip().replace("–", "-").split("-")
            date_range = (dates[0], dates[1] if len(dates) > 1 else "")

        # Get examples
        examples = []
        quotations = sense.find_all("li", class_="quotation")
        for quote in quotations:
            quote = cast(Tag, quote)
            date = cast(Tag, quote.find("div", class_="quotation-date"))
            text = cast(Tag, quote.find("blockquote", class_="quotation-text"))
            citation = cast(Tag, quote.find("cite", class_="citation-text"))
            if all([date, text, citation]):
                examples.append((date.text.strip(), text.text.strip(), citation.text.strip()))
        # Get subject tags
        tags_div = cast(Tag, sense.find("div", class_="tags"))
        tags = []
        if tags_div:
            tags = [tag.text.strip() for tag in tags_div.find_all("a", class_="tag")]
        return Definition(
            sense_number=sense_num,
            definition_text=def_text,
            date_range=date_range,
            examples=examples,
            subject_tags=tags,
        )

    @classmethod
    def from_html(cls, html_content: str) -> "WordEntry":
        """Create a WordEntry instance from OED HTML content.

        Args:
            html_content: HTML content from OED page

        Returns:
            WordEntry instance containing word information

        Raises:
            ValueError: If required content cannot be found
        """
        soup = BeautifulSoup(html_content, "html.parser")

        # Get the word - handle both possible formats
        word_elem = soup.select_one("h1.headword-group .headword")
        if not word_elem:
            raise ValueError("Could not find headword")
        word = word_elem.text.strip()
        # remove any characters in word that are not in the alphabet, hyphen, or apostrophe
        word = "".join(c for c in word if c.isalpha() or c in ("-", "'"))

        # Get etymology - handle both formats
        etymology_section = cast(Tag, soup.find("section", id="etymology"))
        etymology = cls._format_etymology_section(etymology_section=etymology_section)

        # Get definitions
        definitions = []
        meaning_section = soup.find("section", id="meaning_and_use")
        if not meaning_section:
            raise ValueError("Could not find meanings section")

        sense_items = meaning_section.find_all("li", class_=["item", "sense"])  # type: ignore

        for sense in sense_items:
            definition = cls._get_definition_from_sense(cast(Tag, sense))
            if definition:
                definitions.append(definition)
        return cls(word=word, etymology=etymology, definitions=definitions)

    def print_summary(self) -> None:
        """Print a formatted summary of the word entry."""
        print(f"Word: {self.word}")
        print("\nETYMOLOGY:")
        print(self.etymology)
        print("\nDEFINITIONS:")

        for defn in self.definitions:
            print(f"\n{defn.sense_number} ", end="")
            if defn.date_range:
                print(f"[{defn.date_range[0]}-{defn.date_range[1]}]")
            print(defn.definition_text)

            if defn.subject_tags:
                print("Tags:", ", ".join(defn.subject_tags))

            if defn.examples:
                print("First recorded use:")
                date, quote, cite = defn.examples[0]
                print(f"  {date}: {quote}")
                print(f"  - {cite}")
