from typing import Union, Iterator


def filter_by_currency(transactions: list[dict[str, int]], currency: str) -> Union[Iterator[dict[str, int]], str]:
    """Функция, фильтрующая список словарей с транзакциями по указанной валюте"""
    if transactions is None:
        yield "Не передан список словарей с транзакциями"
        return
    elif len(transactions) == 0:
        yield "Список не содержит ни одной транзакции"
        return

    for i, e in enumerate(transactions):
        if not isinstance(transactions[i], dict):
            print(f"""Найдена транзакция не в словаре:
{e}""")
            yield "Детали транзакций должны находиться в словарях. 1 словарь = 1 транзакция"
            return

    filtered_transactions: list[dict[str, int]] = list(filter(lambda item: item["operationAmount"]["currency"]["name"] == currency, transactions))

    return (item_dic for item_dic in filtered_transactions)
