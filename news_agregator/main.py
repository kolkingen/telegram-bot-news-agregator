import time

from loguru import logger

from database import Database
from table_models import Headline
from news_getter import NewsGetter
from ria_rss_scrapper import RiaRssScrapper
from investing_com_scrapper import InvestingComScrapper
from finam_companies_rss_scrapper import FinamCompaniesRssScrapper

SECONDS_TO_REFRESH_NEWS = 60.0


def get_headlines(getters: list[NewsGetter]) -> list[Headline]:
    """Loads news from all sources."""
    all_headlines = []
    for getter in getters:
        all_headlines += getter.get_headlines()
    return all_headlines


if __name__ == '__main__':

    logger.info('Application is started.')

    news_getters: list[NewsGetter] = [
        RiaRssScrapper(),
        InvestingComScrapper(),
        FinamCompaniesRssScrapper()]

    database = Database()
    database.insert_news_sources(news_getters)

    while True:
        headlines = get_headlines(news_getters)
        new_headlines = database.filter_out_old_headlines(headlines)
        database.insert_headlines(new_headlines)
        logger.info(f'{len(headlines)} headlines are downloaded. '
                    f'{len(new_headlines)} of them are new.')
        time.sleep(SECONDS_TO_REFRESH_NEWS)
