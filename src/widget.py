from masks import get_mask_account, get_mask_card_number


def mask_account_card(card_or_account_number: str) -> str:
    """Функция, которая маскирует номер карты и счёта"""
    card_or_account_number_split: list[str] = card_or_account_number.split()
    if "Счет" in card_or_account_number:
        masked_data: str = get_mask_account(int(card_or_account_number_split[-1]))
    else:
        masked_data: str = get_mask_card_number(int(card_or_account_number_split[-1]))
    return card_or_account_number_split[0] + " " + masked_data
