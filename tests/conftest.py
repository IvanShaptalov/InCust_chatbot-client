import pytest


@pytest.fixture
def invalid_key():
    return "aboba"


@pytest.fixture
def invalid_filter_params():
    return ['aboba', '100,100,100', '12-12-12', '-2, 10-50, 100-200', '-22, -2--200', '-100-599', '3, 10-50, hello']


@pytest.fixture
def valid_filter_params():
    return ['1,10-50, 100-200', '2, 20 - 10, 300-150', '0, 10-40, 1000-1', '3, 19-27, 400-200']


@pytest.fixture
def filter_params(invalid_filter_params, valid_filter_params):
    return invalid_filter_params + valid_filter_params
