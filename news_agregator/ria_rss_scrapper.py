from datetime import datetime

from bs4 import BeautifulSoup, ResultSet, Tag
from news_source import NewsSource


class RiaRssScrapper(NewsSource):
    """Scrapper for downloading news from RIA Novosti with RSS."""

    _id = "ria"
    _url = "https://ria.ru/export/rss2/archive/index.xml"

    def _get_headline_items(self, response_text: str) -> ResultSet[Tag]:
        soup = BeautifulSoup(response_text, "xml")
        return soup.find_all("item")

    def _get_url(self, item: Tag) -> str:
        return item.find("guid").text

    def _get_title(self, item: Tag) -> str:
        return item.find("title").text

    def _get_time(self, item: Tag) -> datetime:
        time_string = item.find("pubDate").text
        time_format = "%a, %d %B %Y %H:%M:%S %z"
        return datetime.strptime(time_string, time_format)
