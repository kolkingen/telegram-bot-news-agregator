from datetime import datetime

from bs4 import BeautifulSoup, ResultSet, Tag

from news_getter import NewsGetter
from table_models import NewsSource


class RiaRssScrapper(NewsGetter):
    """Scrapper for downloading news from RIA Novosti with RSS."""

    def _create_source(self) -> NewsSource:
        return NewsSource(
            'ria', 'РИА Новости', 
            'https://ria.ru/export/rss2/archive/index.xml')

    def _get_headline_items(self, response_text: str) -> ResultSet[Tag]:
        soup = BeautifulSoup(response_text, "xml")
        return soup.find_all("item")

    def _get_link(self, item: Tag) -> str:
        return item.find("guid").text

    def _get_title(self, item: Tag) -> str:
        return item.find("title").text

    def _get_time(self, item: Tag) -> datetime:
        time_string = item.find("pubDate").text
        time_format = "%a, %d %B %Y %H:%M:%S %z"
        return datetime.strptime(time_string, time_format)
