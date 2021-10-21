import logging

from aiogram import types, Bot
from aiogram.dispatcher import FSMContext
from icecream import ic

import settings
from client_chat_bot import states
from client_chat_bot.views import views
from utils import useful_methods, keyboard_snippets, text_util, db_util


async def handle_add_event(message: types.Message, bot: Bot):
    ic('add event')
    await bot.send_message(message.chat.id,
                           text_util.EVENT_CREATING_OPENED,
                           reply_markup=keyboard_snippets.go_to_main_menu())
    await states.EventForm.event_name.set()


# region  event name
async def handle_text_length_smaller_3(message: types.Message, state: FSMContext):
    assert len(message.text) <= 3
    return await message.reply(text_util.SMALLER_THAT_3_SYMBOLS,
                               reply_markup=keyboard_snippets.go_to_main_menu())


async def handle_event_name(message: types.Message, state: FSMContext):
    """
    next statement - event title
    """
    statement = await states.EventForm.next()
    assert statement == states.EventForm.event_title.state, "invalid state"
    await state.update_data(event_name=message.text)

    await message.reply(text_util.OK_FOR_HANDLE_NAME,
                        reply_markup=keyboard_snippets.go_to_main_menu())


# endregion event name


# region event title

async def handle_event_title(message: types.Message, state: FSMContext):
    """
    next statement - description
    """
    statement = await states.EventForm.next()
    assert statement == states.EventForm.description.state, "invalid state"
    await state.update_data(event_title=message.text)
    await message.reply(text_util.OK_FOR_HANDLE_TITLE,
                        reply_markup=keyboard_snippets.go_to_main_menu())


# endregion event title
# region description
async def handle_description(message: types.Message, state: FSMContext):
    """
    next statement -
    """
    statement = await states.EventForm.next()
    assert statement == states.EventForm.media.state, "invalid state"
    await state.update_data(description=message.text)
    await message.reply(text_util.OK_FOR_HANDLE_DESCRIPTION,
                        reply_markup=keyboard_snippets.go_to_main_menu())


# endregion
# region handle photo
async def handle_invalid_photo(message: types.Message, state: FSMContext):
    await message.reply(text_util.ERROR_WITH_MEDIA,
                        reply_markup=keyboard_snippets.go_to_main_menu())


async def handle_photo(message: types.Message, state: FSMContext, bot: Bot):
    unique_id = useful_methods.retrieve_message_unique_id(message, bot)
    logging.info(unique_id)
    # solved save photo in group
    result = await bot.send_photo(settings.media_group_id, photo=unique_id)
    if result:

        statement = await states.EventForm.next()
        assert statement == states.EventForm.end_date.state
        await state.update_data(media=unique_id)
        logging.info('message saved')
        await message.reply(f'{text_util.PHOTO_SAVED} {settings.date_format_human}',
                            reply_markup=keyboard_snippets.main_menu_and_skip())
        await message.delete()
    else:
        logging.warning('message not saved')
        await message.reply(text_util.PHOTO_NOT_SAVED,
                            reply_markup=keyboard_snippets.go_to_main_menu())
        await message.delete()


async def handle_end_date(message: types.Message, state: FSMContext):
    # solved validate data

    date = useful_methods.try_get_date_from_str(message.text, settings.date_format)
    # if date is not valid and not skip
    if date is None and message.text != settings.SKIP:
        await message.reply(f'{text_util.DATE_INVALID} {settings.date_format_human}\n')
    else:
        # date valid
        if message.text == settings.SKIP:
            date = 'skip'
        statement = await state.get_state()
        if statement is None:
            return
        await state.update_data(end_date=date)
        logging.info(f'finish statement: {statement}')
        await save_state_info(message, state)
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


# endregion handle photo

# region cancel add event
async def cancel_handler(message: types.Message, state: FSMContext, bot: Bot):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    logging.info(f'Cancelling state {current_state}')
    return await views.handle_start(message, bot)

# endregion cancel add event
