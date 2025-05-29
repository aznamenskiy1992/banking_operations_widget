import pytest

from src.widget import mask_account_card


@pytest.mark.parametrize("number, mask_number", [
    ("Счет 79053641285349013572", "Счет **3572"),
    ("MasterCard 5543812355785520", "MasterCard 5543 81** **** 5520"),
])
def test_definition_account_and_card_number(number, mask_number):
    assert mask_account_card(number) == mask_number


@pytest.mark.parametrize("card_number, mask_number", [
    ("Visa Classic 5543812355785", "Visa Classic 5543 81* *** 785"),  # 13 цифр
    ("Maestro 554381235578552014", "Maestro 5543 81** **** **2014"),  # 18 цифр
    ("Visa Platinum 5543812355785520439", "Visa Platinum 5543 81** **** **** 439"),  # 19 цифр
])
def test_definition_other_card_number(card_number, mask_number):
    assert mask_account_card(card_number) == mask_number


@pytest.mark.parametrize("account_number, mask_number", [
    ("Расчётный счет 79053641285349013572", "Расчётный счет **3572"),
    ("Корреспондентский счет 79053641285349013572", "Корреспондентский счет **3572"),
    ("Расчётный счёт 79053641285349013572", "Расчётный счёт **3572"),
])
def test_definition_other_account_number(account_number, mask_number):
    assert mask_account_card(account_number) == mask_number