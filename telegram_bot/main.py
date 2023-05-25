from os import getenv
import asyncio

from telebot.async_telebot import AsyncTeleBot
from loguru import logger

from message_handlers import register_message_handlers
from callback_handlers import register_callback_handlers
from new_headlines_check_loop import new_headlines_check_loop


def load_token() -> str:
	"""Takes telegram bot api token from environment. 
	If there is no token, closes application.
	"""

	token = getenv('BOT_API_TOKEN')
	if not token:
		logger.error(f'Can\'t find telegram bot api token.')
		exit(1)
	return token


async def start_main_loop(bot: AsyncTeleBot):
	await asyncio.gather(
		bot.infinity_polling(), 
		new_headlines_check_loop(bot))


if __name__ == '__main__':

	logger.info('Application has started.')

	bot = AsyncTeleBot(load_token(), parse_mode='markdown')
	register_message_handlers(bot)
	register_callback_handlers(bot)

	asyncio.run(start_main_loop(bot))
