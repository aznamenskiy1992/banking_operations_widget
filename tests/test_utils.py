import json
import os

import pytest
from unittest.mock import patch
from unittest.mock import mock_open

from src.utils import get_transactions


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
                    "name": "USD",
                    "code": "USD"
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
