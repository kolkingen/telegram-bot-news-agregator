from datetime import datetime

from bs4 import BeautifulSoup, ResultSet, Tag
from news_source import NewsSource


class FinamCompaniesRssScrapper(NewsSource):
    """Scrapper for downloading news about companies from Finam.ru with RSS."""

    _id = "finam_companies"
    _url = "https://www.finam.ru/analysis/conews/rsspoint/"

    def _get_headline_items(self, response_text: str) -> ResultSet[Tag]:
        soup = BeautifulSoup(response_text, "xml")
        headline_items = soup.find_all("item")
        return self._filter_headline_items(headline_items)

    def _filter_headline_items(self, items: ResultSet[Tag]) -> ResultSet[Tag]:
        """Returns headlines only from autor `Finam.ru`."""
        filtered_headline_items = ResultSet(items.source)
        for item in items:
            if "Finam.ru" in item.find("a10:name").text:
                filtered_headline_items.append(item)
        return filtered_headline_items

    def _get_url(self, item: Tag) -> str:
        link = item.find("link").text
        return link.split("?")[0]

    def _get_title(self, item: Tag) -> str:
        return item.find("title").text

    def _get_time(self, item: Tag) -> datetime:
        time_string = item.find("pubDate").text
        time_format = "%a, %d %B %Y %H:%M:%S %z"
        return datetime.strptime(time_string, time_format)
