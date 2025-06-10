import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number, mask_number",
    [
        (5543812355785520, "5543 81** **** 5520"),  # 16 цифр
        (5543812355785, "5543 81* *** 785"),  # 13 цифр
        (554381235578552014, "5543 81** **** **2014"),  # 18 цифр
        (5543812355785520439, "5543 81** **** **** 439"),  # 19 цифр
    ],
)
def test_input_standard_card_number(card_number, mask_number):
    """Тестирует корректность маскировки стандартных номеров карт (целые числа разной длины)."""
    assert get_mask_card_number(card_number) == mask_number


def test_none_card_number():
    """Тестирует обработку None в качестве номера карты."""
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number(None)
    assert str(exc_info.value) == "Не указан номер карты или счёта"


@pytest.mark.parametrize(
    "card_number, error_message",
    [
        (123, "Указан некорректный номер карты или счёта. Проверьте количество цифр"),
        (15234820356820125369, "Указан некорректный номер карты или счёта. Проверьте количество цифр")
    ]
)
def test_none_standard_card_number(card_number, error_message):
    """Тестирует обработку номеров карт некорректной длины (слишком коротких/длинных)."""
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number(card_number)
    assert str(exc_info.value) == error_message


@pytest.mark.parametrize(
    "card_number, mask_number",
    [
        ("5543812355785520", "5543 81** **** 5520"),  # 16 цифр
        ("5543812355785", "5543 81* *** 785"),  # 13 цифр
        ("554381235578552014", "5543 81** **** **2014"),  # 18 цифр
        ("5543812355785520439", "5543 81** **** **** 439"),  # 19 цифр
    ],
)
def test_card_number_str_all_symbols_int(card_number, mask_number):
    """Тестирует корректность маскировки номеров карт, переданных как строки с цифрами."""
    assert get_mask_card_number(card_number) == mask_number


@pytest.mark.parametrize(
    "card_number, error_message",
    [
        ("5543-8123-5585-520", "Номер карты или счёта должен состоять только из цифр"),
        ("5543 812 355 785", "Номер карты или счёта должен состоять только из цифр")
    ]
)
def test_card_number_str_symbols_not_int(card_number, error_message):
    """Тестирует обработку номеров карт с нецифровыми символами (дефисы, пробелы и др.)."""
    with pytest.raises(ValueError) as exc_info:
        get_mask_card_number(card_number)
    assert str(exc_info.value) == error_message


def test_card_number_other_incorrect_types(card_and_account_number_other_incorrect_types):
    """Тестирует обработку некорректных типов данных для номера карты (списки, словари, кортежи, множества, float)."""
    assert get_mask_card_number([5543812355785520, 5543812355785]) == card_and_account_number_other_incorrect_types
    assert get_mask_card_number({"Visa": 5543812355785520}) == card_and_account_number_other_incorrect_types
    assert get_mask_card_number((5543812355785520, 5543812355785)) == card_and_account_number_other_incorrect_types
    assert get_mask_card_number({5543812355785520}) == card_and_account_number_other_incorrect_types
    assert get_mask_card_number(5543812355785520.25) == card_and_account_number_other_incorrect_types


@pytest.mark.parametrize(
    "account_number, mask_number",
    [
        (79053641285349013572, "**3572"),
        (77762358105236921456, "**1456"),
    ],
)
def test_input_account_number(account_number, mask_number):
    """Тестирует корректность маскировки стандартных номеров счетов (целые числа)."""
    assert get_mask_account(account_number) == mask_number


def test_none_account_number(none_card_and_account_number):
    """Тестирует обработку None в качестве номера счета."""
    assert get_mask_account(None) == none_card_and_account_number


def test_none_standard_account_number(none_standard_card_and_account_number):
    """Тестирует обработку номеров счетов некорректной длины (слишком коротких/длинных)."""
    assert get_mask_account(7) == none_standard_card_and_account_number
    assert get_mask_account(745205381921035742369) == none_standard_card_and_account_number
