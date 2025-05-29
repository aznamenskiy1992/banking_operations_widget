def get_mask_card_number(card_number: int) -> str:
    """Функция, которая маскирует номер карты"""

    # Входные данные пустые
    if card_number is None:
        return "Не указан номер карты или счёта"

    if isinstance(card_number, int):  # Входные данные в типе int
        card_number_str = str(card_number)
    elif isinstance(card_number, str):  # Входные данные в типе str
        if not card_number.isdigit():
            return "Номер карты или счёта должен состоять только из цифр"  # Строка содержит не только цифры
        else:
            card_number_str = card_number
    else:
        return "Номер карты или счёта должен быть целым числом"  # Входные данные не str или int

    len_card_number = len(card_number_str)

    # Словарь с данными для маскирования
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
        # Позиции для среза строки
        masking_position_start: int = mask_patterns[len_card_number]["masking"][0]
        masking_position_end: int = mask_patterns[len_card_number]["masking"][1]

        # Кол-во используемых звёздочек для маскирования
        masking_count: int = masking_position_end - masking_position_start

        # Маскируем строку
        mask_card_number: str = (
            card_number_str[:masking_position_start] + "*" * masking_count + card_number_str[masking_position_end:]
        )

        # Позиции для разделения строки
        dividing_start_position: int = 0
        dividing_end_position: int = mask_patterns[len_card_number]["sep"][0]

        dividing_card_number_by_blocks: list[str] = []

        for index in range(len(mask_patterns[len_card_number]["sep"])):
            if index == 0:
                dividing_card_number_by_blocks.append(mask_card_number[:dividing_end_position])  # Первая часть строки
            else:
                dividing_start_position += mask_patterns[len_card_number]["sep"][index - 1]
                dividing_end_position += mask_patterns[len_card_number]["sep"][index]
                if index == len(mask_patterns[len_card_number]["sep"]) - 1:
                    dividing_card_number_by_blocks.append(
                        mask_card_number[dividing_start_position:]
                    )  # Окончание строки
                else:
                    dividing_card_number_by_blocks.append(
                        mask_card_number[dividing_start_position:dividing_end_position]
                    )
    else:
        return "Указан некорректный номер карты или счёта. Проверьте количество цифр"  # Входные данные с некоректным кол-вом цифр

    return " ".join(dividing_card_number_by_blocks)


def get_mask_account(account_number: int) -> str:
    """Функция, которая маскирует номер счёта"""
    if account_number is None:
        return "Не указан номер карты или счёта"

    if isinstance(account_number, int):
        account_number_str = str(account_number)
    elif isinstance(account_number, str):
        if not account_number.isdigit():
            return "Номер карты или счёта должен состоять только из цифр"
        else:
            account_number_str = account_number
    else:
        return "Номер карты или счёта должен быть целым числом"

    len_account_number = len(account_number_str)

    if len_account_number == 20:
        mask_account_number: str = "*" * 2 + str(account_number)[16:]
    else:
        return "Указан некорректный номер карты или счёта. Проверьте количество цифр"

    return mask_account_number
