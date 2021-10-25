from aiogram import types
from icecream import ic
from data import text_util
import keyboards
from data.bot_setup import client_bot

# region server views
from utils import useful_methods


# region bot start

async def handle_start(message: types.Message):
    ic('start statement')
    await client_bot.send_message(message.chat.id,
                                  text_util.MAIN_MENU_OPENED.format(useful_methods.get_full_user_name(message)),
                                  reply_markup=keyboards.r_snippets.main_menu())

# endregion start
