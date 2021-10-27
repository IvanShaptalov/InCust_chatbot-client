from models import db


def user_in_chat_from_client_to_service(receiver_chat_id, sender_chat_id):
    """
    This filter works from client bot to service where receiver in client bot and sender in service chatbot
    :param receiver_chat_id: telegram user chat id receiver from client chatbot
    :param sender_chat_id: sender send info from service bot
    :return: boolean

    """
    receiver_user = db.get_from_db_multiple_filter(db.User, [db.User.chat_id == receiver_chat_id])
    sender_user = db.get_from_db_multiple_filter(db.User, [db.User.chat_id == sender_chat_id])

    if isinstance(receiver_user, db.User) and isinstance(sender_user, db.User):
        # dont send keyboard if receiver in chat in service, id's same and sender user in client chat
        return receiver_user.in_chat_service \
               and receiver_user.current_event_id == sender_user.current_event_id \
               and sender_user.in_chat_client

    return False
