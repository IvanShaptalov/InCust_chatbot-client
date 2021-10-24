import pytest

from tests.test_messenger import test_instance_creating
from utils import messenger


@pytest.fixture
def chat_id():
    return '635466458'


@pytest.fixture
def event_id():
    return -100

