import re
import os
import requests
from typing import Tuple
from bs4 import BeautifulSoup

from .section_scraper import SectionScraper


def get_secondary_quest_list(page_url: str) -> Tuple:
    base_url = os.path.dirname(os.path.dirname(page_url))
    soup = BeautifulSoup(requests.get(page_url).content, "html.parser")
    table_tags = soup.find_all("table")
    quest_names, quest_urls, is_unmarked, cutoff_point, levels, locations, enemies = (
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    )
    for table_tag in table_tags:
        table_rows = table_tag.find_all("tr")[1:]
        table_rows = [row.find_all("td") for row in table_rows]
        for row in table_rows:
            quest_names.append(row[0].text.strip())
            quest_urls.append(base_url + row[0].find_all("a", href=True)[0]["href"])
            is_unmarked.append("Yes" in row[1].text.strip())
            cutoff_point.append(row[2].text.strip())
            levels.append(row[3].text.strip())
            locations.append(re.sub(r"(\w)([A-Z])", r"\1\n\2", row[4].text).strip().split("\n"))
            enemies.append(re.sub(r"(\w)([A-Z])", r"\1\n\2", row[4].text).strip().split("\n"))
            # locations.append(re.split(r"(\w)([A-Z])", row[4].text.strip()))
            # enemies.append(re.split(r"(\w)([A-Z])", row[5].text.strip()))
    return (
        quest_names,
        quest_urls,
        is_unmarked,
        cutoff_point,
        levels,
        locations,
        enemies,
    )
