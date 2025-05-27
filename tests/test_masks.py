import pytest

from src.masks import get_mask_card_number


@pytest.mark.parametrize("card_number, mask_number", [
    (5543812355785520, "5543 81** **** 5520")
])
def input_standard_card_number(card_number, mask_number): # 16 цифр
    assert get_mask_card_number(card_number) == mask_number