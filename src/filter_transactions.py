import re
from collections import Counter


def process_bank_search(data:list[dict], search:str) -> list[dict]:
    """Функция возвращает отфильтрованный список словарей с операциями по ключу description"""
    if data is None:
        raise TypeError("Список операций не передан")
    elif not isinstance(data, list):
        raise TypeError("Операции должны быть переданы, как список словарей")

    if search is None:
        raise TypeError("Строка для поиска описания операций не передана")
    elif not isinstance(search, str):
        raise TypeError("Строка для поиска описания операция должна быть передана в формате str")

    if len(data) == 0:
        return []

    filtered_operations: list[dict] = []
    not_have_description_in_dic: list = []

    for i, e in enumerate(data):
        if "description" not in data[i].keys():
            not_have_description_in_dic.append(str(data[i].get("id", "неизвестный id")))
        else:
            if re.search(rf"^{search}|.{search}.|{search}$", data[i]["description"], flags=re.IGNORECASE):
                filtered_operations.append(e)

    if not_have_description_in_dic:
        print(f"ID операций без ключа description: {', '.join(not_have_description_in_dic)}", end="")

    return filtered_operations


def process_bank_operations(data:list[dict], categories:list)-> dict:
    """Функция возвращает словарь со списком категорий и количеством таких операций"""
    return dict(Counter([data[i]["description"] for i in range(len(data)) if data[i]["description"] in categories]))
