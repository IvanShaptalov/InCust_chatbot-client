from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from icecream import ic

import settings
from utils import text_util, db_util, keyboard_snippets, useful_methods


# region catalog

# region show catalog
async def handle_catalog_message(message: types.Message, bot: Bot):
    ic('show catalog statement')

    event = db_util.get_by_max(db_util.Event, db_util.Event.id)
    await show_catalog_page(chat_id=message.chat.id,
                            events=event.get_next_event(event.id, 2),
                            bot=bot)


async def show_catalog_page(chat_id, events: list, bot: Bot):
    """
    show catalog page to users
    :param chat_id: user chat id
    :param events: list of events
    :param bot: bot
    """
    last_event = None
    for event in events:
        markup = keyboard_snippets.inline_markup(text_util.CONNECT_EVENT, f'{settings.CONNECT_TO_EVENT}:{event.id}')
        if event.event_owner_id == chat_id:
            # markup to owner
            markup.add(
                keyboard_snippets.inline_button(text_util.DELETE_EVENT, f'{settings.DELETE_EVENT}:{event.id}'))  # button to delete event
            pass
        await bot.send_photo(chat_id=chat_id,
                             photo=event.get_media(),
                             caption=f'{event.stringify()}',
                             reply_markup=markup)
        last_event = event
    assert isinstance(last_event, db_util.Event)
    if db_util.get_from_db_multiple_filter(db_util.Event, [db_util.Event.id == last_event.previous_event_id]):
        markup = keyboard_snippets.inline_markup(text_util.PLUS(1), f"{settings.ADD_EVENTS_PAGINATOR}:{1}:{last_event.previous_event_id}").add(
            keyboard_snippets.inline_button(text_util.PLUS(5), f'{settings.ADD_EVENTS_PAGINATOR}:{5}:{last_event.previous_event_id}'))

        await bot.send_message(chat_id,
                               text_util.SHOW_MORE,
                               reply_markup=markup)  # event id and count to add in page
    pass


# endregion

# region delete event
async def handle_catalog_callback(callback: types.CallbackQuery, bot: Bot):
    event_id = int(useful_methods.get_id_from_data(callback.data, 2))
    additional_events = int(useful_methods.get_id_from_data(callback.data, 1))
    event = db_util.get_from_db_multiple_filter(db_util.Event, [db_util.Event.id == event_id])
    await show_catalog_page(chat_id=callback.message.chat.id,
                            events=event.get_next_event(event_id, additional_events),
                            bot=bot)
    await callback.message.delete()
    pass


async def handle_delete_answer(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    if settings.YES in callback.data:
        # retrieve int
        event_id = useful_methods.get_id_from_data(callback.data, 1)
        event = db_util.get_from_db_multiple_filter(db_util.Event, [db_util.Event == callback.data])
        event.delete()
        await state.finish()
        await callback.message.reply(text_util.EVENT_DELETED)
    elif settings.NO in callback.data:
        await callback.message.delete()
        await state.finish()


async def handle_delete_event_callback(callback: types.CallbackQuery, bot: Bot):
    pass
    # todonext create deleting with callback: delete - are you sure? yes: delete event, no: pass :: then delete message
    # print(callback.data)
    # await states.ask_to_delete.set().
    # await state.update_data()
    # await callback.message.reply(text_util.SURE_DELETE,
    #                              reply_markup=keyboard_snippets.sure_keyboard())

# endregion delete event

# endregion catalog
