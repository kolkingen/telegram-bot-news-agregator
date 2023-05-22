from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, ForeignKey, String

DeclarativeBase = declarative_base()


class NewsSource(DeclarativeBase):
    """Information about news sources. Compatible with SQLAlchemy."""
    
    __tablename__ = 'news_sources'

    id_name = Column('id_name', String, primary_key=True)
    show_name = Column('show_name', String, nullable=False)
    link = Column('link', String, nullable=False)

    def __init__(self, id_name: str, show_name: str, link: str) -> None:
        self.id_name = id_name
        self.show_name = show_name
        self.link = link

    def __repr__(self) -> str:
        return self.show_name


class Headline(DeclarativeBase):
    """Information about news headlines. Compatible with SQLAlchemy."""

    __tablename__ = 'headlines'

    source = Column('source', String, ForeignKey(NewsSource.id_name))
    link = Column('link', String, primary_key=True)
    title = Column('title', String, nullable=False)
    time = Column('time', DateTime, nullable=False)

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
