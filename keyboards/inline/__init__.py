# inline
from aiogram import types


def inline_button(text, data) -> types.InlineKeyboardButton:
    return types.InlineKeyboardButton(text, callback_data=data)


def inline_markup(text, data) -> types.InlineKeyboardMarkup:
    """
    send pagination button to catalog
    :param text: text on button
    :param data: data on button
    :return:
    """
    return types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text, callback_data=data))
