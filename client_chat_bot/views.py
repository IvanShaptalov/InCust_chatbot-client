import json

from aiogram import types, Bot
from icecream import ic
import states
from utils import useful_methods, keyboard_snippets

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


def process_updates(request, bot):
    ic('process new updates')
    json_string = request.get_data().decode('utf-8')
    # update = telebot.types.Update.de_json(json_string)
    # bot.process_new_updates([update])
    return "!", 200


def process_webhook(request, bot):
    return ...


# endregion


# region bot views
async def handle_start(message: types.Message, bot: Bot):
    ic('start statement')
    await bot.send_message(message.chat.id,
                           f'Добро пожаловать {useful_methods.get_full_user_name(message)}!',
                           reply_markup=keyboard_snippets.main_menu())

# endregion
