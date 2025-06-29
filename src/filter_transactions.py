import re
from collections import Counter


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Фильтрует банковские операции по совпадению строки поиска в описании операции.

    Принимает:
        data (list[dict]): Список словарей с банковскими операциями. Каждая операция должна содержать
                          поле 'description' (описание операции) и 'id' (идентификатор операции).
        search (str): Строка для поиска в описаниях операций. Поиск выполняется по подстроке без учета регистра.

    Возвращает:
        list[dict]: Отфильтрованный список операций, где в описании найдено совпадение с search.
                   Возвращает пустой список, если совпадений нет или входной список data пуст.

    Исключения:
        TypeError: Если входные параметры не соответствуют ожидаемым типам или не переданы.
    """
    # Проверка корректности входных данных - data
    if data is None:
        raise TypeError("Список операций не передан")
    elif not isinstance(data, list):
        raise TypeError("Операции должны быть переданы, как список словарей")

    # Проверка корректности входных данных - search
    if search is None:
        raise TypeError("Строка для поиска описания операций не передана")
    elif not isinstance(search, str):
        raise TypeError("Строка для поиска описания операция должна быть передана в формате str")

    # Если передан пустой список операций, возвращаем пустой список
    if len(data) == 0:
        return []

    # Инициализация списков для сбора результатов
    filtered_operations: list[dict] = []  # Список для хранения отфильтрованных операций
    not_have_description_in_dic: list = []  # Список для хранения ID операций без поля description

    # Проход по всем операциям в списке data
    for i, e in enumerate(data):
        # Проверка наличия ключа 'description' в текущей операции
        if "description" not in data[i].keys():
            # Если ключа нет, добавляем ID операции в список проблемных операций
            not_have_description_in_dic.append(str(data[i].get("id", "неизвестный id")))
        else:
            # Поиск подстроки search в описании операции (без учета регистра)
            # Регулярное выражение ищет совпадения:
            # - В начале строки (^search)
            # - В середине строки (.search.)
            # - В конце строки (search$)
            if re.search(rf"^{search}|.{search}.|{search}$", data[i]["description"], flags=re.IGNORECASE):
                # Если совпадение найдено, добавляем операцию в результат
                filtered_operations.append(e)

    # Вывод предупреждения об операциях без поля description (если такие есть)
    if not_have_description_in_dic:
        print(f"ID операций без ключа description: {', '.join(not_have_description_in_dic)}", end="")

    # Возвращаем отфильтрованный список операций
    return filtered_operations


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """
    Обрабатывает банковские операции, подсчитывая количество операций по заданным категориям.

    Принимает:
        data (list[dict]): Список словарей с банковскими операциями. Каждая операция должна содержать
                          как минимум поля 'description' (описание операции) и 'id' (идентификатор операции).
        categories (list): Список категорий для фильтрации операций.

    Возвращает:
        dict: Словарь, где ключи - это категории из входного списка categories,
              а значения - количество операций в каждой категории.

    Исключения:
        TypeError: Если входные параметры не соответствуют ожидаемым типам или не переданы.
    """
    # Проверка корректности входных данных - data
    if data is None:
        raise TypeError("Список операций не передан")
    elif not isinstance(data, list):
        raise TypeError("Операции должны быть переданы, как список словарей")

    # Проверка корректности входных данных - categories
    if categories is None:
        raise TypeError("Категории не переданы")
    elif not isinstance(categories, list):
        raise TypeError("Категории должны быть переданы в списке")

    # Если передан пустой список операций, возвращаем пустой словарь
    if len(data) == 0:
        return {}

    # Инициализация списков для сбора результатов
    cnt_operations: list = []  # Список для хранения найденных категорий операций
    not_have_description_in_dic: list = []  # Список для хранения ID операций без поля description

    # Проход по всем операциям в списке data
    for i in range(len(data)):
        # Проверка наличия ключа 'description' в текущей операции
        if "description" not in data[i].keys():
            # Если ключа нет, добавляем ID операции в список проблемных операций
            not_have_description_in_dic.append(str(data[i].get("id", "неизвестный id")))
        else:
            # Если ключ есть и описание операции входит в искомые категории, добавляем в список
            if data[i]["description"] in categories:
                cnt_operations.append(data[i]["description"])

    # Вывод предупреждения об операциях без поля description (если такие есть)
    if not_have_description_in_dic:
        print(f"ID операций без ключа description: {', '.join(not_have_description_in_dic)}", end="")

    # Подсчет количества операций по категориям и возврат результата в виде словаря
    return dict(Counter(cnt_operations))
