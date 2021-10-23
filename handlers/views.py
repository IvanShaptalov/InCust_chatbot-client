import json
from aiogram import types
from icecream import ic
from data import text_util
import keyboards
from data.bot_setup import bot


# region server views


def process_notification(request):
    ic('add')
    post_data = request.get_data().decode("utf-8")
    data = json.loads(post_data)
    return "201"


def process_message(request):
    ic('decline')
    post_data = request.get_data().decode()
    data = json.loads(post_data)
    # try:
    #     bot.send_message(chat_id=data['chat_id'],
    #                      text=data['text'])
    # except Exception as e:
    #     print(e, type(e))
    #     return 'bad request'
    # else:
    #     return '200'
    return '200'


def process_updates(request):
    ic('process new updates')
    json_string = request.get_data().decode('utf-8')
    # update = telebot.types.Update.de_json(json_string)
    # bot.process_new_updates([update])
    return "!", 200


def process_webhook(request):
    return ...


# endregion

# region bot start

async def handle_start(message: types.Message):
    ic('start statement')
    await bot.send_message(message.chat.id,
                           text_util.MAIN_MENU_OPENED(message),
                           reply_markup=keyboards.r_snippets.main_menu())

# endregion start
