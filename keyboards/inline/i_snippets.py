from aiogram import types

import filters
import keyboards
from data import config
from keyboards.inline import inline_button


def sure_inline_keyboard(event_id: int) -> types.InlineKeyboardButton:
    return types.InlineKeyboardMarkup(). \
        add(
        inline_button(config.YES, f'{config.YES}:{event_id}'),
        inline_button(config.NO, f'{config.NO}:')
    )


def in_chat_inline_keyboard(event_id: int, chat_id: str) -> types.InlineKeyboardButton:
    if not filters.filters.user_in_chat(chat_id):
        return types.InlineKeyboardMarkup(). \
            add(
            inline_button(config.YES, f'{config.YES}:{event_id}'),
            inline_button(config.NO, f'{config.NO}:')
        )
