import json
import logging

from src.external_api import convert_currency


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('logs/logs.log', mode="w", encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_transactions(path_to_operations_file: str) -> list[dict[str, int]]:
    """
    Читает и возвращает список банковских операций из JSON-файла.

    Параметры:
        path_to_operations_file (str): Путь к JSON-файлу с операциями

    Возвращает:
        list[dict[str, int]]: Список словарей с операциями. В случае ошибок возвращает пустой список.

    Исключения:
        FileNotFoundError: Если файл не найден по указанному пути (возвращает пустой список)
        json.JSONDecodeError: При ошибке декодирования JSON (пробрасывает исключение дальше)

    Особенности:
        - Проверяет, что данные в файле являются списком
        - Проверяет, что список не пустой
        - В случае ошибок файла выводит сообщение в консоль
        - При некорректных данных возвращает пустой список
        - При ошибках JSON пробрасывает исключение

    Пример использования:
        >>> transactions = get_transactions("data/operations.json")
        >>> print(len(transactions))
        100
    """
    empty_list_to_return = []  # Пустой список для возврата в случае ошибок

    try:
        # Открываем файл для чтения с кодировкой UTF-8
        logger.info("Попытка открытия JSON файла с банковскими операциями")
        with open(path_to_operations_file, "r", encoding="utf-8") as f:
            # Пытаемся загрузить данные из JSON
            logger.info("Попытка получить данные из JSON файла с банковскими операциями")
            operations: list[dict[str, int]] = json.load(f)

            # Проверяем, что данные являются списком
            if not isinstance(operations, list):
                print("Данные в файле находятся не в списке")
                return empty_list_to_return
            # Проверяем, что список не пустой
            elif len(operations) == 0:
                print("Нет данных в файле")
                return empty_list_to_return

            # Возвращаем успешно загруженные операции
            logger.info("Возврат загруженных банковских операций")
            return operations

    except FileNotFoundError:
        # Обработка случая, когда файл не найден
        logger.error("JSON файл с банковскими операциями не найден")
        print("Не найден файл по указанному пути")
        logger.info("Возврат пустого списка")
        return empty_list_to_return

    except json.JSONDecodeError as exc_info:
        # Пробрасываем JSONDecodeError с более понятным сообщением
        raise json.JSONDecodeError(msg="Невозможно декодировать данные в JSON", doc=exc_info.doc, pos=exc_info.pos)


def get_amount(transaction: dict[str, int]) -> float:
    """
    Извлекает сумму транзакции из словаря операции, при необходимости конвертируя в рубли.

    Параметры:
        transaction (dict[str, int]): Словарь с данными о транзакции, должен содержать:
            - operationAmount (dict): Словарь с суммой и валютой операции
                - amount (str|int|float): Сумма операции
                - currency (dict): Словарь с данными о валюте
                    - code (str): Код валюты (например, "RUB", "USD")

    Возвращает:
        float: Сумма операции в рублях. Если валюта не RUB, выполняет конвертацию.

    Исключения:
        TypeError: Если транзакция передана не в виде словаря
        KeyError: Если отсутствуют необходимые ключи в словаре транзакции
        ValueError: Если сумма операции указана в нечисловом формате

    Особенности:
        - Для конвертации валют использует функцию convert_currency()
        - Возвращает сумму как float вне зависимости от исходного формата

    Примеры:
        >>> transaction = {
        ...     "operationAmount": {
        ...         "amount": "100.50",
        ...         "currency": {"code": "RUB"}
        ...     }
        ... }
        >>> get_amount(transaction)
        100.5

        >>> transaction = {
        ...     "operationAmount": {
        ...         "amount": "100",
        ...         "currency": {"code": "USD"}
        ...     }
        ... }
        >>> get_amount(transaction)  # Конвертирует USD в RUB по текущему курсу
        7500.0
    """
    # Проверка типа входных данных
    if not isinstance(transaction, dict):
        raise TypeError("Транзакция должна быть передана в словаре")

    # Проверка наличия основного ключа с суммой и валютой
    if "operationAmount" not in transaction:
        raise KeyError("Нет ключа operationAmount")

    # Проверка наличия обязательных ключей в operationAmount
    amount_currency_key = ["amount", "currency"]
    for key_ in amount_currency_key:
        if key_ not in transaction["operationAmount"]:
            raise KeyError(f"Нет ключа {key_}")

    # Проверка наличия кода валюты
    if "code" not in transaction["operationAmount"]["currency"]:
        raise KeyError("Нет ключа code")

    else:
        try:
            # Извлекаем код валюты и сумму операции
            currency: str = transaction["operationAmount"]["currency"]["code"]
            amount = float(transaction["operationAmount"]["amount"])  # Преобразуем в float
        except ValueError:
            raise ValueError("Сумма транзакции указана в нечисловом формате")
        else:
            # Если валюта не рубли - конвертируем
            if currency != "RUB":
                return convert_currency(currency, amount)
            else:
                return amount  # Для рублей возвращаем как есть
