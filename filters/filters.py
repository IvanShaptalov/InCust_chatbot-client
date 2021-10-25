from models import db


def user_in_chat(chat_id, service_or_client: str = 'client'):
    """

    :param chat_id: telegram user chat id
    :param service_or_client:
    :return: service_or_client: select chat, 'service' to service, 'client' to client
    """
    service = 'service'
    client = 'client'
    user = db.get_from_db_multiple_filter(db.User, [db.User.chat_id == chat_id])
    if isinstance(user, db.User):

        return user.in_chat_client if service_or_client == client else user.in_chat_service
    return False
