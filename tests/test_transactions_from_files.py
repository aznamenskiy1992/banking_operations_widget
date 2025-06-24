import pytest
from unittest.mock import patch
import logging

import pandas as pd

from src.transactions_from_files import get_transactions_from_csv


def test_get_transactions_from_csv_for_get_transactions_from_csv(transactions_from_files):
    """Тестирует возврат списка транзакций из csv файла"""
    mock_data = pd.DataFrame(transactions_from_files)

    with patch("pandas.read_csv", return_value=mock_data) as mock_read_csv:
        result = get_transactions_from_csv("transactions.csv")

        assert result == transactions_from_files

        mock_read_csv.assert_called_once_with("transactions.csv")
