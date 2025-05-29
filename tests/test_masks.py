import pytest

from src.masks import get_mask_card_number


@pytest.mark.parametrize("card_number, mask_number", [
    (5543812355785520, "5543 81** **** 5520"), # 16 цифр
    (5543812355785, "5543 81* *** 785"), # 13 цифр
    (554381235578552014, "5543 81** **** **2014"), # 18 цифр
    (5543812355785520439, "5543 81** **** **** 439"), # 19 цифр
])
def test_input_standard_card_number(card_number, mask_number):
    assert get_mask_card_number(card_number) == mask_number


def test_none_card_number(none_card_and_account_number):
    assert get_mask_card_number(None) == none_card_and_account_number


def test_none_standard_card_number(none_standard_card_and_account_number):
    assert get_mask_card_number(123) == none_standard_card_and_account_number
    assert get_mask_card_number(15234820356820125369) == none_standard_card_and_account_number


@pytest.mark.parametrize("card_number, mask_number", [
    ("5543812355785520", "5543 81** **** 5520"), # 16 цифр
    ("5543812355785", "5543 81* *** 785"), # 13 цифр
    ("554381235578552014", "5543 81** **** **2014"), # 18 цифр
    ("5543812355785520439", "5543 81** **** **** 439"), # 19 цифр
])
def test_card_number_str_all_symbols_int(card_number, mask_number):
    assert get_mask_card_number(card_number) == mask_number


def test_card_number_str_symbols_not_int(card_and_account_number_str_symbols_not_int):
    assert get_mask_card_number("5543-8123-5585-520") == card_and_account_number_str_symbols_not_int
    assert get_mask_card_number("5543 812 355 785") == card_and_account_number_str_symbols_not_int