"""Module for parsing Oxford English Dictionary etymology sections."""

from dataclasses import dataclass

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag


@dataclass
class EtymologyEntry:
    """Represents the etymology section of a word entry."""

    etymology_summary: str  # e.g., "A borrowing from Spanish."
    etymons: list[tuple[str, str]]  # list of (language, word form) tuples
    full_etymology: str  # complete etymology text with all details

    @staticmethod
    def _extract_etymons(summary_div: Tag) -> list[tuple[str, str]]:
        """Extract etymon language and word form pairs from the summary div.

        Args:
            summary_div: The etymology summary HTML section containing etymon information

        Returns:
            List of (language, word form) tuples
        """
        etymons = []
        etymon_element = None

        for element in summary_div.find_all(string=True):
            if isinstance(element, NavigableString) and "Etymon" in str(element):
                etymon_element = element.parent
                break

        if etymon_element and isinstance(etymon_element, Tag):
            languages = etymon_element.find_all("span", {"class": "language-name"})
            forms = etymon_element.find_all("span", {"class": "foreign-form"})

            etymons = [
                (lang.get_text(strip=True), form.get_text(strip=True))
                for lang, form in zip(languages, forms)
                if isinstance(lang, Tag) and isinstance(form, Tag)
            ]

        return etymons

    @classmethod
    def from_html(cls, html_content: str) -> "EtymologyEntry":
        """Create an EtymologyEntry instance from OED HTML content.

        Args:
            html_content: HTML content from OED etymology section

        Returns:
            EtymologyEntry instance containing etymology information

        Raises:
            ValueError: If required content cannot be found
        """
        soup = BeautifulSoup(html_content, "html.parser")

        # Get etymology section
        etymology_section = soup.find("section", attrs={"id": "etymology"})
        if not etymology_section or not isinstance(etymology_section, Tag):
            raise ValueError("Could not find etymology section")

        # Get summary
        etymology_summary_div = etymology_section.find("div", attrs={"class": "etymology-summary"})
        if not etymology_summary_div or not isinstance(etymology_summary_div, Tag):
            raise ValueError("Could not find etymology summary")

        # Get the summary text (first div after header)
        summary_text_div = etymology_summary_div.find("div")
        if not summary_text_div or not isinstance(summary_text_div, Tag):
            raise ValueError("Could not find etymology summary text")

        etymology_summary = summary_text_div.get_text(strip=True)

        # Get etymons from summary section
        etymons = cls._extract_etymons(summary_div=etymology_summary_div)

        # Get full etymology
        etymology_div = etymology_section.find("div", attrs={"id": "main_etymology_complete"})
        if not etymology_div or not isinstance(etymology_div, Tag):
            raise ValueError("Could not find main etymology")

        full_etymology = etymology_div.get_text(separator=" ", strip=True)

        # Remove "Show less" button text if present
        if full_etymology.endswith("Show less"):
            full_etymology = full_etymology[: -len("Show less")].strip()

        return cls(etymology_summary=etymology_summary, etymons=etymons, full_etymology=full_etymology)

    def print_summary(self) -> None:
        """Print a formatted summary of the etymology entry."""
        print("ETYMOLOGY SUMMARY:")
        print(self.etymology_summary)

        if self.etymons:
            print("\nETYMONS:")
            for language, word_form in self.etymons:
                print(f"{language}: {word_form}")

        print("\nFULL ETYMOLOGY:")
        print(self.full_etymology)

    def format_for_email(self) -> str:
        """Format the etymology entry for email inclusion.

        Returns:
            str: Formatted etymology text for email
        """
        email_str = f"ETYMOLOGY SUMMARY:\n{self.etymology_summary}"
        if self.etymons:
            email_str += "ETYMONS:\n"
            for language, word_form in self.etymons:
                email_str += f"{language}: {word_form}\n"
            email_str += "\n"

        email_str += f"FULL ETYMOLOGY:\n{self.full_etymology}\n"
        return email_str
