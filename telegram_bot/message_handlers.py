from functools import partial

from telebot import TeleBot
from telebot.types import Message
from telebot.util import quick_markup
from loguru import logger

import messages
from database import DatabaseConnector
from handler_utils import (
    create_inline_keyboard_for_sources, get_headlines_for_user)

database = DatabaseConnector()


async def _handle_start(message: Message, bot: TeleBot) -> None:
    await bot.send_message(message.chat.id, messages.start)
    database.add_user(message.from_user.id, message.chat.id)
    database.add_user_request(message.from_user.id, 'start', message.date)


async def _handle_default(message: Message, bot: TeleBot) -> None:
    answers_keyboard = create_inline_keyboard_for_sources('default')
    await bot.send_message(
        message.chat.id, messages.default, reply_markup=answers_keyboard)


async def _handle_get(message: Message, bot: TeleBot) -> None:
    user = database.get_user_by_id(message.from_user.id)
    if user.default_source is None:
        await bot.send_message(message.chat.id, messages.no_default_source)
    else:
        for headline in get_headlines_for_user(user.user_id):
            await bot.send_message(user.chat_id, headline)
    database.add_user_request(message.from_user.id, 'get', message.date)


async def _handle_update_n(message: Message, bot: TeleBot) -> None:
    answers_keyboard = quick_markup(
        {f'{option}': {'callback_data': f'update_n {option}'} 
         for option in [1, 2, 3, 5, 10, 15, 20, 25]})
    await bot.send_message(
        message.chat.id, messages.update_n, reply_markup=answers_keyboard)


async def _handle_from_source(message: Message, bot: TeleBot) -> None:
    answers = create_inline_keyboard_for_sources('from_source')
    await bot.send_message(
        message.chat.id, messages.from_source, reply_markup=answers)


async def _handle_subscriptions(message: Message, bot: TeleBot) -> None:
    user_sources = database.get_user_subscriptions(message.from_user.id)
    answers_keyboard = create_inline_keyboard_for_sources(
        'subscriptions', user_sources)
    await bot.send_message(
        message.chat.id, messages.subscriptions, reply_markup=answers_keyboard)


def register_message_handlers(bot: TeleBot) -> None:
    """Registers message handlers for commands: 
    /start, /default, /get, /update_n, /from_source, /subscriptions.
    For other messages registers /start handler.
    """

    reg = partial(bot.register_message_handler, pass_bot=True)
    reg(_handle_default, commands=['default'])
    reg(_handle_get, commands=['get'])
    reg(_handle_update_n, commands=['update_n'])
    reg(_handle_from_source, commands=['from_source'])
    reg(_handle_subscriptions, commands=['subscriptions'])
    reg(_handle_start, func=lambda m: True)
