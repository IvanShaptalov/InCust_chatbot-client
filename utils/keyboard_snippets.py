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
