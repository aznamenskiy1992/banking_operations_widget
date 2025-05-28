import pytest


@pytest.fixture
def none_card_and_account_number():
    return "Не указан номер карты или счёта"


@pytest.fixture
def none_standard_card_and_account_number():
    return "Указан некорректный номер карты или счёта. Проверьте количество цифр"