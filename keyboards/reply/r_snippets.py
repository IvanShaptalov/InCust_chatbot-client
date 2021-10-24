from aiogram import types

from data import config
from keyboards.reply import default_reply_markup


def main_menu() -> types.ReplyKeyboardMarkup:
    return default_reply_markup().add(config.CATALOG, config.ADD_EVENT)


def remove() -> types.ReplyKeyboardRemove:
    return types.ReplyKeyboardRemove()


def go_to_main_menu() -> types.ReplyKeyboardMarkup:
    return default_reply_markup().add(config.MAIN_MENU)


def main_menu_and_skip() -> types.ReplyKeyboardMarkup:
    return go_to_main_menu().add(config.SKIP)


def exit_from_chat_or_show_event() -> types.ReplyKeyboardMarkup:
    return default_reply_markup().add(config.EXIT_FROM_CHAT, config.SHOW_EVENT_IN_CHAT)
