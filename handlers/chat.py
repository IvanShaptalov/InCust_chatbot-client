from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards
from data import text_util
from data.bot_setup import client_bot
from handlers import views
from models import db
from states.client import CatalogGroup
from utils import useful_methods, messenger


async def handle_chat_connect(callback: types.CallbackQuery, state: FSMContext):
    print(callback.data)
    if callback.data and callback.message:
        event_id = useful_methods.get_id_from_data(callback.data, 1)
        with db.session:
            event = db.get_from_db_multiple_filter(table_class=db.Event,
                                                   identifier_to_value=[db.Event.id == event_id],
                                                   open_session=db.session)
            db.session.close()
            if isinstance(event, db.Event):
                await state.update_data(event_id=event_id)
                await CatalogGroup.in_chat.set()

                db.User.set_in_chat(chat_id=callback.message.chat.id,
                                    in_chat=True,
                                    service_or_client='client',
                                    chat_event_id=event_id)
                await callback.message.reply(text_util.ENTER_IN_CHAT.format(event.title),
                                             reply_markup=keyboards.r_snippets.exit_from_chat_or_show_event())

            else:
                await callback.message.reply(text_util.EVENT_DELETED)
                return
    pass


async def leave_chat(message: types.Message, state: FSMContext):
    await state.finish()
    db.User.set_in_chat(chat_id=message.chat.id,
                        in_chat=False,
                        service_or_client='client',
                        chat_event_id=None)
    await views.handle_start(message)


async def show_event(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        event_id = int(data['event_id'])
        with db.session:

            event = db.get_from_db_multiple_filter(table_class=db.Event,
                                                   identifier_to_value=[db.Event.id == event_id],
                                                   open_session=db.session)
            if isinstance(event, db.Event):
                await client_bot.send_photo(chat_id=message.chat.id,
                                            photo=event.get_media(),
                                            caption=f'{event.stringify()}')
            else:
                await message.reply(text_util.EVENT_DELETED)
                return


# region data sending
async def send_text_message(message: types.Message, state: FSMContext):  # create class to send all type of data
    async with state.proxy() as data:
        event_id = int(data['event_id'])
        sender = messenger.TextSender(event_id=event_id,
                                      sender_id=message.chat.id)
        await sender.forward_data(message)


async def send_location(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        event_id = int(data['event_id'])
        sender = messenger.LocationSender(event_id=event_id,
                                          sender_id=message.chat.id)
        await sender.forward_data(message)


async def send_sticker(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        event_id = int(data['event_id'])
        sender = messenger.StickerSender(event_id=event_id,
                                         sender_id=message.chat.id)
        await sender.forward_data(message)


async def send_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        event_id = int(data['event_id'])
        sender = messenger.PhotoSender(event_id=event_id,
                                       sender_id=message.chat.id)
        await sender.forward_data(message)


async def send_animation(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        event_id = int(data['event_id'])
        sender = messenger.AnimationSender(event_id=event_id,
                                           sender_id=message.chat.id)
        await sender.forward_data(message)


async def send_video(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        event_id = int(data['event_id'])
        sender = messenger.VideoSender(event_id=event_id,
                                       sender_id=message.chat.id)
        await sender.forward_data(message)


async def send_audio(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        event_id = int(data['event_id'])
        sender = messenger.AudioSender(event_id=event_id,
                                       sender_id=message.chat.id)
        await sender.forward_data(message)


async def send_voice(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        event_id = int(data['event_id'])
        sender = messenger.VoiceSender(event_id=event_id,
                                       sender_id=message.chat.id)
        await sender.forward_data(message)
# endregion data sending
