def get_mask_card_number(card_number: int) -> str:
    """Функция, которая маскирует номер карты"""
    if len(str(card_number)) == 16:
        dividing_card_number_by_blocks: list[str] = [
            str(card_number)[:4],
            str(card_number)[4:6] + "*" * 2,
            "*" * 4,
            str(card_number)[12:],
        ]
    elif len(str(card_number)) == 13:
        dividing_card_number_by_blocks: list[str] = [
            str(card_number)[:4],
            str(card_number)[4:6] + "*",
            "*" * 3,
            str(card_number)[-3:],
        ]
    elif len(str(card_number)) == 18:
        dividing_card_number_by_blocks: list[str] = [
            str(card_number)[:4],
            str(card_number)[4:6] + "*" * 2,
            "*" * 4,
            "*" * 2 + str(card_number)[-4:],
        ]
    mask_card_number: str = " ".join(dividing_card_number_by_blocks)
    return mask_card_number


def get_mask_account(account_number: int) -> str:
    """Функция, которая маскирует номер счёта"""
    mask_account_number: str = "*" * 2 + str(account_number)[16:]
    return mask_account_number
