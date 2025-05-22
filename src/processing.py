from typing import Union


def filter_by_state(
    source_data: list[dict[str, Union[str, int]]], state: str = "EXECUTED"
) -> list[dict[str, Union[str, int]]]:
    """Функция, которая фильтрует список словарей по ключу state"""
    return list(filter(lambda data: data["state"] == state, source_data))


def sort_by_date(
    source_data: list[dict[str, Union[str, int]]], sort: str = "True"
) -> list[dict[str, Union[str, int]]]:
    """
    Сортирует словари по дате (значению ключа date)
    """
    if sort.lower() == "true":
        reverse = True
    else:
        reverse = False
    return sorted(source_data, key=lambda data: data["date"], reverse=reverse)
