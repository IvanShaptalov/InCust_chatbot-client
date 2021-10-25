import pytest

from filters.filters import user_in_chat
from models import db


@pytest.mark.config
def test_config_valid():
    try:
        from data import config
        print(config.YES)
    except KeyError as e:
        assert False, "config valid failed"


@pytest.mark.internet
def test_internet_connection():
    import requests
    google = 'https://www.google.com/'
    try:
        requests.get(google)
    except Exception as e:
        print(e)
        assert False, 'check internet connection'


@pytest.mark.filter
def test_user_in_chat_working(chat_id):
    # client chat
    db.User.set_in_chat(chat_id=chat_id, in_chat=False, service_or_client='client')
    assert user_in_chat(chat_id=chat_id, service_or_client='client') is False, "error with chat_id_client settings"
    db.User.set_in_chat(chat_id=chat_id, in_chat=True, service_or_client='client')
    assert user_in_chat(chat_id=chat_id,
                        service_or_client='client') is True, "error with client get user in client chat"

    # service chat
    db.User.set_in_chat(chat_id=chat_id, in_chat=False, service_or_client='service')
    assert user_in_chat(chat_id=chat_id, service_or_client='service') is False, "error with service chat settings"
    db.User.set_in_chat(chat_id=chat_id, in_chat=True, service_or_client='service')
    assert user_in_chat(chat_id=chat_id,
                        service_or_client='service') is True, "error with client get user in service chat"
