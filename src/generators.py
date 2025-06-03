from typing import Union, Iterator


def filter_by_currency(transactions: list[dict[str, int]], currency: str) -> Union[Iterator[dict[str, int]], str]:
    """Функция, фильтрующая список словарей с транзакциями по указанной валюте"""
    if transactions is None:
        raise ValueError("Не передан список словарей с транзакциями")
    elif len(transactions) == 0:
        raise ValueError("Список не содержит ни одной транзакции")

    if currency is None:
        raise ValueError("Вместо валюты транзакций передано None. должно быть str")
    elif len(currency) == 0:
        raise ValueError("Вместо валюты транзакций передана пустая строка")
    elif not isinstance(currency, str):
        raise TypeError("Валюта транзакций передана не в str")

    for i, e in enumerate(transactions):
        if not isinstance(transactions[i], dict):
            print(f"""Найдена транзакция, переданная не в типе dict:
{e}
Тип, в котором передана транзакция {type(transactions[i])}""")
            raise TypeError("Детали транзакций должны находиться в словарях. 1 словарь = 1 транзакция")

    filtered_transactions: list[dict[str, int]] = list(filter(lambda item: item.get("operationAmount", {}).get("currency", {}).get("name") == currency, transactions))

    for transaction in filtered_transactions:
        yield transaction
