from aiogram import types
import settings


def _def_markup(resize_keyboard=True, selective=True) -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)


def main_menu() -> types.ReplyKeyboardMarkup:
    return _def_markup().add(settings.CATALOG, settings.ADD_EVENT)


def remove() -> types.ReplyKeyboardRemove:
    return types.ReplyKeyboardRemove()


def go_to_main_menu() -> types.ReplyKeyboardMarkup:
    return _def_markup().add(settings.MAIN_MENU)


def main_menu_and_skip() -> types.ReplyKeyboardMarkup:
    return go_to_main_menu().add(settings.SKIP)


def sure_keyboard() -> types.InlineKeyboardButton:
    return _def_markup().add(settings.YES, settings.NO)


# inline
def _def_inline_markup() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup()


def inline_markup(text, data) -> types.InlineKeyboardMarkup:
    """
    send pagination button to catalog
    :param text: text on button
    :param data: data on button
    :return:
    """
    return _def_inline_markup().add(types.InlineKeyboardButton(text, callback_data=data))


# todo onetime keyboard

def inline_button(text, data) -> types.InlineKeyboardButton:
    return types.InlineKeyboardButton(text, callback_data=data)
