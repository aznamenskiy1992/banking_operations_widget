from json import JSONDecodeError
from unittest.mock import patch, Mock

import pytest
import requests

from src.external_api import convert_currency


@patch("requests.get")
def test_get_success_response_for_convert_currency(mock_get):
    """Тестирует успешный ответ от API конвертации валют"""
    mock_get.return_value.json.return_value = {
        "success": True,
        "query": {
            "from": "USD",
            "to": "RUB",
            "amount": 10.2
        },
        "info": {
            "timestamp": 1750162276,
            "rate": 78.392543
        },
        "date": "2025-06-17",
        "result": 799.603939
    }

    assert convert_currency("USD", 10.2) == 799.603939

    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=10.2",
        headers={"apikey": "my_API_key"},
        data={}
    )


@patch("requests.get")
def test_http_error_for_convert_currency(mock_get):
    """Тестирует обработку HTTP Error (400-599 статусы)"""
    mock_get.return_value.status_code.return_value = 400
    mock_get.return_value.json.return_value = {
        "error": {
            "code": "invalid_conversion_amount",
            "message": "You have not specified an amount to be converted. [Example: amount=5]"
        }
    }

    with pytest.raises(requests.HTTPError) as exc_info:
        convert_currency("USD", 10.2)
    assert str(exc_info.value) == "You have not specified an amount to be converted. [Example: amount=5]"

    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=10.2",
        headers={"apikey": "my_API_key"},
        data={}
    )
