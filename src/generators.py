from typing import Union


def filter_by_currency(transactions: list[dict[str, int]], currency: str) -> Union[list[dict[str, int]], list[None], str]:
    """Функция, фильтрующая список словарей с транзакциями по указанной валюте"""
    if transactions is None:
        return "Не передан список словарей с транзакциями"
    elif len(transactions) == 0:
        return "Список не содержит ни одной транзакции"

    for i, e in enumerate(transactions):
        if not isinstance(transactions[i], dict):
            print(f"""Найдена транзакция не в словаре:
{e}""")
            return "Детали транзакций должны находиться в словарях. 1 словарь = 1 транзакция"
