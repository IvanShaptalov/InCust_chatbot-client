import pytest

from tests import conftest
from utils import messenger

base_sender = None


@pytest.mark.messenger
def test_instance_creating(event_id, chat_id):
    global base_sender
    """cover base __init__, _get_event, _get_sender"""
    base_sender = messenger.BaseSender(sender_id=chat_id, event_id=event_id)
    return base_sender


@pytest.mark.messenger
def test_prepare_to_send(event_id, chat_id):
    """ cover BaseSender.prepare_to_send"""
    global base_sender
    if base_sender is None:
        base_sender = test_instance_creating(event_id, chat_id)
    assert isinstance(base_sender, messenger.BaseSender)
    result = base_sender.prepare_to_send()
    assert isinstance(result, str), "result is not str"
