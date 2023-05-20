import time

from finam_companies_rss_scrapper import FinamCompaniesRssScrapper
from headline import Headline
from investing_com_scrapper import InvestingComScrapper
from news_source import NewsSource
from ria_rss_scrapper import RiaRssScrapper

SECONDS_TO_REFRESH_NEWS = 5 * 60.0  # 5 min


def get_headlines(sources: list[NewsSource]) -> list[Headline]:
    """Loads news from all sources."""
    all_news_headlines = []
    for source in sources:
        all_news_headlines += source.get_headlines()
    return all_news_headlines


def print_headlines(headlines: list[Headline]) -> None:
    print("Количество новостей:", len(headlines))
    for h in headlines:
        print(f"{h.source} ({h.release_time:%a %H:%M}): {h.title}")


if __name__ == "__main__":

    news_sources: list[NewsSource] = [
        RiaRssScrapper(),
        InvestingComScrapper(),
        FinamCompaniesRssScrapper(),
    ]

    while True:
        news_headlines = get_headlines(news_sources)
        print_headlines(news_headlines)
        time.sleep(SECONDS_TO_REFRESH_NEWS)
