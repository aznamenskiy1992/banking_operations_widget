import logging

import pandas as pd


def get_transactions_from_csv(path_to_csv: str) -> list:
    """Функция возвращает список транзакций из csv файла"""
    try:
        transactions_from_file: pd.DataFrame = pd.read_csv(path_to_csv, sep=";", encoding="utf-8")

    except FileNotFoundError:
        raise FileNotFoundError("Файл не найден. Проверьте путь до файла")

    else:
        if len(transactions_from_file) == 0:
            return []

        transactions_list: list = transactions_from_file.to_dict("records")
        return transactions_list


def get_transactions_from_xlsx(path_to_xlsx: str) -> list:
    """Функция возвращает список транзакций из xlsx файла"""
    transactions_from_file: pd.DataFrame = pd.read_excel(path_to_xlsx)

    transactions_list: list = transactions_from_file.to_dict("records")
    return transactions_list