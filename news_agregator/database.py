from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from news_getter import NewsGetter
from table_models import DeclarativeBase, Headline


class Database:

    def __init__(self) -> None:
        engine = create_engine(self._create_url())
        DeclarativeBase.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def insert_news_sources(self, getters: list[NewsGetter]) -> None:
        """Inserts sources into `news_sources` db table."""
        for getter in getters:
            self.session.merge(getter.source)
        self.session.commit()
    
    def insert_headlines(self, headlines: list[Headline]) -> None:
        """Inserts headlines into `headlines` db table."""
        self.session.add_all(headlines)
        self.session.commit()
    
    def filter_out_old_headlines(
            self, headlines: list[Headline]
    ) -> list[Headline]:
        """Returns only new headlines."""

        new_headlines = []
        query = self.session.query(Headline)
        for headline in headlines:
            if not query.filter(Headline.link==headline.link).first():
                new_headlines.append(headline)
        return new_headlines

    def _create_url(self) -> URL:
        return URL.create(
            drivername='postgresql',
            username='postgres',
            password='password',
            host='postgres_container',
            port=5432,
            database='postgres')
