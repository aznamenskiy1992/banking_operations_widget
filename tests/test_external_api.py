from unittest.mock import patch

from src.external_api import convert_currency


@patch("requests.get")
def test_get_success_response_for_convert_currency(mock_get):
    """Тестирует успешный ответ от API конвертации валют"""
    response_data = {
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

    mock_get.return_value.json.return_value = response_data
    assert convert_currency("USD", 10.2) == response_data
    mock_get.assert_called_once_with("https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=10.2")
