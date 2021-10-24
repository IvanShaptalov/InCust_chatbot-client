from aiogram import Bot, Dispatcher

from data.config import CLIENT_BOT_TOKEN, SERVICE_BOT_TOKEN
from states import client

client_bot = Bot(token=CLIENT_BOT_TOKEN)
service_bot = Bot(token=SERVICE_BOT_TOKEN)
dispatcher = Dispatcher(client_bot, storage=client.storage)
