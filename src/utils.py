import json
from json import JSONDecodeError

from src.external_api import convert_currency


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


def get_amount(transaction: dict[str, int]) -> float:
    """Функция возвращает сумму транзакции из операции"""
    if not isinstance(transaction, dict):
        raise TypeError("Транзакция должна быть передана в словаре")

    if "operationAmount" not in transaction:
        raise KeyError("Нет ключа operationAmount")
    elif "amount" not in transaction["operationAmount"]:
        raise KeyError("Нет ключа amount")

    else:
        try:
            currency: str = transaction["operationAmount"]["currency"]["code"]
            amount = float(transaction["operationAmount"]["amount"])
        except ValueError:
            raise ValueError("Сумма транзакции указана в нечисловом формате")
        else:
            if currency != "RUB":
                return convert_currency(currency, amount)
            else:
                return amount

