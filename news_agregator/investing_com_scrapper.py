from datetime import datetime

import requests
from bs4 import BeautifulSoup, ResultSet, Tag
from news_source import NewsSource


class InvestingComScrapper(NewsSource):
    """Scrapper for loading news from ru.investing.com"""

    _id = "investing"
    _url = "https://ru.investing.com/news/headlines"

    def _get_headline_items(self, response_text: str) -> ResultSet[Tag]:
        soup = BeautifulSoup(response_text, "lxml")
        articles_div = soup.find(name="div", class_="largeTitle")
        article_class = "js-article-item articleItem onlyHeadlines"
        return articles_div.find_all("article", class_=article_class)

    def _get_url(self, item: Tag) -> str:
        relative_url = item.find("a", href=True, class_="title")["href"]
        return "https://ru.investing.com" + relative_url

    def _get_title(self, item: Tag) -> str:
        return item.find("a", class_="title").text

    def _get_time(self, item: Tag) -> datetime:
        # Release time is on the headline's web page
        page_html_text = self._get_headline_page(item)
        time_string = self._get_time_string(page_html_text)
        time_string = time_string[13:] + " +0300"  # add timezone
        time_format = "%d.%m.%Y %H:%M %z"
        return datetime.strptime(time_string, time_format)

    def _get_headline_page(self, item: Tag) -> str:
        url = self._get_url(item)
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
        except requests.RequestException:
            return ""
        return response.text

    def _get_time_string(self, html_text: str) -> str:
        soup = BeautifulSoup(html_text, "lxml")
        headline_details = soup.find_all(name="div", class_="contentSectionDetails")
        for detail in headline_details:
            if "Опубликовано" in detail.text:
                return detail.text.strip()
