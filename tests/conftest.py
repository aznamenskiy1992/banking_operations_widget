import pytest


@pytest.fixture
def none_card_and_account_number():
    return "Не указан номер карты или счёта"


@pytest.fixture
def none_standard_card_and_account_number():
    return "Указан некорректный номер карты или счёта. Проверьте количество цифр"


@pytest.fixture
def card_and_account_number_str_symbols_not_int():
    return "Номер карты или счёта должен состоять только из цифр"