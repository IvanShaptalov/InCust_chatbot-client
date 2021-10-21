import os
import logging

from flask import request, Flask
from icecream import ic
import views
import settings
from aiogram import Bot, Dispatcher, executor, types

from client_chat_bot import states
from utils import db_util

# region bot config
logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot, storage=states.storage)
db_util.create_db()
server = Flask(__name__)
ic('configured')


# endregion

# region server routes
@server.route('/notification/', methods=['POST'])
def process_notification():
    return views.process_notification(request)


@server.route('/message/', methods=['POST'])
def process_message():
    return views.process_message(request)


@server.route('/' + settings.BOT_TOKEN, methods=['POST'])
def get_message():
    return views.process_updates(request, bot)


@server.route('/')
def webhook():
    return views.process_webhook(request, bot)


# endregion

# region bot routes
@dp.message_handler(commands=settings.START)
async def handle_start(message: types.Message):
    return await views.handle_start(message, bot)

# endregion

if __name__ == '__main__':
    if os.environ.get('heroku'):
        ic('listener run')
        server.run(host='0.0.0.0', port=settings.PORT)
    else:
        executor.start_polling(dp, skip_updates=True)
    ic('start')
# endregion
