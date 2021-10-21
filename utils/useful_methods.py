from aiogram import types


def get_full_user_name(message: types.Message):
    """get user fullname from message"""
    if message.from_user:
        pre_fn = message.from_user.first_name
        pre_ln = message.from_user.last_name
        first_name = pre_fn if pre_fn else ''
        last_name = pre_ln if pre_ln else ''
        return f'{first_name} {last_name}'
    else:
        return ''
