from aiogram import types
from icecream import ic

import keyboards
import states.client
from data import config, text_util
from utils import useful_methods
from models import db
from utils import paginator
from data.bot_setup import client_bot


# region catalog

# region show catalog
async def handle_catalog_menu(message: types.Message):
    ic('show catalog statement')
    await states.client.CatalogGroup.catalog_menu.set()
    event = db.get_by_max(db.Event, db.Event.id)
    if isinstance(event, db.Event):
        await paginator.show_catalog_page(chat_id=message.chat.id,
                                          events=event.get_next_event(event.id, 2),
                                          bot=client_bot)
    else:
        await message.reply(text_util.CATALOG_EMPTY)


async def handle_catalog_callback(callback: types.CallbackQuery):
    event_id = int(useful_methods.get_id_from_data(callback.data, 2))
    additional_events = int(useful_methods.get_id_from_data(callback.data, 1))
    event = db.get_from_db_multiple_filter(db.Event, [db.Event.id == event_id])
    if isinstance(event, db.Event):
        await paginator.show_catalog_page(chat_id=callback.message.chat.id,
                                          events=event.get_next_event(event_id, additional_events),
                                          bot=client_bot)
    await callback.message.delete()
    pass


# endregion show catalog

# region delete event


# delete event
async def handle_delete_answer(callback: types.CallbackQuery):
    # if yes - delete event
    if config.YES in callback.data:
        # retrieve int
        event_id = useful_methods.get_id_from_data(callback.data, 1)
        event = db.get_from_db_multiple_filter(db.Event, [db.Event.id == event_id])
        if isinstance(event, db.Event):  # if event exist"
            event.delete()
        if callback.message:
            await callback.message.reply(text_util.EVENT_DELETED)
    if callback.message:
        await callback.message.delete()


async def handle_sure_to_delete_callback(callback: types.CallbackQuery):
    # solved create deleting with callback: delete - are you sure? yes: delete event, no: pass :: then delete message
    print(callback.data)
    event_id = useful_methods.get_id_from_data(callback.data, 1)
    if db.get_from_db_multiple_filter(db.Event, [db.Event.id == event_id]):
        await callback.message.reply(text_util.SURE_DELETE,
                                     reply_markup=keyboards.i_snippets.sure_inline_keyboard(event_id=event_id))
    else:
        await callback.message.reply(text_util.EVENT_DELETED,
                                     reply_markup=keyboards.r_snippets.main_menu())


# endregion delete event
async def show_event(callback: types.CallbackQuery):
    print(callback.data)
    event = useful_methods.get_event(callback)
    chat_id = callback.message.chat.id
    if isinstance(event, db.Event):
        await client_bot.send_photo(chat_id=chat_id,
                                    photo=event.get_media(),
                                    caption=f'{event.stringify()}')
    else:
        await client_bot.send_message(chat_id,
                                      text_util.EVENT_DELETED)
    # todonow send deep link
# endregion catalog
