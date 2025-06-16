import json


def get_transactions(path_to_operations_file: str) -> list[dict[str, int]]:
    """Функция возвращает список банковских операций из operations.json"""
    with open(path_to_operations_file, "r", encoding="utf-8") as f:
        operations: list[dict[str, int]] = json.load(f)

    return operations
