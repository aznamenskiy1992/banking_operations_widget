import os

import requests
from dotenv import load_dotenv

load_dotenv()
token_for_exchange_rates_data_api = os.getenv("API_KEY_FOR_EXCHANGE_RATES_DATA")


def convert_currency(from_: str, amount: float) -> float:
    """
    Конвертирует сумму из указанной валюты в рубли по курсу Exchange Rates Data API.

    Параметры:
        from_ (str): Код исходной валюты (например, 'USD', 'EUR')
        amount (float): Сумма для конвертации

    Возвращает:
        float: Сумма в рублях после конвертации

    Исключения:
        requests.HTTPError: При ошибке запроса к API с сообщением об ошибке от сервера

    Примеры:
        >>> convert_currency('USD', 100)
        7500.50  # Пример возвращаемого значения (курс 1 USD = 75.0050 RUB)

    Примечания:
        - Для работы требуется API ключ в переменной token_for_exchange_rates_data_api
        - Используется API сервиса https://exchangeratesdataapi.com/
        - В случае ошибки возвращает сообщение об ошибке от API
    """
    # Формируем URL запроса с параметрами конвертации
    url: str = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={from_}&amount={amount}"

    # Подготавливаем данные для запроса
    payload = {}  # Пустой payload, так как все параметры передаются в URL
    headers = {"apikey": token_for_exchange_rates_data_api}  # Заголовок с API ключом

    try:
        # Отправляем GET-запрос к API
        response = requests.get(url, headers=headers, data=payload)

        # Проверяем статус ответа (вызовет исключение при кодах 4XX/5XX)
        response.raise_for_status()

        # Возвращаем результат конвертации из JSON ответа
        return response.json()["result"]

    except requests.HTTPError as exc_info:
        # При ошибке HTTP преобразуем JSON ответ с ошибкой и пробрасываем исключение
        raise requests.HTTPError(exc_info.response.json()["error"]["message"])
