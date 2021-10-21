from aiogram import types
import settings


def main_menu() -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(settings.CATALOG, settings.ADD_EVENT)
    return markup
