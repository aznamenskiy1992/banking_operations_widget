import pytest


from src.filter_transactions import process_bank_search


@pytest.mark.parametrize(
    "search_str, out_data",
    [
        (
            "организации",
            [
                {
                    "id": 939719570,
                    "state": "EXECUTED",
                    "date": "2018-06-30T02:08:58.425572",
                    "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод организации",
                    "from": "Счет 75106830613657916952",
                    "to": "Счет 11776614605963066702",
                },
                {
                    "id": 594226727,
                    "state": "CANCELED",
                    "date": "2018-09-12T21:27:25.241689",
                    "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
                    "description": "Перевод организации",
                    "from": "Visa Platinum 1246377376343588",
                    "to": "Счет 14211924144426031657",
                },
            ]
        ),
        (
            "с карты",
            [
                {
                    "id": 895315941,
                    "state": "EXECUTED",
                    "date": "2018-08-19T04:27:37.904916",
                    "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод с карты на карту",
                    "from": "Visa Classic 6831982476737658",
                    "to": "Visa Platinum 8990922113665229",
                },
            ]
        ),
        (
            "счет",
            [
                {
                    "id": 142264268,
                    "state": "EXECUTED",
                    "date": "2019-04-04T23:20:05.206878",
                    "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод со счета на счет",
                    "from": "Счет 19708645243227258542",
                    "to": "Счет 75651667383060284188",
                },
                {
                    "id": 873106923,
                    "state": "EXECUTED",
                    "date": "2019-03-23T01:09:46.296404",
                    "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
                    "description": "Перевод со счета на счет",
                    "from": "Счет 44812258784861134719",
                    "to": "Счет 74489636417521191160",
                },
            ]
        ),
        (
            "перевод с",
            [
                {
                    "id": 142264268,
                    "state": "EXECUTED",
                    "date": "2019-04-04T23:20:05.206878",
                    "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод со счета на счет",
                    "from": "Счет 19708645243227258542",
                    "to": "Счет 75651667383060284188",
                },
                {
                    "id": 873106923,
                    "state": "EXECUTED",
                    "date": "2019-03-23T01:09:46.296404",
                    "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
                    "description": "Перевод со счета на счет",
                    "from": "Счет 44812258784861134719",
                    "to": "Счет 74489636417521191160",
                },
                {
                    "id": 895315941,
                    "state": "EXECUTED",
                    "date": "2018-08-19T04:27:37.904916",
                    "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод с карты на карту",
                    "from": "Visa Classic 6831982476737658",
                    "to": "Visa Platinum 8990922113665229",
                },
            ]
        )
    ]
)
def test_return_filtered_operation_for_process_bank_search(example_input_transactions_for_for_filter_by_currency_and_transaction_descriptions, search_str, out_data):
    """Тестирует возврат отфильтрованного списка словарей с операциями"""
    result = process_bank_search(example_input_transactions_for_for_filter_by_currency_and_transaction_descriptions, search_str)
    assert result == out_data


def test_empty_out_data_for_process_bank_search(example_input_transactions_for_for_filter_by_currency_and_transaction_descriptions):
    """Тестирует кейс, когда в ключе description нет вхождения искомой строки"""
    result = process_bank_search(example_input_transactions_for_for_filter_by_currency_and_transaction_descriptions, "!")
    assert result == []


def test_not_description_in_dict_for_process_bank_search(example_input_transactions_without_need_key_for_for_filter_by_currency_and_transaction_descriptions, capsys):
    """Тестирует кейс, когда в словарях нет ключа description"""
    result = process_bank_search(example_input_transactions_without_need_key_for_for_filter_by_currency_and_transaction_descriptions, "перевод с")

    captured = capsys.readouterr()
    assert captured.out == "ID операций без ключа description: 939719570, 895315941"

    assert result == [
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        }
    ]


@pytest.mark.parametrize(
    "input_data, search_str, raise_message",
    [
        ({"test",}, "перевод с", "Операции должны быть переданы, как список словарей"),
        (None, "перевод с", "Список операций не передан"),
        ([], ["перевод с"], "Строка для поиска описания операция должна быть передана в формате str"),
        ([], None, "Строка для поиска описания операций не передана")
    ]
)
def test_args_in_incorrect_type_for_process_bank_search(input_data, search_str, raise_message):
    """Тестирует кейс, когда аргументы переданые в неправильных типах"""
    with pytest.raises(TypeError) as exc_info:
        process_bank_search(input_data, search_str)
    assert str(exc_info.value) == raise_message


def test_input_empty_list_for_process_bank_search():
    """Тестирует кейс, когда передан пустой список транзакций"""
    result = process_bank_search([], "перевод с")
    assert result == []
