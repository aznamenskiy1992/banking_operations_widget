import pytest

from src.generators import filter_by_currency


def test_none_list_for_filter_by_currency(none_transactions_list_for_filter_by_currancy_and_transaction_descriptions):
    """Тестирует обработку None в качестве списка словарей."""
    assert filter_by_currency(None, "USD") == none_transactions_list_for_filter_by_currancy_and_transaction_descriptions
