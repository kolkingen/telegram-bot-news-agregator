from abc import ABC, abstractmethod
from datetime import datetime

import requests
from bs4 import ResultSet, Tag

from table_models import Headline, NewsSource


class NewsGetter(ABC):
    """Abstract class for all getters, scrappers of news."""

    def __init__(self) -> None:
        self.source = self._create_source()

    def get_headlines(self) -> list[Headline]:
        """Returns Headlines from chosen source."""
        try:
            response = requests.get(self.source.link, timeout=5)
            response.raise_for_status()
        except requests.RequestException:
            return []
        return self._parse_response(response.text)

    def _parse_response(self, response_text: str) -> list[Headline]:
        headlines = []
        for headline_item in self._get_headline_items(response_text):
            headline = self._parse_headline_item(headline_item)
            if headline is not None:
                headlines.append(headline)
        return headlines

    def _parse_headline_item(self, item: Tag) -> Headline | None:
        try:
            link = self._get_link(item)
            title = self._get_title(item)
            time = self._get_time(item)
        except Exception:
            # if any error occurs, then this headline is not valid
            return None
        return Headline(self.source.id_name, link, title, time)

    @abstractmethod
    def _create_source(self) -> NewsSource:
        pass

    @abstractmethod
    def _get_headline_items(self, response_text: str) -> ResultSet[Tag]:
        pass

    @abstractmethod
    def _get_link(self, item: Tag) -> str:
        pass

    @abstractmethod
    def _get_title(self, item: Tag) -> str:
        pass

    @abstractmethod
    def _get_time(self, item: Tag) -> datetime:
        pass
