import json
from json import JSONDecodeError


def get_transactions(path_to_operations_file: str) -> list[dict[str, int]]:
    """Функция возвращает список банковских операций из operations.json"""
    empty_list_to_return = []

    try:
        with open(path_to_operations_file, "r", encoding="utf-8") as f:
            operations: list[dict[str, int]] = json.load(f)

            if not isinstance(operations, list):
                print("Данные в файле находятся не в списке")
                return empty_list_to_return
            elif len(operations) == 0:
                print("Нет данных в файле")
                return empty_list_to_return

            return operations

    except FileNotFoundError:
        print("Не найден файл по указанному пути")
        return empty_list_to_return

    except json.JSONDecodeError as exc_info:
        raise json.JSONDecodeError(
            msg="Невозможно декодировать данные в JSON",
            doc=exc_info.doc,
            pos=exc_info.pos
        )
