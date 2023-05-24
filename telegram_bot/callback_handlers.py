from functools import partial
from typing import Callable

from telebot import TeleBot
from telebot.types import CallbackQuery

from handler_utils import get_headlines_for_user, edit_message_after_choosing
from database import DatabaseConnector

database = DatabaseConnector()


def _handle_callback_from_source(callback: CallbackQuery, bot: TeleBot) -> None:
    source = database.get_news_source_by_id(callback.data.split()[-1])
    edit_message_after_choosing(bot, callback.message, source.show_name)
    for h in get_headlines_for_user(callback.from_user.id, source.id_name):
        bot.send_message(callback.message.chat.id, h, parse_mode='markdown')
    database.add_user_request(
        callback.from_user.id, callback.data, callback.message.date)


def _handle_callback_default(callback: CallbackQuery, bot: TeleBot) -> None:
    source = database.get_news_source_by_id(callback.data.split()[-1])
    database.change_user(callback.from_user.id, default_source=source.id_name)
    edit_message_after_choosing(bot, callback.message, source.show_name)
    database.add_user_request(
        callback.from_user.id, callback.data, callback.message.date)


def _handle_callback_update_n(callback: CallbackQuery, bot: TeleBot) -> None:
    n = int(callback.data.split()[-1])
    database.change_user(callback.from_user.id, news_count=n)
    edit_message_after_choosing(bot, callback.message, str(n))
    database.add_user_request(
        callback.from_user.id, callback.data, callback.message.date)


def _handle_callback_subscriptions(callback: CallbackQuery, bot: TeleBot) -> None:
    source = database.get_news_source_by_id(callback.data.split()[-1])
    edit_message_after_choosing(bot, callback.message, source.show_name)
    user_subscriptions = database.get_user_subscriptions(callback.from_user.id)
    if source.id_name in user_subscriptions:
        database.delete_subscription(callback.from_user.id, source.id_name)
    else:
        database.add_subscription(callback.from_user.id, source.id_name)
    database.add_user_request(
        callback.from_user.id, callback.data, callback.message.date)


def _get_command_filter(source: str) -> Callable[[CallbackQuery], bool]:
    def filter(callback: CallbackQuery) -> bool:
        return callback.data.startswith(source)
    return filter


def register_callback_handlers(bot: TeleBot) -> None:
    """Registers callback handlers for commands: 
    /from_source, /default, /update_n, /subscriptions.
    """

    reg = partial(bot.register_callback_query_handler, pass_bot=True)
    reg(_handle_callback_from_source, _get_command_filter('from_source'))
    reg(_handle_callback_default, _get_command_filter('default'))
    reg(_handle_callback_update_n, _get_command_filter('update_n'))
    reg(_handle_callback_subscriptions, _get_command_filter('subscriptions'))
