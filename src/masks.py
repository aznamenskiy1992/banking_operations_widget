def get_mask_card_number(card_number: int) -> str:
    """Функция, которая маскирует номер карты"""
    card_number_str = str(card_number)
    len_card_number = len(str(card_number))

    mask_patterns = {
        16: {
            "masking": (6, 12),
            "sep": (4, 4, 4, 4),
        },
        13: {
            "masking": (6, 10),
            "sep": (4, 3, 3, 3),
        },
        18: {
            "masking": (6, 14),
            "sep": (4, 4, 4, 6),
        },
        19: {
            "masking": (6, 16),
            "sep": (4, 4, 4, 4, 3),
        },
    }

    if len_card_number in list(mask_patterns.keys()):
        masking_position_start: int = mask_patterns[len_card_number]["masking"][0]
        masking_position_end: int = mask_patterns[len_card_number]["masking"][1]

        masking_count: int = masking_position_end - masking_position_start

        mask_card_number: str = (
            card_number_str[:masking_position_start] + "*" * masking_count + card_number_str[masking_position_end:]
        )

        dividing_start_position: int = 0
        dividing_end_position: int = mask_patterns[len_card_number]["sep"][0]
        dividing_card_number_by_blocks: list[str] = []

        for index in range(len(mask_patterns[len_card_number]["sep"])):
            if index == 0:
                dividing_card_number_by_blocks.append(mask_card_number[:dividing_end_position])
            else:
                dividing_start_position += mask_patterns[len_card_number]["sep"][index - 1]
                dividing_end_position += mask_patterns[len_card_number]["sep"][index]
                if index == len(mask_patterns[len_card_number]["sep"]) - 1:
                    dividing_card_number_by_blocks.append(mask_card_number[dividing_start_position:])
                else:
                    dividing_card_number_by_blocks.append(
                        mask_card_number[dividing_start_position:dividing_end_position]
                    )

    mask_card_number: str = " ".join(dividing_card_number_by_blocks)

    return mask_card_number


def get_mask_account(account_number: int) -> str:
    """Функция, которая маскирует номер счёта"""
    mask_account_number: str = "*" * 2 + str(account_number)[16:]
    return mask_account_number
