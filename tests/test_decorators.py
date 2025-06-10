from fileinput import filename
import os

import pytest

from src.decorators import log, file_address


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
