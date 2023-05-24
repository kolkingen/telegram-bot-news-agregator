"""This module represents tables from working 
database, compatible with SQLAlchemy.
Both `news_agregator` and `telegram_bot` use it.
"""


from datetime import datetime

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, DateTime, ForeignKey, String, Integer

DeclarativeBase = declarative_base()


class NewsSource(DeclarativeBase):
    """Information about news sources. Compatible with SQLAlchemy."""
    
    __tablename__ = 'news_sources'

    id_name = Column(String, primary_key=True)
    show_name = Column(String, nullable=False)
    link = Column(String, nullable=False)

    def __init__(self, id_name: str, show_name: str, link: str) -> None:
        self.id_name = id_name
        self.show_name = show_name
        self.link = link

    def __repr__(self) -> str:
        return self.show_name


class Headline(DeclarativeBase):
    """Information about news headlines. Compatible with SQLAlchemy."""

    __tablename__ = 'headlines'

    source = Column(String, ForeignKey(NewsSource.id_name))
    link = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    time = Column(DateTime, nullable=False)

    def __init__(
        self, source: str, link: str, 
        title: str, time: datetime
    ) -> None:

        self.source = source
        self.link = link
        self.title = title
        self.time = time

    def __repr__(self) -> None:
        return f'{self.source} ({self.time:%a %H:%M}): {self.title}'


class User(DeclarativeBase):
    """Information about telegram user. Compatible with SQLAlchemy."""

    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True)
    news_count = Column(Integer, default=5, nullable=False)
    default_source = Column(
        String, ForeignKey(NewsSource.id_name), nullable=True)

    def __init__(
        self, user_id: int, chat_id: int, 
        news_count: int = 5, 
        default_source: str | None = None
    ) -> None:

        self.user_id = user_id
        self.chat_id = chat_id
        self.news_count = news_count
        self.default_source = default_source
    
    def __repr__(self) -> str:
        return str(self.user_id)


class UserRequest(DeclarativeBase):
    """Information about interaction with user. Compatible with SQLAlchemy."""

    __tablename__ = 'user_requests'

    request_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.user_id), nullable=False)
    request = Column(String, nullable=False)
    time = Column(DateTime, nullable=False)

    def __init__(self, user_id: int, request: str, time: datetime) -> None:
        self.user_id = user_id
        self.request = request
        self.time = time
    
    def __repr__(self) -> str:
        return f'({self.time}) {self.user_id}: {self.request}'


class Subscription(DeclarativeBase):
    """Information about user subscriptions for news sources. 
    Compatible with SQLAlchemy.
    """

    __tablename__ = 'subscriptions'

    subscription_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.user_id), nullable=False)
    source = Column(String, ForeignKey(NewsSource.id_name), nullable=True)

    def __init__(self, user_id: int, source: str) -> None:
        self.user_id = user_id
        self.source = source

    def __repr__(self) -> str:
        return f'{self.user_id} is subscribed to {self.source}.'
