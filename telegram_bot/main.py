from os import getenv

from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from loguru import logger

from message_handlers import register_message_handlers
from callback_handlers import register_callback_handlers


def load_token() -> str:
	"""Takes telegram bot api token from environment. 
	If there is no token, closes application.
	"""

	token = getenv('BOT_API_TOKEN')
	if not token:
		logger.error(f'Can\'t find telegram bot api token.')
		exit(1)
	return token


def check_if_bot_works(bot: TeleBot) -> None:
	"""Tests bot by getting info about bot from telegram server."""

	try:
		bot.get_me()
	except ApiTelegramException:
		logger.error('API token is not valid.')
		exit(1)


if __name__ == '__main__':

	logger.info('Application has started.')

	bot = TeleBot(load_token())
	check_if_bot_works(bot)
	register_message_handlers(bot)
	register_callback_handlers(bot)

	bot.infinity_polling()
