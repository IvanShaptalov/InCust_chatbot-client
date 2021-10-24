# todonext refactor, create tests
from aiogram import types

from models import db
from utils import useful_methods


def user_in_chat(chat_id):
    user = db.get_from_db_multiple_filter(db.User, [db.User.chat_id == chat_id])
    if isinstance(user, db.User):
        return user.in_chat
    return False


def event_is_removed(event_id, data):
    # todo create event
    # event_id = useful_methods.get_id_from_data(callback.data, 1)
    pass

# class MyFilter(BoundFilter):
#     key = 'is_admin'
#
#     def __init__(self, is_admin):
#         self.is_admin = is_admin
#
#     async def check(self, message: types.Message):
#         pass
#         # todo check that user is admin
#
#
# dp.filters_factory.bind(MyFilter)
