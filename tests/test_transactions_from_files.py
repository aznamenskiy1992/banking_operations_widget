import pytest
from unittest.mock import patch
import logging

import pandas as pd

from src.transactions_from_files import get_transactions_from_csv, get_transactions_from_xlsx


def test_get_transactions_from_csv_for_get_transactions_from_csv(transactions_from_files):
    """Тестирует возврат списка транзакций из csv файла"""
    mock_data = pd.DataFrame(transactions_from_files)

    with patch("pandas.read_csv", return_value=mock_data) as mock_read_csv:
        result = get_transactions_from_csv("transactions.csv")

        assert result == transactions_from_files

        mock_read_csv.assert_called_once_with("transactions.csv", sep=";", encoding="utf-8")


def test_file_not_found_for_get_transactions_from_csv():
    """Обрабатывает кейс, когда csv файл не найден"""
    with pytest.raises(FileNotFoundError) as exc_info:
        get_transactions_from_csv("test.csv")
    assert str(exc_info.value) == "Файл не найден. Проверьте путь до файла"


@patch("src.transactions_from_files.pd.read_csv")
def test_empty_csv_file_for_get_transactions_from_csv(mock_read_csv):
    """Обрабатывает кейс, когда csv файл пустой"""
    mock_read_csv.return_value = []

    result = get_transactions_from_csv("transactions.csv")

    assert result == []

    mock_read_csv.assert_called_once_with("transactions.csv", sep=";", encoding="utf-8")


def test_get_transactions_from_xlsx_for_get_transactions_from_xlsx(transactions_from_files):
    """Тестирует возврат списка транзакций из csv файла"""
    mock_data = pd.DataFrame(transactions_from_files)

    with patch("src.transactions_from_files.pd.read_excel", return_value=mock_data) as mock_read_xlsx:
        result = get_transactions_from_xlsx("transactions_excel.xlsx")

        assert result == transactions_from_files

        mock_read_xlsx.assert_called_once_with("transactions_excel.xlsx")
