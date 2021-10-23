from aiogram import types

from data import config
from keyboards.inline import inline_button


def sure_inline_keyboard(event_id: int) -> types.InlineKeyboardButton:
    return types.InlineKeyboardMarkup(). \
        add(
        inline_button(config.YES, f'{config.YES}:{event_id}'),
        inline_button(config.NO, f'{config.NO}:')
    )
