import logging

from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from icecream import ic

import settings
from client_chat_bot import states
from utils import useful_methods, keyboard_snippets, text_util


# region catalog
async def handle_catalog(message: types.Message, bot: Bot):
    ic('show catalog statement')
    await bot.send_message(message.chat.id,
                           text_util.CATALOG_OPENED)


# endregion catalog