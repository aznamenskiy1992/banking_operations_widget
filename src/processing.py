from typing import Union


def filter_by_state(
    source_data: list[dict[str, Union[str, int]]], state: str = "EXECUTED"
) -> Union[list[dict[str, Union[str, int]]], str]:
    """Функция, которая фильтрует список словарей по ключу state"""
    if source_data is None:
        return "Не указан список словарей"

    try:
        filtered_data = list(filter(lambda data: data["state"] == state, source_data))
    except:
        return "В словарях нет ключа 'state'"
    else:
        if len(filtered_data) ==0:
            return "Нет словарей со значением state"
        else:
            return filtered_data


def sort_by_date(
    source_data: list[dict[str, Union[str, int]]], sort: str = "True"
) -> list[dict[str, Union[str, int]]]:
    """Функция, которая сортирует список словарей по дате"""
    if sort.lower() == "true":
        reverse = True
    else:
        reverse = False
    return sorted(source_data, key=lambda data: data["date"], reverse=reverse)
