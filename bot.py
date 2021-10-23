import os
import logging
from flask import request, Flask
from icecream import ic

import handlers
from handlers import views
from aiogram import executor

from data import config
from data.bot_setup import dispatcher

# region bot config
from models import db

db.create_db()
logging.basicConfig(level=logging.INFO)
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


@server.route('/' + config.BOT_TOKEN, methods=['POST'])
def get_message():
    return views.process_updates(request)


@server.route('/')
def webhook():
    return views.process_webhook(request)


# endregion


# region engine
if __name__ == '__main__':
    handlers.setup(dispatcher)
    if os.environ.get('heroku'):
        ic('listener run')
        server.run(host='0.0.0.0', port=config.PORT)
    else:
        executor.start_polling(dispatcher, skip_updates=True)
    ic('start')
# endregion engine
