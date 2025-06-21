import json
import logging
import os
from json import JSONDecodeError
from unittest.mock import mock_open, patch

import pytest

from src.utils import get_amount, get_transactions


def test_get_transactions(caplog):
    """Тестирует выдачу банковских операций из JSON файла"""
    caplog.set_level(logging.DEBUG)

    # Создаём фейковые данные
    fake_json_data = [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {"amount": "8221.37", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560",
        },
        {
            "id": 667307132,
            "state": "EXECUTED",
            "date": "2019-07-13T18:51:29.313309",
            "operationAmount": {"amount": "97853.86", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод с карты на счет",
            "from": "Maestro 1308795367077170",
            "to": "Счет 96527012349577388612",
        },
    ]
    fake_json_str = json.dumps(fake_json_data)

    with patch("builtins.open", mock_open(read_data=fake_json_str)) as mocked_open:
        result = get_transactions("operations.json")

    assert result == fake_json_data
    mocked_open.assert_called_once_with("operations.json", "r", encoding="utf-8")

    assert "Попытка открытия JSON файла с банковскими операциями" in caplog.text
    assert "Попытка получить данные из JSON файла с банковскими операциями" in caplog.text
    assert "Возврат загруженных банковских операций" in caplog.text

    assert len(caplog.records) == 3
    assert caplog.records[0].levelname == "INFO"
    assert caplog.records[1].levelname == "INFO"
    assert caplog.records[2].levelname == "INFO"


def test_incorrect_path_to_operations_json(caplog):
    """Тестирует обработку кейса, когда указан некорректный путь до файла с банковскими операциями"""
    caplog.set_level(logging.DEBUG)

    assert (
        get_transactions(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "operations.json"))
        == []
    )

    assert "JSON файл с банковскими операциями не найден" in caplog.text
    assert "Возврат пустого списка" in caplog.text

    assert len(caplog.records) == 3
    assert caplog.records[0].levelname == "INFO"
    assert caplog.records[1].levelname == "ERROR"
    assert caplog.records[2].levelname == "INFO"


def test_not_list_in_operations_json(caplog):
    """Тестирует обработку кейса, когда в файле с банковскими операциями данные содержутся не в списке"""
    caplog.set_level(logging.DEBUG)

    fake_json_data = []
    fake_json_str = json.dumps(
        (
            {
                "id": 667307132,
                "state": "EXECUTED",
                "date": "2019-07-13T18:51:29.313309",
                "operationAmount": {"amount": "97853.86", "currency": {"name": "руб.", "code": "RUB"}},
                "description": "Перевод с карты на счет",
                "from": "Maestro 1308795367077170",
                "to": "Счет 96527012349577388612",
            }
        )
    )

    with patch("builtins.open", mock_open(read_data=fake_json_str)) as mocked_open:
        result = get_transactions("operations.json")

    assert result == fake_json_data
    mocked_open.assert_called_once_with("operations.json", "r", encoding="utf-8")

    assert "Банковские операции в JSON файле находятся не в списке" in caplog.text
    assert "Возврат пустого списка" in caplog.text

    assert len(caplog.records) == 4
    assert caplog.records[2].levelname == "ERROR"
    assert caplog.records[3].levelname == "INFO"


def test_empty_operations_json(caplog):
    """Тестирует обработку кейса, когда файл с банковскими операциями пустой"""
    caplog.set_level(logging.DEBUG)

    fake_json_data = []
    fake_json_str = json.dumps(fake_json_data)

    with patch("builtins.open", mock_open(read_data=fake_json_str)) as mocked_open:
        result = get_transactions("operations.json")

    assert result == fake_json_data
    mocked_open.assert_called_once_with("operations.json", "r", encoding="utf-8")

    assert "JSON файл с банковскими операциями пустой" in caplog.text
    assert "Возврат пустого списка" in caplog.text

    assert len(caplog.records) == 4

    assert caplog.records[2].levelname == "ERROR"
    assert caplog.records[3].levelname == "INFO"


def test_decode_error_to_json_data(caplog):
    """Тестирует обработку кейса, когда в файле содержатся данные, которые невозможно декодировать"""
    caplog.set_level(logging.DEBUG)

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

    assert "Ошибка декодирования данных в JSON" in caplog.text

    assert len(caplog.records) == 3

    assert caplog.records[2].levelname == "CRITICAL"


@pytest.mark.parametrize(
    "operations, result",
    [
        (
            {
                "id": 41428829,
                "state": "EXECUTED",
                "date": "2019-07-03T18:35:29.512364",
                "operationAmount": {"amount": "8221.37", "currency": {"name": "руб.", "code": "RUB"}},
                "description": "Перевод организации",
                "from": "MasterCard 7158300734726758",
                "to": "Счет 35383033474447895560",
            },
            8221.37,
        ),
        (
            {
                "id": 41428829,
                "state": "EXECUTED",
                "date": "2019-07-03T18:35:29.512364",
                "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
                "description": "Перевод организации",
                "from": "MasterCard 7158300734726758",
                "to": "Счет 35383033474447895560",
            },
            31957.58,
        ),
    ],
)
def test_get_amount_for_get_amount(operations, result, caplog):
    """Функция возвращает сумму транзакции из операции"""
    caplog.set_level(logging.DEBUG)

    assert get_amount(operations) == result

    assert "Возврат суммы транзакции" in caplog.text

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "INFO"


@pytest.mark.parametrize(
    "operations, error_message",
    [
        (
            {
                "id": 41428829,
                "state": "EXECUTED",
                "date": "2019-07-03T18:35:29.512364",
                "amount": "8221.37",
                "currency": {"name": "руб.", "code": "RUB"},
                "description": "Перевод организации",
                "from": "MasterCard 7158300734726758",
                "to": "Счет 35383033474447895560",
            },
            "Нет ключа operationAmount",
        ),
        (
            {
                "id": 41428829,
                "state": "EXECUTED",
                "date": "2019-07-03T18:35:29.512364",
                "operationAmount": {"currency": {"name": "руб.", "code": "RUB"}},
                "description": "Перевод организации",
                "from": "MasterCard 7158300734726758",
                "to": "Счет 35383033474447895560",
            },
            "Нет ключа amount",
        ),
        (
            {
                "id": 41428829,
                "state": "EXECUTED",
                "date": "2019-07-03T18:35:29.512364",
                "operationAmount": {"amount": "31957.58", "name": "руб.", "code": "RUB"},
                "description": "Перевод организации",
                "from": "MasterCard 7158300734726758",
                "to": "Счет 35383033474447895560",
            },
            "Нет ключа currency",
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
                    },
                },
                "description": "Перевод организации",
                "from": "MasterCard 7158300734726758",
                "to": "Счет 35383033474447895560",
            },
            "Нет ключа code",
        ),
    ],
)
def test_not_need_key_in_dict_for_get_amount(operations, error_message, caplog):
    """Тестирует обработку кейса, когда в словаре с операцией нет нужных ключей"""
    caplog.set_level(logging.DEBUG)

    with pytest.raises(KeyError) as exc_info:
        get_amount(operations)
    assert str(exc_info.value) == f"'{error_message}'"

    assert "Нет нужного ключа в словаре транзакций"

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "CRITICAL"


def test_cant_convert_to_float_for_get_amount(caplog):
    """Тестирует обработку кейса, когда значение в ключе amount не конвертируется во float"""
    caplog.set_level(logging.DEBUG)

    incorrect_operations = {
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "operationAmount": {"amount": "31957 58", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "MasterCard 7158300734726758",
        "to": "Счет 35383033474447895560",
    }
    with pytest.raises(ValueError) as exc_info:
        get_amount(incorrect_operations)
    assert str(exc_info.value) == "Сумма транзакции указана в нечисловом формате"

    assert "Сумма транзакции не преобразуется в float" in caplog.text

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "CRITICAL"


def test_not_dict_for_get_amount(caplog):
    """Тестирует обработку кейса, когда операция передаётся не в словаре"""
    caplog.set_level(logging.DEBUG)

    incorrect_operations = [
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {"amount": "31957 58", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560",
        }
    ]
    with pytest.raises(TypeError) as exc_info:
        get_amount(incorrect_operations)
    assert str(exc_info.value) == "Транзакция должна быть передана в словаре"

    assert "Транзакция получена не в словаре" in caplog.text

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "CRITICAL"


def test_get_amount_with_convert_to_rub_for_get_amount(caplog):
    """Тестирует возврат суммы транзакции из операции с конвертацией в рубли из иностранной валюты"""
    caplog.set_level(logging.DEBUG)

    with patch("src.utils.convert_currency") as mock_convert_currency:
        mock_convert_currency.return_value = 799.603939

        result = get_amount(
            {
                "id": 41428829,
                "state": "EXECUTED",
                "date": "2019-07-03T18:35:29.512364",
                "operationAmount": {"amount": "10.2", "currency": {"name": "USD", "code": "USD"}},
                "description": "Перевод организации",
                "from": "MasterCard 7158300734726758",
                "to": "Счет 35383033474447895560",
            }
        )

        assert result == 799.603939

        mock_convert_currency.assert_called_once_with("USD", 10.2)

        assert "Возврат суммы транзакции с конвертацией в рубли" in caplog.text

        assert len(caplog.records) == 1
        assert caplog.records[0].levelname == "INFO"
