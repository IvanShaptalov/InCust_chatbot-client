import datetime

from aiogram import types, Bot
from aiogram.types import PhotoSize

from models import db


def get_full_user_name(message: types.Message) -> str:
    """get user fullname from message"""
    if message.from_user:
        pre_fn = message.from_user.first_name
        pre_ln = message.from_user.last_name
        first_name = pre_fn if pre_fn else ' '
        last_name = pre_ln if pre_ln else ' '
        return f'{first_name} {last_name}'
    else:
        return ''


def get_event(callback):
    event_id = get_id_from_data(callback.data, 1)
    event = db.get_from_db_multiple_filter(db.Event, [db.Event.id == event_id])
    if isinstance(event, db.Event):
        return event


def retrieve_message_unique_id(message: types.Message, bot: Bot):
    photo = message.photo[0]
    assert isinstance(photo, PhotoSize)
    # solved send photo.file_id
    photo_file_id = photo.file_id
    return photo_file_id


def try_get_date_from_str(from_date, date_format):
    # upper_bound date to include current day
    try:
        date_from = datetime.datetime.strptime(from_date, date_format)
        if date_from < datetime.datetime.now():
            # if start day bigger than end_date raise error
            raise ValueError()
    except ValueError as e:
        return None
    else:
        return date_from


def get_id_from_data(data: str, index):
    """
    get id from data
    :param data: data from callback
    :param index: index of information
    """
    assert ':' in data
    return data.split(':')[index]


def format_hast(first_chat_id, second_chat_id, event_id):
    """generate chat_hash"""
    return f"{first_chat_id}-{second_chat_id}-{event_id}"


def check_hash_valid(chat_hash1, chat_hash2):
    """
    check if two users in one chat
    chat hash consist 1 chat id, 2 chat id and event id
    :param chat_hash1: chat_id of first user
    :param chat_hash2: chat_id of second user
    :return:
    """
    if chat_hash1 is None or chat_hash2 is None:
        return False
    chat11, chat12, event_id1 = chat_hash1.split('-')
    chat21, chat22, event_id2 = chat_hash2.split('-')

    in_chat = sorted([chat11, chat12]) == sorted([chat21, chat22]) and event_id1 == event_id2
    return in_chat

