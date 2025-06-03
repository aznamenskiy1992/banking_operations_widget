from typing import Union


def filter_by_currency(transactions: list[dict[str, int]], currency: str) -> Union[list[dict[str, int]], list[None], str]:
    """Функция, фильтрующая список словарей с транзакциями по указанной валюте"""
    if transactions is None:
        return "Не передан список словарей с транзакциями"
