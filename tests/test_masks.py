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