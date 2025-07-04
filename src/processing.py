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
        raise ValueError("Не указан список словарей")

    try:
        # Фильтрация словарей по значению state с обработкой возможного исключения KeyError
        filtered_data = list(filter(lambda data: data["state"] == state, source_data))
    except KeyError:
        # Обработка случая, когда в словарях отсутствует ключ 'state'
        raise KeyError("В словарях нет ключа 'state'")
    else:
        # Проверка на пустой результат фильтрации
        if len(filtered_data) == 0:
            return "Нет словарей со значением state"
        else:
            # Возврат успешного результата фильтрации
            return filtered_data


def sort_by_date(
    source_data: list[dict[str, Union[str, int]]], sort: str = "True"
) -> Union[list[dict[str, Union[str, int]]], str]:
    """Сортирует список словарей по дате.

    Args:
        source_data: Список словарей, которые нужно отсортировать. Каждый словарь должен
            содержать ключ 'date' с значением даты для сортировки.
        sort: Строковый флаг, определяющий порядок сортировки. При значении "True" (по умолчанию)
            сортировка выполняется по убыванию, иначе - по возрастанию. Регистр не учитывается.

    Returns:
        Отсортированный список словарей или строку с сообщением об ошибке, если в словарях
        отсутствует ключ 'date'.
    """
    # Определяем направление сортировки (по убыванию или возрастанию)
    if sort.lower() == "true":
        reverse = True
    else:
        reverse = False

    try:
        # Пытаемся отсортировать данные по ключу "date" с указанным направлением
        sorted_data = sorted(source_data, key=lambda data: data["date"], reverse=reverse)
    except KeyError:
        # Если ключ "date" отсутствует в словарях, возвращаем сообщение об ошибке
        raise KeyError("В словарях нет ключа 'date'")
    else:
        # Возвращаем отсортированные данные, если ошибок не возникло
        return sorted_data
