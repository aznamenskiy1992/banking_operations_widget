import pytest

from src.generators import filter_by_currency


def test_none_list_for_filter_by_currency(none_transactions_list_for_filter_by_currancy_and_transaction_descriptions):
    """Тестирует обработку None в качестве списка словарей."""
    assert filter_by_currency(None, "USD") == none_transactions_list_for_filter_by_currancy_and_transaction_descriptions


def test_empty_transactions_list_for_filter_by_currancy_and_transaction_descriptions(empty_transactions_list_for_filter_by_currancy_and_transaction_descriptions):
    """Тестирует обработку кейса, когда на вход подаётся пустой список словарей с транзакциями"""
    assert filter_by_currency([], "USD") == empty_transactions_list_for_filter_by_currancy_and_transaction_descriptions


def test_in_transactions_list_not_dict_for_filter_by_currancy_and_transaction_descriptions(in_transactions_list_not_dict_for_filter_by_currancy_and_transaction_descriptions):
    """Тестирует обработку кейса, когда на вход подаётся список с транзакциями не в словарях"""
    assert filter_by_currency([{(939719570, 9824.07), (142264268, "EXECUTED")}], "USD") == in_transactions_list_not_dict_for_filter_by_currancy_and_transaction_descriptions
