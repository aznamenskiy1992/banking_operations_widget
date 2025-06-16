import json


def get_transactions(path_to_operations_file: str) -> list[dict[str, int]]:
    """Функция возвращает список банковских операций из operations.json"""
    try:
        with open(path_to_operations_file, "r", encoding="utf-8") as f:
            operations: list[dict[str, int]] = json.load(f)
    except FileNotFoundError:
        print("Не найден файл по указанному пути")
        return []

    return operations
