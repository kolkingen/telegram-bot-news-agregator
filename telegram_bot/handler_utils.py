from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telebot.util import quick_markup

import messages
from table_models import Headline, NewsSource, Subscription
from database import DatabaseConnector

database = DatabaseConnector()


def _format_headline(headline: Headline) -> str:
    """Formats headline for showing to user. It uses markdown style."""
    source = database.get_news_source_by_id(headline.source)
    return f'[{source.show_name}]({headline.link}) ({headline.time:%d.%m.%y %H:%M:%S})\n\n{headline.title}'


def create_inline_keyboard_for_sources(
        callback_prefix: str,
        user_subscriptions: list[str] | None = None
) -> InlineKeyboardMarkup:
    """Creates inline keybord with sources' full names. 
    If `user_subscriptions` is not None, adds info about subscriptions.
    """
    
    sources = database.get_news_sources()
    inline_keyboard_markup = InlineKeyboardMarkup()
    for source in sources:

        if user_subscriptions is None:
            sub_info = ''
        elif source.id_name in user_subscriptions:
            sub_info = ' - ' + messages.yes_subscription
        else:
            sub_info = ' - ' + messages.no_subscription

        button = InlineKeyboardButton(
            source.show_name + sub_info, 
            callback_data=f'{callback_prefix} {source.id_name}')
        inline_keyboard_markup.add(button)
    return inline_keyboard_markup


def get_headlines_for_user(user_id: int, source: str | None = None) -> None:
    """Returns formatted headlines for `user` from `source`. 
    If source is None, it uses `user.default_source`.
    Returns only `user.news_count` headlines.
    """

    user = database.get_user_by_id(user_id)
    if source is None: source = user.default_source
    headlines = database.get_last_headlines_by_source(source, user.news_count)
    return [_format_headline(h) for h in headlines]


def edit_message_after_choosing(
    bot: TeleBot, message: Message, choice: str
) -> None:
    """Edits message with inline keyboard. Removes keyboard, prints choice."""

    new_text = ' '.join((message.text, messages.you_have_chosen, choice))
    bot.edit_message_text(
        new_text, message.chat.id, message.id, reply_markup=None)
