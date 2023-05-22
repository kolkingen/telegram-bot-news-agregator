from datetime import datetime

import requests
from bs4 import BeautifulSoup, ResultSet, Tag

from news_getter import NewsGetter
from table_models import NewsSource


class InvestingComScrapper(NewsGetter):
    """Scrapper for loading news from ru.investing.com"""

    def _create_source(self) -> NewsSource:
        return NewsSource('investing', 'Investing.com', 'https://ru.investing.com/news/headlines')

    def _get_headline_items(self, response_text: str) -> ResultSet[Tag]:
        soup = BeautifulSoup(response_text, "lxml")
        articles_div = soup.find(name="div", class_="largeTitle")
        article_class = "js-article-item articleItem onlyHeadlines"
        return articles_div.find_all("article", class_=article_class)

    def _get_link(self, item: Tag) -> str:
        relative_link = item.find("a", href=True, class_="title")["href"]
        return "https://ru.investing.com" + relative_link

    def _get_title(self, item: Tag) -> str:
        return item.find("a", class_="title").text

    def _get_time(self, item: Tag) -> datetime:
        # Release time is on the news' web page
        page_html_text = self._get_headline_page(item)
        time_string = self._get_time_string(page_html_text)
        time_string = time_string[13:] + " +0300"  # add timezone
        time_format = "%d.%m.%Y %H:%M %z"
        return datetime.strptime(time_string, time_format)

    def _get_headline_page(self, item: Tag) -> str:
        link = self._get_link(item)
        response = requests.get(link, timeout=5)
        response.raise_for_status()
        return response.text

    def _get_time_string(self, html_text: str) -> str:
        soup = BeautifulSoup(html_text, "lxml")
        headline_details = soup.find_all(name="div", class_="contentSectionDetails")
        for detail in headline_details:
            if "Опубликовано" in detail.text:
                return detail.text.strip()
