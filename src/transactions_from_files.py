import logging

import pandas as pd


def get_transactions_from_csv(path_to_csv: str) -> list:
    """Функция возвращает список транзакций из csv файла"""
    try:
        transactions_from_file: pd.DataFrame = pd.read_csv(path_to_csv, sep=";", encoding="utf-8")

    except FileNotFoundError:
        raise FileNotFoundError("Файл не найден. Проверьте путь до файла")

    else:
        transactions_list: list = transactions_from_file.to_dict("records")
        return transactions_list