"""Module for parsing Oxford English Dictionary HTML responses."""

from dataclasses import dataclass
from typing import List, Optional

from bs4 import BeautifulSoup


@dataclass
class Definition:
    """Represents a single definition with its examples and metadata."""

    sense_number: str  # e.g., "1.", "1.a.", "2.", etc.
    definition_text: str
    date_range: Optional[tuple[str, str]]  # e.g., ("1806", "")
    examples: List[tuple[str, str, str]]  # List of (date, quote, citation)
    subject_tags: List[str]  # e.g., ["weaponry", "historical"]


@dataclass
class WordEntry:
    """Represents a complete dictionary entry for a word."""

    word: str
    etymology: str
    definitions: List[Definition]

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

        # Get etymology - handle both formats
        etymology_section = soup.find("section", id="etymology")
        if etymology_section:
            etymology_div = etymology_section.find("div", class_="etymology")
            etymology = etymology_div.text.strip() if etymology_div else ""
        else:
            etymology = ""

        # Get definitions
        definitions = []
        meaning_section = soup.find("section", id="meaning_and_use")
        if not meaning_section:
            raise ValueError("Could not find meanings section")

        sense_items = meaning_section.find_all("li", class_=["item", "sense"])

        for sense in sense_items:
            # Skip if this is just a container for subsenses
            def_div = sense.find("div", class_="definition")
            if not def_div:
                continue

            # Get sense number
            sense_num_div = sense.find("div", class_="item-enumerator")
            sense_num = sense_num_div.text.strip() if sense_num_div else ""

            # Get definition text
            def_text = def_div.text.strip()

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
                date = quote.find("div", class_="quotation-date")
                text = quote.find("blockquote", class_="quotation-text")
                citation = quote.find("cite", class_="citation-text")

                if all([date, text, citation]):
                    examples.append((date.text.strip(), text.text.strip(), citation.text.strip()))

            # Get subject tags
            tags_div = sense.find("div", class_="tags")
            tags = []
            if tags_div:
                tags = [tag.text.strip() for tag in tags_div.find_all("a", class_="tag")]

            definitions.append(
                Definition(
                    sense_number=sense_num,
                    definition_text=def_text,
                    date_range=date_range,
                    examples=examples,
                    subject_tags=tags,
                )
            )

        return cls(word=word, etymology=etymology, definitions=definitions)

    def print_summary(self):
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
