import pytest

from src.widget import mask_account_card


@pytest.mark.parametrize("number, mask_number", [
    ("Счет 79053641285349013572", "Счет **3572"),
    ("MasterCard 5543812355785520", "MasterCard 5543 81** **** 5520"),
])
def test_definition_account_and_card_number(number, mask_number):
    assert mask_account_card(number) == mask_number