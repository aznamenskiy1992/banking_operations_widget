def get_mask_card_number(card_number: int) -> str:
    """Функция, которая маскирует номер карты"""
    dividing_card_number_by_blocks: list[str] = [
        str(card_number)[:4],
        str(card_number)[4:6] + "*" * 2,
        "*" * 4,
        str(card_number)[12:],
    ]
    mask_card_number: str = " ".join(dividing_card_number_by_blocks)
    return mask_card_number


def get_mask_account(account_number: int) -> str:
    """Функция, которая маскирует номер счёта"""
    mask_account_number: str = "*" * 2 + str(account_number)[16:]
    return mask_account_number
