import json
import os
import logging
from flask import request, Flask
from icecream import ic

import settings
from aiogram import Bot, Dispatcher, executor

from utils import db_util

logging.basicConfig(level=logging.INFO)
# config
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)
db_util.create_db()
server = Flask(__name__)
ic('configured')


@server.route('/notification/', methods=['POST'])
def process():
    ic('add')
    post_data = request.get_data().decode("utf-8")
    data = json.loads(post_data)
    return "201"


@server.route('/message/', methods=['POST'])
def decline():
    ic('decline')
    post_data = request.get_data().decode()
    data = json.loads(post_data)
    try:
        bot.send_message(chat_id=data['chat_id'],
                         text=data['text'])
    except Exception as e:
        print(e, type(e))
        return 'bad request'
    else:
        return '200'


@server.route('/' + settings.BOT_TOKEN, methods=['POST'])
def get_message():
    ic('process new updates')
    json_string = request.get_data().decode('utf-8')
    # update = telebot.types.Update.de_json(json_string)
    # bot.process_new_updates([update])
    return "!", 200


@server.route('/')
def webhook():
    # ic('set webhook')
    # bot.remove_webhook()
    # webhook_url = settings.bot_link + settings.BOT_TOKEN
    # ic(webhook_url)
    # bot.set_webhook(url=webhook_url)
    return '!', '200'


# endregion
if __name__ == '__main__':
    if os.environ.get('heroku'):
        ic('listener run')
        server.run(host='0.0.0.0', port=settings.PORT)
    else:
        executor.start_polling(dp, skip_updates=True)
    ic('start')
# endregion
