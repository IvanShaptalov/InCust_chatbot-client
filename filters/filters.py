from models import db


def user_in_chat(chat_id):
    user = db.get_from_db_multiple_filter(db.User, [db.User.chat_id == chat_id])
    if isinstance(user, db.User):
        return user.in_chat
    return False
