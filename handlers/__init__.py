from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text

from data import config
from states.client import EventForm
from . import add_event
from . import catalog
from . import chat
from . import views
from . import service_bot


def setup(dp: Dispatcher):
    # views
    dp.register_message_handler(views.handle_start,
                                lambda message: message.text == config.START or message.text == config.MAIN_MENU)
    # dp.register_message_handler(views.)

    # catalog
    dp.register_message_handler(catalog.handle_catalog_menu, lambda message: message.text in config.CATALOG)
    dp.register_callback_query_handler(catalog.handle_sure_to_delete_callback,
                                       lambda callback: config.DELETE_EVENT in callback.data)
    dp.register_callback_query_handler(catalog.handle_delete_answer,
                                       lambda callback: config.YES in callback.data or config.NO in callback.data)
    dp.register_callback_query_handler(catalog.handle_catalog_callback,
                                       lambda callback: config.ADD_EVENTS_PAGINATOR in callback.data)

    # add_event
    dp.register_message_handler(add_event.handle_add_event, lambda message: message.text in config.ADD_EVENT)
    dp.register_message_handler(add_event.cancel_handler, Text(equals=config.MAIN_MENU, ignore_case=True), state='*')

    dp.register_message_handler(add_event.handle_text_length_smaller_3, lambda message: len(message.text) <= 3, state=EventForm.event_name)
    dp.register_message_handler(add_event.handle_event_name, state=EventForm.event_name)

    dp.register_message_handler(add_event.handle_text_length_smaller_3, lambda message: len(message.text) <= 3, state=EventForm.event_title)
    dp.register_message_handler(add_event.handle_event_title, state=EventForm.event_title)

    dp.register_message_handler(add_event.handle_text_length_smaller_3, lambda message: len(message.text) <= 3, state=EventForm.event_title)
    dp.register_message_handler(add_event.handle_description, state=EventForm.description)

    dp.register_message_handler(add_event.handle_invalid_photo, content_types=['text', 'document', 'audio', 'contact', 'gps'], state=EventForm.media)
    dp.register_message_handler(add_event.handle_photo, content_types=['photo'], state=EventForm.media)

    dp.register_message_handler(add_event.handle_end_date, content_types=['text'], state=EventForm.end_date)

    # chat

    # service_bot
