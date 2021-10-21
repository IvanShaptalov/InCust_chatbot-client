from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

storage = MemoryStorage()


class ClientForm(StatesGroup):
    event_name = State()
    event_title = State()
    description = State()
    media = State()
    end_date = State()  # can be empty


class Menu(StatesGroup):
    start_menu = State()
    catalog = State()
    add_client = ClientForm()
    chat = State()
