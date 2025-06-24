import logging

import pandas as pd


def get_transactions_from_csv(path_to_csv: str) -> list:
    """Функция возвращает список транзакций из csv файла"""
    transactions_from_file: pd.DataFrame = pd.read_csv(path_to_csv, sep=";", encoding="utf-8")

    transactions_list: list = transactions_from_file.to_dict("records")

    return transactions_list