import os
import logging

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from flask import request, Flask
from icecream import ic
from client_chat_bot.views import views, views_catalog, views_add_event
import settings
from aiogram import Bot, Dispatcher, executor, types

from client_chat_bot import states
from client_chat_bot.states import EventForm
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
# region start
@dp.message_handler(lambda message: message.text == settings.START or message.text == settings.MAIN_MENU)
async def handle_start(message: types.Message):
    logging.info(message.chat.id)
    return await views.handle_start(message, bot)


# endregion start

# region catalog
@dp.message_handler(lambda message: message.text in settings.CATALOG)
async def handle_catalog(message: types.Message):
    return await views_catalog.handle_catalog_message(message, bot)


@dp.callback_query_handler(lambda callback: settings.DELETE_EVENT in callback.data)
async def handle_delete_event_callback(callback: types.CallbackQuery):
    return await views_catalog.handle_delete_event_callback(callback, bot)


# @dp.message_handler(lambda message: message.text.lower() == settings.YES.lower()
#                     or message.text.lower() == settings.NO.lower(),
#                     state=states.ask_to_delete)
# async def handle_delete_answer(message: types.Message, )

@dp.callback_query_handler(lambda callback: settings.ADD_EVENTS_PAGINATOR in callback.data)
async def handle_callback_paginator(callback: types.CallbackQuery):
    return await views_catalog.handle_catalog_callback(callback, bot)


# endregion catalog

# region add event
@dp.message_handler(lambda message: message.text in settings.ADD_EVENT)
async def handle_add_catalog(message: types.Message):
    """
    Conversation's entry point
    """
    return await views_add_event.handle_add_event(message, bot)


@dp.message_handler(Text(equals=settings.MAIN_MENU, ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    return await views_add_event.cancel_handler(message, state, bot)


# event name
@dp.message_handler(lambda message: len(message.text) <= 3, state=EventForm.event_name)
async def handle_event_name_invalid(message: types.Message, state: FSMContext):
    return await views_add_event.handle_text_length_smaller_3(message, state)


@dp.message_handler(state=EventForm.event_name)
async def handle_event_name(message: types.Message, state: FSMContext):
    return await views_add_event.handle_event_name(message, state)


# event title
@dp.message_handler(lambda message: len(message.text) <= 3, state=EventForm.event_title)
async def handle_event_title_invalid(message: types.Message, state: FSMContext):
    return await views_add_event.handle_text_length_smaller_3(message, state)


@dp.message_handler(state=EventForm.event_title)
async def handle_event_title(message: types.Message, state: FSMContext):
    return await views_add_event.handle_event_title(message, state)


# description
@dp.message_handler(lambda message: len(message.text) <= 3, state=EventForm.description)
async def handle_event_description_invalid(message: types.Message, state: FSMContext):
    return await views_add_event.handle_text_length_smaller_3(message, state)


@dp.message_handler(state=EventForm.description)
async def handle_description(message: types.Message, state: FSMContext):
    return await views_add_event.handle_description(message, state)


# media
@dp.message_handler(content_types=['text', 'document', 'audio', 'contact', 'gps'], state=EventForm.media)
async def handle_invalid_photo(message: types.Message, state: FSMContext):
    return await views_add_event.handle_invalid_photo(message, state)


@dp.message_handler(content_types=['photo'], state=EventForm.media)
async def handle_photo(message: types.Message, state: FSMContext):
    return await views_add_event.handle_photo(message, state, bot)


@dp.message_handler(content_types=['text'], state=EventForm.end_date)
async def handle_end_date(message: types.Message, state: FSMContext):
    return await views_add_event.handle_end_date(message, state, bot)


# endregion add event


# endregion bot routes

# region engine
if __name__ == '__main__':
    if os.environ.get('heroku'):
        ic('listener run')
        server.run(host='0.0.0.0', port=settings.PORT)
    else:
        executor.start_polling(dp, skip_updates=True)
    ic('start')
# endregion engine
