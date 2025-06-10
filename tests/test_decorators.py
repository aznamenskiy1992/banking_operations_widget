from fileinput import filename
import os

import pytest

from src.decorators import log, file_address
from tests.conftest import example_input_list_dicts_for_filter_by_state


def test_log_success_operation_in_file_for_get_mask_card_number_with_log_decorator(example_input_card_for_get_mask_curd_number):
    """Тестирует выполнение успешной операции. Логи в файл"""
    @log("mylog.txt")
    def get_mask_card_number(card_number):
        card_number_str = str(card_number)
        return card_number_str[:4] + " " + card_number_str[4:6] + "*" * 2 + " " + "*" * 4 + " " + card_number_str[12:]

    result = get_mask_card_number(example_input_card_for_get_mask_curd_number)
    with open(file_address, "r", encoding="utf-8") as file:
        content = file.readlines()
        assert content[-1].strip() == "get_mask_card_number ok"


def test_log_success_operation_in_file_for_filter_by_state_with_log_decorator(example_input_list_dicts_for_filter_by_state):
    """Тестирует выполнение успешной операции. Логи в файл"""
    @log("mylog.txt")
    def filter_by_state(source_data, state = "EXECUTED"):
        filtered_data = list(filter(lambda data: data["state"] == state, source_data))
        return filtered_data

    result = filter_by_state(example_input_list_dicts_for_filter_by_state)
    with open(file_address, "r", encoding="utf-8") as file:
        content = file.readlines()
        assert content[-1].strip() == "filter_by_state ok"


def test_log_error_operation_in_file_for_get_mask_card_number_with_log_decorator(example_input_none_for_get_mask_card_number):
    """Тестирует логирование ошибок при выполнении операции. Логи в файл"""
    @log("mylog.txt")
    def get_mask_card_number(card_number):
        if card_number is None:
            raise ValueError("Не указан номер карты или счёта")
        card_number_str = str(card_number)
        return card_number_str[:4] + " " + card_number_str[4:6] + "*" * 2 + " " + "*" * 4 + " " + card_number_str[12:]

    result = get_mask_card_number(example_input_none_for_get_mask_card_number)
    with open(file_address, "r", encoding="utf-8") as file:
        content = file.readlines()
        assert content[-1].strip() == f"get_mask_card_number error: Не указан номер карты или счёта. Inputs: {example_input_none_for_get_mask_card_number}"


def test_log_error_operation_in_file_for_filter_by_state_with_log_decorator(example_input_none_for_filter_by_state):
    """Тестирует логирование ошибок при выполнении операции. Логи в файл"""
    @log("mylog.txt")
    def filter_by_state(source_data, state = "EXECUTED"):
        try:
            filtered_data = list(filter(lambda data: data["state"] == state, source_data))
        except KeyError:
            raise KeyError("В словарях нет ключа 'state'")
        return filtered_data

    result = filter_by_state(example_input_none_for_filter_by_state)
    with open(file_address, "r", encoding="utf-8") as file:
        content = file.readlines()
        assert content[-1].strip() == f"filter_by_state error: \"В словарях нет ключа 'state'\". Inputs: {example_input_none_for_filter_by_state}"
