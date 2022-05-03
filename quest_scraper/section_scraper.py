import requests
from typing import List
from bs4 import BeautifulSoup, element


class SectionScraper:
    def __init__(self, soup: BeautifulSoup) -> None:
        super().__init__()
        self.soup = soup

    def scrape_p(self, content: element.Tag) -> str:
        return content.text.strip()

    def scrape_ul(self, content: element.Tag) -> str:
        list_md = ""
        for _item in list(content.children):
            if _item != "\n":
                list_md += f"\n* {_item.text}"
        return list_md + "\n"

    def scrape_section(
        self, section_id: str, includes: List[str], break_tag: str
    ) -> str:
        section_start = self.soup.find(id=section_id).parent
        section_content = section_start.find_next_siblings()
        required_content = []
        for content in section_content:
            if content.name in includes:
                if content.name == "p" or content.name == "dl":
                    md = self.scrape_p(content)
                    required_content.append(md)
                if content.name == "ul":
                    md = self.scrape_ul(content)
                    required_content.append(md)
            elif content.name == break_tag:
                break
        return "\n".join(required_content).strip()
