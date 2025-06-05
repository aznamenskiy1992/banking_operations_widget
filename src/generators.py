from typing import Any, Dict, Iterator, Union


def filter_by_currency(transactions: list[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """Функция, фильтрующая список словарей с транзакциями по указанной валюте"""
    if transactions is None:
        raise ValueError("Вместо списка словарей с транзакциями передано None. Должен быть список словарей")
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
            print(
                f"""Найдена транзакция, переданная не в типе dict:
{e}
Тип, в котором передана транзакция {type(transactions[i])}"""
            )
            raise TypeError("Детали транзакций должны находиться в словарях. 1 словарь = 1 транзакция")

    filtered_transactions: list[dict[str, int]] = list(
        filter(
            lambda item: item.get("operationAmount", {}).get("currency", {}).get("name", "").lower()
            == currency.lower(),
            transactions,
        )
    )

    for transaction in filtered_transactions:
        yield transaction


def transaction_descriptions(transactions: list[Dict[str, Any]]) -> str:
    """Функция, возвращающая описание каждой операции из списка транзакций"""
    if transactions is None:
        raise ValueError("Вместо списка словарей с транзакциями передано None. Должен быть список словарей")
    elif len(transactions) == 0:
        raise ValueError("Список не содержит ни одной транзакции")

    for i, e in enumerate(transactions):
        if not isinstance(transactions[i], dict):
            print(
                f"""Найдена транзакция, переданная не в типе dict:
{e}
Тип, в котором передана транзакция {type(transactions[i])}"""
            )
            raise TypeError("Детали транзакций должны находиться в словарях. 1 словарь = 1 транзакция")

    for i in range(len(transactions)):
        if not transactions[i].get("description"):
            continue
        else:
            yield transactions[i]["description"]


def card_number_generator(start: int, stop: int) -> str:
    pass
