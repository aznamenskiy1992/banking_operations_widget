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


@pytest.fixture
def card_and_account_number_other_incorrect_types():
    return "Номер карты или счёта должен быть целым числом"


@pytest.fixture
def card_and_account_number_incorrect_types():
    return """Номер карты или счёта должен быть строкой.
    Маска ввода:
    Для счёта - 'Счёт 79053641285349013572'
    Для Карты - 'Visa Classic 5543812355785'"""


@pytest.fixture
def not_have_date():
    return "Не указана дата"