from aiogram import types, Bot
from icecream import ic

from utils import text_util


# region catalog


async def handle_catalog(message: types.Message, bot: Bot):
    ic('show catalog statement')
    await bot.send_message(message.chat.id,
                           text_util.CATALOG_OPENED)
    # events = Event.get_next_event()
    # print(events)
    # todonext create pagination, deletions and chat in events

# endregion catalog
