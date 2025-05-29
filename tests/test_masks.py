import pytest

from src.masks import get_mask_card_number, get_mask_account


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


def test_card_number_other_incorrect_types(card_and_account_number_other_incorrect_types):
    assert get_mask_card_number([5543812355785520, 5543812355785]) == card_and_account_number_other_incorrect_types
    assert get_mask_card_number({"Visa": 5543812355785520}) == card_and_account_number_other_incorrect_types
    assert get_mask_card_number((5543812355785520, 5543812355785)) == card_and_account_number_other_incorrect_types
    assert get_mask_card_number({5543812355785520}) == card_and_account_number_other_incorrect_types
    assert get_mask_card_number(5543812355785520.25) == card_and_account_number_other_incorrect_types


@pytest.mark.parametrize("account_number, mask_number", [
    (79053641285349013572, "**3572"),
    (77762358105236921456, "**1456"),
])
def test_input_account_number(account_number, mask_number):
    assert get_mask_account(account_number) == mask_number


def test_none_standard_account_number(none_standard_card_and_account_number):
    assert get_mask_account(7) == none_standard_card_and_account_number
    assert get_mask_account(745205381921035742369) == none_standard_card_and_account_number