from typing import Union


def filter_by_state(
    source_data: list[dict[str, Union[str, int]]], state: str = "EXECUTED"
) -> Union[list[dict[str, Union[str, int]]], str]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    Функция принимает список словарей и возвращает только те словари,
    у которых значение ключа 'state' совпадает с заданным.
    Также обрабатывает возможные ошибки и крайние случаи.

    Args:
        source_data: Список словарей для фильтрации. Каждый словарь должен содержать ключ 'state'.
        state: Значение состояния для фильтрации. По умолчанию "EXECUTED".

    Returns:
        Отфильтрованный список словарей или строку с сообщением об ошибке:
        - Если source_data is None - возвращает "Не указан список словарей"
        - Если в словарях нет ключа 'state' - возвращает "В словарях нет ключа 'state'"
        - Если нет совпадений по state - возвращает "Нет словарей со значением state"
        - В случае успеха - возвращает отфильтрованный список словарей
    """
    # Проверка на None входных данных
    if source_data is None:
        return "Не указан список словарей"

    try:
        # Фильтрация словарей по значению state с обработкой возможного исключения KeyError
        filtered_data = list(filter(lambda data: data["state"] == state, source_data))
    except:
        # Обработка случая, когда в словарях отсутствует ключ 'state'
        return "В словарях нет ключа 'state'"
    else:
        # Проверка на пустой результат фильтрации
        if len(filtered_data) == 0:
            return "Нет словарей со значением state"
        else:
            # Возврат успешного результата фильтрации
            return filtered_data


def sort_by_date(
    source_data: list[dict[str, Union[str, int]]], sort: str = "True"
) -> list[dict[str, Union[str, int]]]:
    """Функция, которая сортирует список словарей по дате"""
    if sort.lower() == "true":
        reverse = True
    else:
        reverse = False

    try:
        sorted_data = sorted(source_data, key=lambda data: data["date"], reverse=reverse)
    except:
        return "В словарях нет ключа 'date'"
    else:
        return sorted_data
