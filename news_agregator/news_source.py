from abc import ABC, abstractmethod
from datetime import datetime

import requests
from bs4 import ResultSet, Tag
from headline import Headline


class NewsSource(ABC):
    """Abstract class for all news sources."""

    _id = ""
    _url = ""

    def get_headlines(self) -> list[Headline]:
        """Returns Headlines from chosen sourse."""
        try:
            response = requests.get(self._url, timeout=5)
            response.raise_for_status()
        except requests.RequestException:
            return []
        return self._parse_response(response.text)

    def _parse_response(self, response_text: str) -> list[Headline]:
        headlines = []
        for headline_item in self._get_headline_items(response_text):
            headline = self._parse_headline_item(headline_item)
            if headline:
                headlines.append(headline)
        return headlines

    def _parse_headline_item(self, item: Tag) -> Headline | None:
        try:
            url=self._get_url(item)
            title=self._get_title(item)
            release_time=self._get_time(item)
        except Exception:
            # if any error occurs, then this headline is not valid
            return None
        return Headline(self._id, url, title, release_time)

    @abstractmethod
    def _get_headline_items(self, response_text: str) -> ResultSet[Tag]:
        pass

    @abstractmethod
    def _get_url(self, item: Tag) -> str:
        pass

    @abstractmethod
    def _get_title(self, item: Tag) -> str:
        pass

    @abstractmethod
    def _get_time(self, item: Tag) -> datetime:
        pass
