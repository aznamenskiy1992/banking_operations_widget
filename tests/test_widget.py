import pytest

from src.widget import mask_account_card, get_date


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


def test_none_card_and_account_number(none_card_and_account_number):
    assert mask_account_card(None) == none_card_and_account_number


def test_card_and_account_number_incorrect_types(card_and_account_number_incorrect_types):
    assert mask_account_card([5543812355785, 79053641285349013572]) == card_and_account_number_incorrect_types
    assert mask_account_card({"Visa": 5543812355785520, "Расчётный счет": 79053641285349013572}) == card_and_account_number_incorrect_types
    assert mask_account_card((5543812355785, 79053641285349013572)) == card_and_account_number_incorrect_types
    assert mask_account_card({5543812355785, 79053641285349013572}) == card_and_account_number_incorrect_types
    assert mask_account_card(5543812355785.25) == card_and_account_number_incorrect_types
    assert mask_account_card(5543812355785) == card_and_account_number_incorrect_types
    assert mask_account_card(79053641285349013572) == card_and_account_number_incorrect_types


@pytest.mark.parametrize("date, convert_date", [
    ("2023-05-15T12:30:45", "15.05.2023"),
    ("2000-01-01T00:00:00", "01.01.2000"),
    ("0001-01-01T00:00:00", "01.01.0001"),
])
def test_convert_str_to_date_d_m_y(date, convert_date):
    assert get_date(date) == convert_date


def test_not_have_date(not_have_date):
    assert get_date("T12:30:45") == not_have_date