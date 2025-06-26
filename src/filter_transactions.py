import re


def process_bank_search(data:list[dict], search:str) -> list[dict]:
    """Функция возвращает отфильтрованный список словарей с операциями по ключу description"""
    return [e for i, e in enumerate(data) if re.search(rf"^{search}|.{search}.|{search}$", data[i]["description"], flags=re.IGNORECASE)]
