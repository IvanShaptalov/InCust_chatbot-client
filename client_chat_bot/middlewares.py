from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from app import dp


class MyFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        pass
        # todo check that user is admin


dp.filters_factory.bind(MyFilter)
