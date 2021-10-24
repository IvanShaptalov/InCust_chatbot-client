import handlers
from aiogram import executor
from data.bot_setup import dispatcher

from models import db

if __name__ == '__main__':
    handlers.setup(dispatcher)
    db.create_db()
    executor.start_polling(dispatcher, skip_updates=True)
