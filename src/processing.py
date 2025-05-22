from typing import Union


def filter_by_state(
    source_data: list[dict[str, Union[str, int]]], state: str = "EXECUTED"
) -> list[dict[str, Union[str, int]]]:
    """
    Получает список словарей и возвращает список словарей, у которых ключ state соответствует переданному значению
    """
    return list(filter(lambda data: data["state"] == state, source_data))
