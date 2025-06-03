import pytest

from src.generators import filter_by_currency


def test_none_list_for_filter_by_currency():
    """Тестирует обработку None в качестве списка словарей."""
    with pytest.raises(ValueError) as exc_info:
        next(filter_by_currency(None, "USD"))
    assert str(exc_info.value) == "Вместо списка словарей с транзакциями передано None. Должен быть список словарей"


def test_empty_transactions_list_for_filter_by_currency_and_transaction_descriptions():
    """Тестирует обработку кейса, когда на вход подаётся пустой список словарей с транзакциями"""
    with pytest.raises(ValueError) as exc_info:
        next(filter_by_currency([], "USD"))
    assert str(exc_info.value) == "Список не содержит ни одной транзакции"


@pytest.mark.parametrize(
    "transactions, currency, error_message",
    [
        (
            [{(939719570, 9824.07), (142264268, "EXECUTED")}],
            "USD",
            "Детали транзакций должны находиться в словарях. 1 словарь = 1 транзакция"
        ),
        (
            [(939719570, 9824.07), (142264268, "EXECUTED")],
            "USD",
            "Детали транзакций должны находиться в словарях. 1 словарь = 1 транзакция"
        )
    ]
)
def test_in_transactions_list_not_dict_for_filter_by_currency_and_transaction_descriptions(transactions, currency, error_message):
    """Тестирует обработку кейса, когда на вход подаётся список с транзакциями не в словарях"""
    with pytest.raises(TypeError) as exc_info:
        next(filter_by_currency(transactions, currency))
    assert str(exc_info.value) == error_message


def test_filter_by_currency(example_input_transactions_for_for_filter_by_currency_and_transaction_descriptions):
    """Тестирует фильтрацию транзакций по переданной валюте"""
    generator = filter_by_currency(example_input_transactions_for_for_filter_by_currency_and_transaction_descriptions, "USD")
    assert next(generator) == {
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
    }
    assert next(generator) == {
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
    }
    assert next(generator) == {
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
    }


def test_not_need_key_in_dict_for_filter_by_currency(example_input_transactions_without_need_key_for_for_filter_by_currency_and_transaction_descriptions):
    """Тестирует обработку кейса, когда в словарях нет ключей 'operationAmount', 'currency', 'name'"""
    generator = filter_by_currency(example_input_transactions_without_need_key_for_for_filter_by_currency_and_transaction_descriptions, "USD")
    assert next(generator) == {
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
    }


def test_none_currency_in_transactions_for_filter_by_currency(example_input_transactions_for_for_filter_by_currency_and_transaction_descriptions):
    """Тестирует обработку кейса, где на вход подаётся валюта в виде None"""
    with pytest.raises(ValueError) as exc_info:
        next(filter_by_currency(example_input_transactions_for_for_filter_by_currency_and_transaction_descriptions, None))
    assert str(exc_info.value) == "Вместо валюты транзакций передано None. должно быть str"


def test_empty_currency_in_transactions_for_filter_by_currency(example_input_transactions_for_for_filter_by_currency_and_transaction_descriptions):
    """Тестирует обработку кейса, где вместо валюты подаётся пустая строка"""
    with pytest.raises(ValueError) as exc_info:
        next(filter_by_currency(example_input_transactions_for_for_filter_by_currency_and_transaction_descriptions, ""))
    assert str(exc_info.value) == "Вместо валюты транзакций передана пустая строка"


@pytest.mark.parametrize(
    "transactions, currency, error_message",
    [
        ([
             {
                 "id": 939719570,
                 "state": "EXECUTED",
                 "date": "2018-06-30T02:08:58.425572",
                 "operationAmount": {
                     "amount": "9824.07",
                 },
                 "description": "Перевод организации",
                 "from": "Счет 75106830613657916952",
                 "to": "Счет 11776614605963066702"
             }
         ],
         ["USD"],
         "Валюта транзакций передана не в str"
        ),
        ([
             {
                 "id": 939719570,
                 "state": "EXECUTED",
                 "date": "2018-06-30T02:08:58.425572",
                 "operationAmount": {
                     "amount": "9824.07",
                 },
                 "description": "Перевод организации",
                 "from": "Счет 75106830613657916952",
                 "to": "Счет 11776614605963066702"
             }
         ],
         {"USD",},
         "Валюта транзакций передана не в str"
        ),
    ]
)
def test_currency_not_str_for_filter_by_currency(transactions, currency, error_message):
    """Тестирует обработку кейса, где на вход подаётся валюта транзакции не в str"""
    with pytest.raises(TypeError) as exc_info:
        next(filter_by_currency(transactions, currency))
    assert str(exc_info.value) == error_message


def test_currency_in_different_registers_for_filter_by_currency(example_input_transactions_for_for_filter_by_currency_and_transaction_descriptions):
    """Тестирует обработку кейса, где на вход подаётся валюта транзакции в нижнем регистре"""
    generator = filter_by_currency(example_input_transactions_for_for_filter_by_currency_and_transaction_descriptions, "usd")
    assert next(generator) == {
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
    }
    assert next(generator) == {
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
    }
    assert next(generator) == {
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
    }
