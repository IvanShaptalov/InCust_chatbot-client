import pytest
from icecream import ic

# py.test -m call_data -v


@pytest.mark.config
def test_config_valid():
    try:
        import settings
        print(settings.protocol)
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
