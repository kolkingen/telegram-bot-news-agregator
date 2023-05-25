import asyncio

from telebot.async_telebot import AsyncTeleBot

from database import DatabaseConnector
from handler_utils import format_headline
from table_models import Headline

database = DatabaseConnector()


def _gather_users_info() -> list[dict[str, int | list[str]]]:
    return [
        {'chat_id': user.chat_id, 'news_count': user.news_count, 
         'sources': database.get_user_subscriptions(user.user_id)} 
        for user in database.get_users()
    ]


def _get_chat_id_headline_pairs(headlines) -> list[tuple[int, str]]:

    users_info = _gather_users_info()
    pairs = []

    for headline in headlines:
        for user in users_info:

            if headline.source in user['sources'] and user['news_count'] > 0:
                pair = (user['chat_id'], format_headline(headline))
                pairs.append(pair)
                # limiting number of headlines for user
                user['news_count'] -= 1

    return pairs


async def _deliver_headlines(
    bot: AsyncTeleBot, headlines: list[Headline]
) -> None:
    
    chat_text_pairs = _get_chat_id_headline_pairs(headlines)
    for chat_id, headline_text in chat_text_pairs:
        await bot.send_message(chat_id, headline_text)


async def new_headlines_check_loop(bot: AsyncTeleBot) -> None:
    """Every 5 seconds checks database for new headlines and delivers them."""

    while True:
        new_headlines = database.get_new_headlines()
        if new_headlines: 
            await _deliver_headlines(bot, new_headlines)
        await asyncio.sleep(5)
