from models import db
from utils import useful_methods


def user_in_chat(receiver_chat_id, sender_chat_id):
    """
    This filter works from client bot to service where receiver in client bot and sender in service chatbot
    :param receiver_chat_id: telegram user chat id receiver from client chatbot
    :param sender_chat_id: sender send info from service bot
    :return: boolean
    """
    receiver_user = db.get_from_db_multiple_filter(db.User, [db.User.chat_id == receiver_chat_id])
    sender_user = db.get_from_db_multiple_filter(db.User, [db.User.chat_id == sender_chat_id])

    if isinstance(receiver_user, db.User) and isinstance(sender_user, db.User):
        result = useful_methods.check_hash_valid(sender_user.chat_hash, receiver_user.chat_hash)
        return result
    return False
