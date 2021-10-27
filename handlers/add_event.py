import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from icecream import ic

from data import config, text_util
from data.bot_setup import client_bot

import states
import keyboards
from handlers import views
from keyboards.reply.r_snippets import go_to_main_menu
from utils import useful_methods
from models import db


async def handle_add_event(message: types.Message):
    ic('add event')
    await client_bot.send_message(message.chat.id,
                                  text_util.EVENT_CREATING_OPENED,
                                  reply_markup=go_to_main_menu())
    await states.client.EventForm.event_name.set()


# region  event name
async def handle_text_length_smaller_3(message: types.Message, state: FSMContext):
    assert len(message.text) <= 3
    return await message.reply(text_util.SMALLER_THAT_3_SYMBOLS,
                               reply_markup=go_to_main_menu())


async def handle_event_name(message: types.Message, state: FSMContext):
    """
    next statement - event title
    """
    statement = await states.client.EventForm.next()
    assert statement == states.client.EventForm.event_title.state, "invalid state"
    await state.update_data(event_name=message.text)

    await message.reply(text_util.OK_FOR_HANDLE_NAME,
                        reply_markup=go_to_main_menu())


# endregion event name


# region event title

async def handle_event_title(message: types.Message, state: FSMContext):
    """
    next statement - description
    """
    statement = await states.client.EventForm.next()
    assert statement == states.client.EventForm.description.state, "invalid state"
    await state.update_data(event_title=message.text)
    await message.reply(text_util.OK_FOR_HANDLE_TITLE,
                        reply_markup=go_to_main_menu())


# endregion event title
# region description
async def handle_description(message: types.Message, state: FSMContext):
    """
    next statement -
    """
    statement = await states.client.EventForm.next()
    assert statement == states.client.EventForm.media.state, "invalid state"
    await state.update_data(description=message.text)
    await message.reply(text_util.OK_FOR_HANDLE_DESCRIPTION,
                        reply_markup=go_to_main_menu())


# endregion
# region handle photo
async def handle_invalid_photo(message: types.Message, state: FSMContext):
    await message.reply(text_util.ERROR_WITH_MEDIA,
                        reply_markup=go_to_main_menu())


async def handle_photo(message: types.Message, state: FSMContext):
    unique_id = useful_methods.retrieve_message_unique_id(message, client_bot)
    logging.info(unique_id)
    # solved save photo in group
    result = await client_bot.send_photo(config.MEDIA_GROUP_ID, photo=unique_id)
    if result:

        statement = await states.client.EventForm.next()
        assert statement == states.client.EventForm.end_date.state
        await state.update_data(media=unique_id)
        logging.info('message saved')
        await message.reply(f'{text_util.PHOTO_SAVED} {config.date_format_human}',
                            reply_markup=keyboards.r_snippets.main_menu_and_skip())
        await message.delete()
    else:
        logging.warning('message not saved')
        await message.reply(text_util.PHOTO_NOT_SAVED,
                            reply_markup=go_to_main_menu())
        await message.delete()


async def handle_end_date(message: types.Message, state: FSMContext):
    # solved validate data

    date = useful_methods.try_get_date_from_str(message.text, config.date_format)
    # if date is not valid and not skip
    if date is None and message.text != config.SKIP:
        await message.reply(f'{text_util.DATE_INVALID} {config.date_format_human}\n')
    else:
        # date valid
        if message.text == config.SKIP:
            date = None

        statement = await state.get_state()
        if statement is None:
            return

        await state.update_data(end_date=date)
        logging.info(f'finish statement: {statement}')
        event = await save_state_info(message, state)
        if isinstance(event, db.Event):
            await client_bot.send_photo(chat_id=event.event_owner_id,
                                        photo=event.get_media(),
                                        caption=f'{event.stringify()}\n{text_util.EVENT_CREATED}',
                                        reply_markup=go_to_main_menu())
        await state.finish()


async def save_state_info(message: types.Message, state: FSMContext):
    """
    save received info to database
    """
    async with state.proxy() as data:
        event_name = data['event_name']
        event_title = data['event_title']
        description = data['description']
        media = data['media']  # photo unique id
        end_date = data['end_date']

        user = db.User()
        user.chat_id = message.chat.id
        user.user_fullname = useful_methods.get_full_user_name(message)
        user.in_chat_client = False
        user.in_chat_service = False

        event = db.Event()
        event.ev_name = event_name
        event.title = event_title
        event.description = description
        event.media = media
        event.end_date = end_date
        event.event_owner = user
        event.event_owner_id = message.chat.id

        event.save()

        return event


# endregion handle photo

# region cancel add event
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    logging.info(f'Cancelling state {current_state}')
    return await views.handle_start(message)

# endregion cancel add event
