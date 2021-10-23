from aiogram import Bot, Dispatcher

from data.config import BOT_TOKEN
from states import client

bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot, storage=client.storage)
