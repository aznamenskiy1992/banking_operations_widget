import pandas as pd


def get_transactions_from_csv(path_to_csv: str) -> list:
    """
    Читает транзакции из CSV-файла и возвращает их в виде списка словарей.

    Параметры:
        path_to_csv (str): Путь к CSV-файлу с транзакциями.
                           Файл должен быть разделен точкой с запятой (;)
                           и использовать кодировку UTF-8.

    Возвращает:
        list: Список словарей, где каждый словарь представляет одну транзакцию.
              Если файл пустой, возвращает пустой список.

    Исключения:
        FileNotFoundError: Если файл по указанному пути не найден.

    Особенности:
        - Использует pandas.read_csv() для чтения файла
        - Автоматически преобразует DataFrame в список словарей
        - Обрабатывает случай пустого файла
        - Разделитель полей - точка с запятой (;)
        - Кодировка файла - UTF-8
    """
    try:
        # Чтение CSV-файла с указанными параметрами:
        # sep=";" - разделитель точка с запятой
        # encoding="utf-8" - кодировка UTF-8
        transactions_from_file: pd.DataFrame = pd.read_csv(path_to_csv, sep=";", encoding="utf-8")

    except FileNotFoundError:
        # Обработка случая, когда файл не найден
        raise FileNotFoundError("Файл не найден. Проверьте путь до файла")

    else:
        # Проверка на пустой DataFrame
        if len(transactions_from_file) == 0:
            return []  # Возвращаем пустой список, если файл пустой

        # Преобразование DataFrame в список словарей
        # Каждая строка DataFrame становится отдельным словарем
        transactions_list: list = transactions_from_file.to_dict("records")
        return transactions_list


def get_transactions_from_xlsx(path_to_xlsx: str) -> list:
    """
    Читает транзакции из Excel-файла (XLSX) и возвращает их в виде списка словарей.

    Параметры:
        path_to_xlsx (str): Путь к Excel-файлу формата XLSX с транзакциями.
                           Файл должен быть в формате Excel (.xlsx).

    Возвращает:
        list: Список словарей, где каждый словарь представляет одну транзакцию.
              Ключи словаря соответствуют названиям столбцов в файле.
              Если файл пустой, возвращает пустой список.

    Исключения:
        FileNotFoundError: Если файл по указанному пути не найден.
        ValueError: Если файл не является корректным Excel-файлом (обрабатывается pandas внутренне).

    Особенности:
        - Использует pandas.read_excel() для чтения файла
        - Автоматически преобразует DataFrame в список словарей
        - Обрабатывает случай пустого файла
        - Поддерживает только формат XLSX (не XLS)
        - Читает первый лист Excel-файла по умолчанию
    """
    try:
        # Чтение Excel-файла с помощью pandas
        # По умолчанию читает первый лист файла
        transactions_from_file: pd.DataFrame = pd.read_excel(path_to_xlsx)

    except FileNotFoundError:
        # Обработка случая, когда файл не найден
        raise FileNotFoundError("Файл не найден. Проверьте путь до файла")

    except Exception as e:
        # Общая обработка других ошибок чтения Excel
        raise ValueError(f"Ошибка при чтении Excel-файла: {str(e)}")

    else:
        # Проверка на пустой DataFrame
        if len(transactions_from_file) == 0:
            return []  # Возвращаем пустой список, если файл пустой

        # Преобразование DataFrame в список словарей
        # Каждая строка таблицы становится отдельным словарем
        # с ключами, соответствующими названиям столбцов
        transactions_list: list = transactions_from_file.to_dict("records")
        return transactions_list
