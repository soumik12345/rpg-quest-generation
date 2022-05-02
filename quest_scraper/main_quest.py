import re
import requests
from abc import ABC
from bs4 import BeautifulSoup

from .section_scraper import SectionScraper


class MainQuestScraper(ABC):
    def __init__(self, quest_url) -> None:
        super().__init__()
        self.soup = BeautifulSoup(requests.get(quest_url).content, "html.parser")

    def scrape_title(self) -> str:
        title = str(self.soup.find(property="og:title"))
        return re.findall(r"content=\"([\w\d\s()]+)\"", title)[0]

    def scrape_walkthrough(self) -> str:
        walkthrough_scraper = SectionScraper(self.soup)
        return walkthrough_scraper.scrape_section(
            section_id="Walkthrough", includes=["p", "ul"], break_tag="h2"
        )
    
    def scrape_journal_entry(self) -> str:
        journal_entry_scraper = SectionScraper(self.soup)
        return journal_entry_scraper.scrape_section(
            section_id="Journal_Entry", includes=["p", "ul", "dl"], break_tag="h2"
        )
    
    def scrape_objectives(self) -> str:
        objectives_scraper = SectionScraper(self.soup)
        return objectives_scraper.scrape_section(
            section_id="Objectives", includes=["p", "ul"], break_tag="h2"
        )
