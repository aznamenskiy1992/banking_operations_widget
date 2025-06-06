from typing import Any, Dict, Iterator


def filter_by_currency(transactions: list[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует список транзакций по указанной валюте и возвращает итератор по подходящим транзакциям.

    Параметры:
        transactions: list[Dict[str, Any]] - список словарей, где каждый словарь содержит информацию о транзакции.
            Каждая транзакция должна содержать информацию о валюте в поле 'operationAmount.currency.name'.
        currency: str - код валюты (например, "USD", "EUR"), по которой нужно отфильтровать транзакции.
            Сравнение происходит без учета регистра.

    Возвращает:
        Iterator[Dict[str, Any]]: итератор по словарям с транзакциями, где валюта соответствует заданной.

    Исключения:
        ValueError: Возникает в следующих случаях:
            - передан None вместо списка транзакций
            - передан пустой список транзакций
            - передан None вместо валюты
            - передан пустая строка в качестве валюты
        TypeError: Возникает в следующих случаях:
            - валюта передана не в виде строки
            - хотя бы одна транзакция передана не в виде словаря
    """
    # Проверка корректности входных данных: список транзакций
    if transactions is None:
        raise ValueError("Вместо списка словарей с транзакциями передано None. Должен быть список словарей")
    elif len(transactions) == 0:
        raise ValueError("Список не содержит ни одной транзакции")

    # Проверка корректности входных данных: валюта
    if currency is None:
        raise ValueError("Вместо валюты транзакций передано None. должно быть str")
    elif len(currency) == 0:
        raise ValueError("Вместо валюты транзакций передана пустая строка")
    elif not isinstance(currency, str):
        raise TypeError("Валюта транзакций передана не в str")

    # Проверка, что все транзакции переданы в виде словарей
    for i, e in enumerate(transactions):
        if not isinstance(transactions[i], dict):
            print(
                f"""Найдена транзакция, переданная не в типе dict:
{e}
Тип, в котором передана транзакция {type(transactions[i])}"""
            )
            raise TypeError("Детали транзакций должны находиться в словарях. 1 словарь = 1 транзакция")

    # Фильтрация транзакций по валюте (без учета регистра)
    filtered_transactions: list[dict[str, int]] = list(
        filter(
            lambda item: item.get("operationAmount", {}).get("currency", {}).get("name", "").lower()
            == currency.lower(),
            transactions,
        )
    )

    # Возврат результата через итератор
    for transaction in filtered_transactions:
        yield transaction


def transaction_descriptions(transactions: list[Dict[str, Any]]) -> Iterator[str]:
    """
    Возвращает итератор по описаниям операций из списка транзакций.

    Параметры:
        transactions: list[Dict[str, Any]] - список словарей, где каждый словарь содержит информацию о транзакции.
            Каждая транзакция может содержать поле "description" с текстовым описанием операции.
            Если поле отсутствует, транзакция пропускается.

    Возвращает:
        Iterator[str]: итератор по строкам с описаниями транзакций. Если у транзакции нет поля "description",
            она не включается в результат.

    Исключения:
        ValueError: Возникает в следующих случаях:
            - передан None вместо списка транзакций
            - передан пустой список транзакций
        TypeError: Возникает, если хотя бы одна транзакция передана не в виде словаря.
    """
    # Проверка корректности входных данных: список транзакций
    if transactions is None:
        raise ValueError("Вместо списка словарей с транзакциями передано None. Должен быть список словарей")
    elif len(transactions) == 0:
        raise ValueError("Список не содержит ни одной транзакции")

    # Проверка, что все транзакции переданы в виде словарей
    for i, e in enumerate(transactions):
        if not isinstance(transactions[i], dict):
            print(
                f"""Найдена транзакция, переданная не в типе dict:
{e}
Тип, в котором передана транзакция {type(transactions[i])}"""
            )
            raise TypeError("Детали транзакций должны находиться в словарях. 1 словарь = 1 транзакция")

    # Извлечение описаний транзакций (если они есть)
    for i in range(len(transactions)):
        if not transactions[i].get("description"):
            continue  # Пропускаем транзакции без описания
        else:
            yield transactions[i]["description"]  # Возвращаем описание через итератор


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """
    Генерирует номера банковских карт в заданном диапазоне в формате XXXX XXXX XXXX XXXX.

    Параметры:
        start: int - начальный номер карты (должен быть положительным целым числом)
        stop: int - конечный номер карты (не может превышать 9999 9999 9999 9999)

    Возвращает:
        Iterator[str]: итератор по строкам, где каждая строка представляет номер карты
        в формате "XXXX XXXX XXXX XXXX" (16 цифр, разделенных пробелами по 4).
        Номера дополняются ведущими нулями, если число цифр меньше 16.

    Исключения:
        ValueError: Возникает в следующих случаях:
            - start или stop равно None
            - start не положительное число
            - stop превышает 9999999999999999
            - stop меньше start
        TypeError: Возникает, если start или stop не являются целыми числами.
    """
    # Проверка корректности параметра start
    if start is None:
        raise ValueError("Вместо start передано None. Должно быть целое число")
    elif not isinstance(start, int):
        print(f"start передан в типе {type(start)}")
        raise TypeError("start должен быть целым числом")
    elif start <= 0:
        raise ValueError("start должен быть > 0")

    # Проверка корректности параметра stop
    if stop is None:
        raise ValueError("Вместо stop передано None. Должно быть целое число")
    elif not isinstance(stop, int):
        print(f"stop передан в типе {type(stop)}")
        raise TypeError("stop должен быть целым числом")
    elif stop > 9999999999999999:
        raise ValueError("stop не может быть больше 9999 9999 9999 9999")

    # Проверка, что stop не меньше start
    if stop < start:
        raise ValueError("stop должен быть >= start")

    # Генерация номеров карт
    for number in range(start, stop + 1):
        # Преобразуем число в строку и дополняем ведущими нулями до 16 цифр
        number_str = str(number)
        number_temp: str = "0" * (16 - len(number_str)) + number_str

        # Форматируем номер карты: разбиваем на группы по 4 цифры
        formatted_number = " ".join([number_temp[:4], number_temp[4:8], number_temp[8:12], number_temp[12:]])

        # Возвращаем отформатированный номер через итератор
        yield formatted_number
