from aiogram import Bot

from data import config, text_util
from models import db
import keyboards


async def show_catalog_page(chat_id, events: list, bot: Bot):
    """
    show catalog page to users
    :param chat_id: user chat id
    :param events: list of events
    :param bot: bot
    """
    last_event = None
    for event in events:
        markup = keyboards.inline.inline_markup(text_util.CONNECT_EVENT, f'{config.CONNECT_TO_CHAT}:{event.id}')

        if event.event_owner_id == chat_id:
            # markup to owner
            markup.add(
                keyboards.inline.inline_button(text_util.DELETE_EVENT,
                                               f'{config.DELETE_EVENT}:{event.id}'))  # button to delete event
            pass
        await bot.send_photo(chat_id=chat_id,
                             photo=event.get_media(),
                             caption=f'{event.stringify()}',
                             reply_markup=markup)
        last_event = event
    assert isinstance(last_event, db.Event)
    if db.get_from_db_multiple_filter(db.Event, [db.Event.id == last_event.previous_event_id]):
        markup = keyboards.inline.inline_markup(text_util.PLUS.format(1),
                                                f"{config.ADD_EVENTS_PAGINATOR}:{1}:{last_event.previous_event_id}").add(
            keyboards.inline.inline_button(text_util.PLUS.format(5),
                                           f'{config.ADD_EVENTS_PAGINATOR}:{5}:{last_event.previous_event_id}'))

        await bot.send_message(chat_id,
                               text_util.SHOW_MORE,
                               reply_markup=markup)  # event id and count to add in page
