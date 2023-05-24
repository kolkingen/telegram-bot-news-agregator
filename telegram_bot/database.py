from typing import Self
from datetime import datetime

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
from loguru import logger

from table_models import (
    DeclarativeBase, NewsSource, Headline, User, Subscription, UserRequest)


class DatabaseConnector:
    """Class for connecting to postgres database. Works as singleton."""

    def __init__(self) -> None:
        engine = create_engine(self._create_url())
        DeclarativeBase.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
    
    def __new__(cls: Self) -> Self:
        if not hasattr(cls, 'instance'):
            cls.instance = super(DatabaseConnector, cls).__new__(cls)
        logger.info('DatabaseConnector has created.')
        return cls.instance

    def _create_url(self) -> URL:
        return URL.create(
            drivername='postgresql',
            username='postgres',
            password='password',
            host='postgres_container',
            port=5432,
            database='postgres')

    def add_user(self, user_id: int, chat_id: int) -> None:
        """Adds user to database, if it not exists."""

        if not self.get_user_by_id(user_id):
            self.session.add(User(user_id, chat_id))
            self.session.commit()

    def change_user(
        self, user_id: int, 
        default_source: str | None = None, 
        news_count: int | None = None
    ) -> None:
        """Changes default_source and news_count for user by id."""

        user = self.get_user_by_id(user_id)
        if default_source is not None:
            user.default_source = default_source
        if news_count is not None:
            user.news_count = news_count
        self.session.commit()

    def get_user_by_id(self, user_id: int) -> User:
        return self.session.query(User)\
            .filter(User.user_id == user_id).first()

    def get_news_source_by_id(self, id_name: str) -> NewsSource:
        return self.session.query(NewsSource)\
            .filter(NewsSource.id_name == id_name).first()

    def get_news_sources(self) -> list[NewsSource]:
        return self.session.query(NewsSource).all()

    def get_last_headlines_by_source(
        self, source: str, limit: int = 5
    ) -> list[Headline]:
        return self.session.query(Headline)\
            .filter(Headline.source == source)\
            .order_by(Headline.time.desc())\
            .limit(limit).all()

    def get_user_subscriptions(self, user_id: int) -> list[str]:
        """Returns only id_names for sources in user's subscriptions."""
        subscriptions = self.session.query(Subscription)\
            .filter(Subscription.user_id == user_id).all()
        return [s.source for s in subscriptions]

    def delete_subscription(self, user_id: int, source: str) -> None:
        self.session.query(Subscription)\
            .filter(Subscription.user_id==user_id)\
            .filter(Subscription.source==source).delete()
        self.session.commit()

    def add_subscription(self, user_id: int, source: str) -> None:
        self.session.add(Subscription(user_id, source))
        self.session.commit()

    def add_user_request(self, user_id: int, request: str, time: int) -> None:
        formatted_time = datetime.fromtimestamp(time)
        user_request = UserRequest(user_id, request, formatted_time)
        self.session.add(user_request)
        self.session.commit()
