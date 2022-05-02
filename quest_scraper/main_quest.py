import re
import os
import requests
from abc import ABC
from bs4 import BeautifulSoup
from typing import Tuple, List

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



def get_main_quest_list(page_url: str) -> Tuple[List, List, List]:
    base_url = os.path.dirname(page_url)
    soup = BeautifulSoup(requests.get(page_url).content, "html.parser")
    table_tags = soup.find_all("table", class_="wikitable sortable")
    quest_names, quest_levels, quest_locations, quest_urls = [], [], [], []
    for table_tag in table_tags:
        table_rows = table_tag.find_all('tr')[1:]
        table_rows = [row.find_all('td') for row in table_rows]
        for row in table_rows:
            a_tags = row[0].find_all("a", href=True)
            quest_urls.append(base_url + a_tags[0]['href'])
            quest_names.append(row[0].text.strip())
            quest_levels.append(0 if row[1].text.strip() == "-" else int(row[1].text.strip()))
            quest_locations.append(row[2].text.strip())
    return quest_names, quest_levels, quest_locations, quest_urls
