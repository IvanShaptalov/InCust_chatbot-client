from aiogram import types
from icecream import ic

import models.db
from data import text_util
import keyboards
from data.bot_setup import client_bot

# region server views
from utils import useful_methods


# region bot start

async def handle_start(message: types.Message):
    ic('start statement')
    fullname = useful_methods.get_full_user_name(message)
    if not models.db.get_from_db_multiple_filter(models.db.User, [models.db.User.chat_id == message.chat.id]):
        user = models.db.User()
        user.chat_id, user.user_fullname = message.chat.id, fullname
        user.in_chat_service, user.in_chat_client = False, False
        user.save()
    await client_bot.send_message(message.chat.id,
                                  text_util.MAIN_MENU_OPENED.format(fullname),
                                  reply_markup=keyboards.r_snippets.main_menu())

# endregion start
