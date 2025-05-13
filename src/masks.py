def get_mask_card_number(card_number: int) -> str:
    """Функция, которая маскирует номер карты"""
    dividing_card_number_by_blocks: list[str] = [
        str(card_number)[:5],
        str(card_number)[4:6] + "*" * 2,
        "*" * 4,
        str(card_number)[12:],
    ]
    mask_card_number: str = " ".join(dividing_card_number_by_blocks)
    return mask_card_number