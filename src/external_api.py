from typing import Union

import requests


def convert_currency(from_: str, amount: float) -> float:
  """Функция конвертирует иностранную валюту в рубли по Exchange Rates Data API и возвращает ответ"""
  url: str = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={from_}&amount={amount}"

  payload = {}
  headers = {
    "apikey": "my_API_key"
  }

  response = requests.get(url, headers=headers, data=payload)

  return response.json()["result"]