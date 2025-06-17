import json
import os
from json import JSONDecodeError

import pytest
from unittest.mock import patch
from unittest.mock import mock_open

from src.utils import get_transactions, get_amount


def test_get_transactions():
    """Тестирует выдачу банковских операций из JSON файла"""

    # Создаём фейковые данные
    fake_json_data = [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589"
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {
                "amount": "8221.37",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560"
        },
        {
            "id": 667307132,
            "state": "EXECUTED",
            "date": "2019-07-13T18:51:29.313309",
            "operationAmount": {
                "amount": "97853.86",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод с карты на счет",
            "from": "Maestro 1308795367077170",
            "to": "Счет 96527012349577388612"
        }
    ]
    fake_json_str = json.dumps(fake_json_data)

    with patch("builtins.open", mock_open(read_data=fake_json_str)) as mocked_open:
        result = get_transactions("operations.json")

    assert result == fake_json_data
    mocked_open.assert_called_once_with("operations.json", "r", encoding="utf-8")


def test_incorrect_path_to_operations_json():
    """Тестирует обработку кейса, когда указан некорректный путь до файла с банковскими операциями"""
    assert get_transactions(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "operations.json")) == []


def test_not_list_in_operations_json():
    """Тестирует обработку кейса, когда в файле с банковскими операциями данные содержутся не в списке"""
    fake_json_data = []
    fake_json_str = json.dumps(
        (
            {
                "id": 667307132,
                "state": "EXECUTED",
                "date": "2019-07-13T18:51:29.313309",
                "operationAmount": {
                    "amount": "97853.86",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                },
                "description": "Перевод с карты на счет",
                "from": "Maestro 1308795367077170",
                "to": "Счет 96527012349577388612"
            }
        )
    )

    with patch("builtins.open", mock_open(read_data=fake_json_str)) as mocked_open:
        result = get_transactions("operations.json")

    assert result == fake_json_data
    mocked_open.assert_called_once_with("operations.json", "r", encoding="utf-8")


def test_empty_operations_json():
    """Тестирует обработку кейса, когда файл с банковскими операциями пустой"""
    fake_json_data = []
    fake_json_str = json.dumps(fake_json_data)

    with patch("builtins.open", mock_open(read_data=fake_json_str)) as mocked_open:
        result = get_transactions("operations.json")

    assert result == fake_json_data
    mocked_open.assert_called_once_with("operations.json", "r", encoding="utf-8")


def test_decode_error_to_json_data():
    """Тестирует обработку кейса, когда в файле содержатся данные, которые невозможно декодировать"""
    invalid_json_str = """[
        {
            "id": 667307132,
            "state": "EXECUTED"
            "date": "2019-07-13T18:51:29.313309",
            "operationAmount": {
                "amount": "97853.86",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            }
        }"""
    with patch("builtins.open", mock_open(read_data=invalid_json_str)) as mocked_open:
        with pytest.raises(JSONDecodeError) as exc_info:
            get_transactions("operations.json")

    assert str(exc_info.value) == "Невозможно декодировать данные в JSON: line 5 column 13 (char 85)"
    mocked_open.assert_called_once_with("operations.json", "r", encoding="utf-8")


@pytest.mark.parametrize(
    "operations, result", [
        (
                {
                    "id": 41428829,
                    "state": "EXECUTED",
                    "date": "2019-07-03T18:35:29.512364",
                    "operationAmount": {
                      "amount": "8221.37",
                      "currency": {
                        "name": "руб.",
                        "code": "RUB"
                      }
                    },
                    "description": "Перевод организации",
                    "from": "MasterCard 7158300734726758",
                    "to": "Счет 35383033474447895560"
                },
                8221.37
        ),
        (
                {
                    "id": 41428829,
                    "state": "EXECUTED",
                    "date": "2019-07-03T18:35:29.512364",
                    "operationAmount": {
                      "amount": "31957.58",
                      "currency": {
                        "name": "руб.",
                        "code": "RUB"
                      }
                    },
                    "description": "Перевод организации",
                    "from": "MasterCard 7158300734726758",
                    "to": "Счет 35383033474447895560"
                },
                31957.58
        )
    ]
)
def test_get_amount_for_get_amount(operations, result):
    """Функция возвращает сумму транзакции из операции"""
    assert get_amount(operations) == result


@pytest.mark.parametrize(
    "operations, error_message",
    [
        (
                {
                    "id": 41428829,
                    "state": "EXECUTED",
                    "date": "2019-07-03T18:35:29.512364",
                    "amount": "8221.37",
                    "currency": {
                      "name": "руб.",
                      "code": "RUB"
                    },
                    "description": "Перевод организации",
                    "from": "MasterCard 7158300734726758",
                    "to": "Счет 35383033474447895560"
                },
                "Нет ключа operationAmount"
        ),
        (
                {
                    "id": 41428829,
                    "state": "EXECUTED",
                    "date": "2019-07-03T18:35:29.512364",
                    "operationAmount": {
                      "currency": {
                        "name": "руб.",
                        "code": "RUB"
                      }
                    },
                    "description": "Перевод организации",
                    "from": "MasterCard 7158300734726758",
                    "to": "Счет 35383033474447895560"
                },
                "Нет ключа amount"
        )
    ]
)
def test_not_need_key_in_dict_for_get_amount(operations, error_message):
    """Тестирует обработку кейса, когда в словаре с операцией нет нужных ключей"""
    with pytest.raises(KeyError) as exc_info:
        get_amount(operations)
    assert str(exc_info.value) == f"'{error_message}'"


def test_cant_convert_to_float_for_get_amount():
    """Тестирует обработку кейса, когда значение в ключе amount не конвертируется во float"""
    incorrect_operations = {
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "operationAmount": {
            "amount": "31957 58",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод организации",
        "from": "MasterCard 7158300734726758",
        "to": "Счет 35383033474447895560"
    }
    with pytest.raises(ValueError) as exc_info:
        get_amount(incorrect_operations)
    assert str(exc_info.value) == "Сумма транзакции указана в нечисловом формате"


def test_not_dict_for_get_amount():
    """Тестирует обработку кейса, когда операция передаётся не в словаре"""
    incorrect_operations = [
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {
                "amount": "31957 58",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560"
        }
    ]
    with pytest.raises(TypeError) as exc_info:
        get_amount(incorrect_operations)
    assert str(exc_info.value) == "Транзакция должна быть передана в словаре"
