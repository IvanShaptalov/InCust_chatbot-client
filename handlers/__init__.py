from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text

from data import config
from states.client import EventForm, CatalogGroup

from . import add_event
from . import catalog
from . import chat
from . import views


def setup(dp: Dispatcher):
    # views
    dp.register_message_handler(views.handle_start,
                                lambda message: message.text == config.START or message.text == config.MAIN_MENU)

    # catalog
    dp.register_message_handler(catalog.handle_catalog_menu, lambda message: message.text in config.CATALOG, state='*')
    dp.register_callback_query_handler(catalog.handle_sure_to_delete_callback,
                                       lambda callback: config.DELETE_EVENT in callback.data, state='*')
    dp.register_callback_query_handler(catalog.handle_delete_answer,
                                       lambda callback: config.YES in callback.data or config.NO in callback.data,
                                       state='*')
    dp.register_callback_query_handler(catalog.handle_catalog_callback,
                                       lambda callback: config.ADD_EVENTS_PAGINATOR in callback.data, state='*')

    # add_event
    dp.register_message_handler(add_event.handle_add_event, lambda message: message.text in config.ADD_EVENT, state='*')

    dp.register_message_handler(add_event.cancel_handler, Text(equals=config.MAIN_MENU, ignore_case=True), state='*')

    dp.register_message_handler(add_event.handle_text_length_smaller_3, lambda message: len(message.text) <= 3,
                                state=EventForm.event_name)
    dp.register_message_handler(add_event.handle_event_name, state=EventForm.event_name)

    dp.register_message_handler(add_event.handle_text_length_smaller_3, lambda message: len(message.text) <= 3,
                                state=EventForm.event_title)
    dp.register_message_handler(add_event.handle_event_title, state=EventForm.event_title)

    dp.register_message_handler(add_event.handle_text_length_smaller_3, lambda message: len(message.text) <= 3,
                                state=EventForm.description)
    dp.register_message_handler(add_event.handle_description, state=EventForm.description)

    dp.register_message_handler(add_event.handle_invalid_photo,
                                content_types=['text', 'document', 'audio', 'contact', 'gps'], state=EventForm.media)
    dp.register_message_handler(add_event.handle_photo, content_types=['photo'], state=EventForm.media)

    dp.register_message_handler(add_event.handle_end_date, content_types=['text'], state=EventForm.end_date)

    # chat
    dp.register_callback_query_handler(chat.handle_chat_connect,
                                       lambda callback: config.CONNECT_TO_CHAT in callback.data,
                                       state=CatalogGroup.catalog_menu)
    dp.register_message_handler(chat.leave_chat, Text(equals=config.EXIT_FROM_CHAT), state='*')
    dp.register_message_handler(chat.show_event, Text(equals=config.SHOW_EVENT_IN_CHAT), state=CatalogGroup.in_chat)
    # chat content sending
    dp.register_message_handler(chat.send_text_message, content_types=['text'], state=CatalogGroup.in_chat)
    dp.register_message_handler(chat.send_location, content_types=['location'], state=CatalogGroup.in_chat)
    dp.register_message_handler(chat.send_sticker, content_types=['sticker'], state=CatalogGroup.in_chat)
    dp.register_message_handler(chat.send_photo, content_types=['photo'], state=CatalogGroup.in_chat)
    dp.register_message_handler(chat.send_animation, content_types=['animation'], state=CatalogGroup.in_chat)
    dp.register_message_handler(chat.send_audio, content_types=['audio'], state=CatalogGroup.in_chat)
    dp.register_message_handler(chat.send_video, content_types=['video'], state=CatalogGroup.in_chat)
    dp.register_message_handler(chat.send_voice, content_types=['voice'], state=CatalogGroup.in_chat)
    # service_bot
