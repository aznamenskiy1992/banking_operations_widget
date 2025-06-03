import pytest


@pytest.fixture
def none_card_and_account_number():
    """Фикстура возвращает стандартное сообщение об ошибке, когда номер карты/счёта не указан (None)."""
    return "Не указан номер карты или счёта"


@pytest.fixture
def none_standard_card_and_account_number():
    """Фикстура возвращает сообщение об ошибке для некорректной длины номера карты/счёта."""
    return "Указан некорректный номер карты или счёта. Проверьте количество цифр"


@pytest.fixture
def card_and_account_number_str_symbols_not_int():
    """Фикстура возвращает сообщение об ошибке, когда номер содержит нецифровые символы."""
    return "Номер карты или счёта должен состоять только из цифр"


@pytest.fixture
def card_and_account_number_other_incorrect_types():
    """Фикстура возвращает сообщение об ошибке для нецелочисленных типов данных номера."""
    return "Номер карты или счёта должен быть целым числом"


@pytest.fixture
def card_and_account_number_incorrect_types():
    """Фикстура возвращает форматированное сообщение об ошибке для некорректного строкового ввода.
    Содержит примеры правильного формата для карты и счёта."""
    return """Номер карты или счёта должен быть строкой.
    Маска ввода:
    Для счёта - 'Счёт 79053641285349013572'
    Для Карты - 'Visa Classic 5543812355785'"""


@pytest.fixture
def not_have_date():
    """Фикстура возвращает сообщение об ошибке для отсутствующей или неверно форматированной даты.
    Указывает требуемый формат YYYY-MM-DD."""
    return "Дата не указана или указана неверно. Формат ввода даты YYYY-MM-DD"


@pytest.fixture
def none_date():
    """Фикстура возвращает сообщение об ошибке, когда дата не указана (None)."""
    return "Дата не указана"


@pytest.fixture
def example_input_transactions_for_for_filter_by_currency_and_transaction_descriptions():
    """Фикстура передаёт список транзакций в функции filter_by_currency и transaction_descriptions"""
    transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        },
    ]
    return transactions


@pytest.fixture
def example_input_transactions_without_need_key_for_for_filter_by_currency_and_transaction_descriptions():
    """Фикстура передаёт список транзакций в функции filter_by_currency и transaction_descriptions без необходимых ключей"""
    transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
            },
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
            },
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        }
    ]
    return transactions
