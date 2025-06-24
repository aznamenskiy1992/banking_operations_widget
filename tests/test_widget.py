import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "number, mask_number",
    [
        ("Счет 79053641285349013572", "Счет **3572"),
        ("MasterCard 5543812355785520", "MasterCard 5543 81** **** 5520"),
    ],
)
def test_definition_account_and_card_number(number, mask_number):
    """Тестирует базовые случаи определения и маскировки номеров счетов и карт."""
    assert mask_account_card(number) == mask_number


@pytest.mark.parametrize(
    "card_number, mask_number",
    [
        ("Visa Classic 5543812355785", "Visa Classic 5543 81* *** 785"),  # 13 цифр
        ("Maestro 554381235578552014", "Maestro 5543 81** **** **2014"),  # 18 цифр
        ("Visa Platinum 5543812355785520439", "Visa Platinum 5543 81** **** **** 439"),  # 19 цифр
    ],
)
def test_definition_other_card_number(card_number, mask_number):
    """Тестирует определение и маскировку карт различных платежных систем с разной длиной номеров."""
    assert mask_account_card(card_number) == mask_number


@pytest.mark.parametrize(
    "account_number, mask_number",
    [
        ("Расчётный счет 79053641285349013572", "Расчётный счет **3572"),
        ("Корреспондентский счет 79053641285349013572", "Корреспондентский счет **3572"),
        ("Расчётный счёт 79053641285349013572", "Расчётный счёт **3572"),
    ],
)
def test_definition_other_account_number(account_number, mask_number):
    """Тестирует определение и маскировку счетов с разными вариантами написания (счёт/счет)."""
    assert mask_account_card(account_number) == mask_number


def test_none_card_and_account_number():
    """Тестирует обработку случая, когда на вход подается None вместо номера карты/счета."""
    with pytest.raises(ValueError) as exc_info:
        mask_account_card(None)
    assert str(exc_info.value) == "Не указан номер карты или счёта"


@pytest.mark.parametrize(
    "card_or_account_number, error_message",
    [
        (
            [5543812355785, 79053641285349013572],
            """Номер карты или счёта должен быть строкой.
    Маска ввода:
    Для счёта - 'Счёт 79053641285349013572'
    Для Карты - 'Visa Classic 5543812355785'""",
        ),
        (
            {"Visa": 5543812355785520, "Расчётный счет": 79053641285349013572},
            """Номер карты или счёта должен быть строкой.
    Маска ввода:
    Для счёта - 'Счёт 79053641285349013572'
    Для Карты - 'Visa Classic 5543812355785'""",
        ),
        (
            (5543812355785, 79053641285349013572),
            """Номер карты или счёта должен быть строкой.
    Маска ввода:
    Для счёта - 'Счёт 79053641285349013572'
    Для Карты - 'Visa Classic 5543812355785'""",
        ),
        (
            {5543812355785, 79053641285349013572},
            """Номер карты или счёта должен быть строкой.
    Маска ввода:
    Для счёта - 'Счёт 79053641285349013572'
    Для Карты - 'Visa Classic 5543812355785'""",
        ),
        (
            5543812355785.25,
            """Номер карты или счёта должен быть строкой.
    Маска ввода:
    Для счёта - 'Счёт 79053641285349013572'
    Для Карты - 'Visa Classic 5543812355785'""",
        ),
        (
            5543812355785,
            """Номер карты или счёта должен быть строкой.
    Маска ввода:
    Для счёта - 'Счёт 79053641285349013572'
    Для Карты - 'Visa Classic 5543812355785'""",
        ),
        (
            79053641285349013572,
            """Номер карты или счёта должен быть строкой.
    Маска ввода:
    Для счёта - 'Счёт 79053641285349013572'
    Для Карты - 'Visa Classic 5543812355785'""",
        ),
    ],
)
def test_card_and_account_number_incorrect_types(card_or_account_number, error_message):
    """Тестирует обработку некорректных типов данных вместо номера карты/счета:
    - Списки
    - Словари
    - Кортежи
    - Множества
    - Числа с плавающей точкой
    - Целые числа без указания типа карты/счета
    """
    with pytest.raises(TypeError) as exc_info:
        mask_account_card(card_or_account_number)
    assert str(exc_info.value) == error_message


@pytest.mark.parametrize(
    "date, convert_date",
    [
        ("2023-05-15T12:30:45", "15.05.2023"),
        ("2000-01-01T00:00:00", "01.01.2000"),
        ("0001-01-01T00:00:00", "01.01.0001"),
    ],
)
def test_convert_str_to_date_d_m_y(date, convert_date):
    """Тестирует корректное преобразование даты из формата ISO 8601 в формат DD.MM.YYYY."""
    assert get_date(date) == convert_date


def test_not_have_date():
    """Тестирует обработку случая, когда дата указана без корректной даты (только время)."""
    with pytest.raises(ValueError) as exc_info:
        get_date("T12:30:45")
    assert str(exc_info.value) == "Дата не указана или указана неверно. Формат ввода даты YYYY-MM-DD"


def test_none_date():
    """Тестирует обработку случая, когда на вход подается None вместо даты."""
    with pytest.raises(ValueError) as exc_info:
        get_date(None)
    assert str(exc_info.value) == "Дата не указана"


@pytest.mark.parametrize(
    "date, convert_date",
    [
        (" 2023-05-15 T12:30:45 ", "15.05.2023"),
        (" 2000-01-01 T00:00:00", "01.01.2000"),
    ],
)
def test_whitespace_in_date(date, convert_date):
    """Тестирует корректную обработку дат с лишними пробельными символами."""
    assert get_date(date) == convert_date
