from typing import Union
import os

from dotenv import load_dotenv
import requests


load_dotenv()
token_for_exchange_rates_data_api = os.getenv("API_KEY_FOR_EXCHANGE_RATES_DATA")


def convert_currency(from_: str, amount: float) -> float:
    """Функция конвертирует иностранную валюту в рубли по Exchange Rates Data API и возвращает ответ"""
    url: str = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={from_}&amount={amount}"

    payload = {}
    headers = {
      "apikey": token_for_exchange_rates_data_api
    }

    try:
        response = requests.get(url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json()["result"]
    except requests.HTTPError as exc_info:
      raise requests.HTTPError(exc_info.response.json()["error"]["message"])
