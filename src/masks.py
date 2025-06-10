def get_mask_card_number(card_number: int) -> str:
    """Функция для маскирования номера карты или счёта.

    Принимает номер карты (целое число или строку из цифр) и возвращает его замаскированную версию
    в формате, разделённом пробелами (например, "1234 56** **** 5678").

    Args:
        card_number: Номер карты или счёта (int или str, содержащий только цифры).

    Returns:
        str: Замаскированный номер карты в отформатированном виде или сообщение об ошибке.
    """

    # Обработка случая, когда входные данные не переданы (None)
    if card_number is None:
        raise ValueError("Не указан номер карты или счёта")

    # Преобразование номера карты в строку и проверка типа входных данных
    if isinstance(card_number, int):  # Если номер карты передан как целое число
        card_number_str = str(card_number)
    elif isinstance(card_number, str):  # Если номер карты передан как строка
        if not card_number.isdigit():
            raise ValueError("Номер карты или счёта должен состоять только из цифр")  # Строка содержит нецифровые символы
        else:
            card_number_str = card_number
    else:
        return "Номер карты или счёта должен быть целым числом"  # Недопустимый тип данных (не int и не str)

    len_card_number = len(card_number_str)

    # Словарь с шаблонами маскирования для разных длин номеров карт
    # Ключи — допустимые длины номеров, значения — параметры маскирования и разделения:
    #   - "masking": (start, end) — диапазон символов для замены на звёздочки
    #   - "sep": (n1, n2, ...) — длины блоков, на которые нужно разделить номер
    mask_patterns = {
        16: {  # Стандартные 16-значные карты (Visa, Mastercard)
            "masking": (6, 12),  # Маскируем символы с 6 по 11 (6 символов)
            "sep": (4, 4, 4, 4),  # Разбиваем на 4 блока по 4 цифры
        },
        13: {  # Редкие 13-значные карты (старые Visa)
            "masking": (6, 10),  # Маскируем символы с 6 по 9 (4 символа)
            "sep": (4, 3, 3, 3),  # Разбиваем на блоки: 4, 3, 3, 3
        },
        18: {  # Некоторые виды карт/счетов (например, Maestro)
            "masking": (6, 14),  # Маскируем символы с 6 по 13 (8 символов)
            "sep": (4, 4, 4, 6),  # Разбиваем на блоки: 4, 4, 4, 6
        },
        19: {  # Длинные номера (некоторые типы счетов)
            "masking": (6, 16),  # Маскируем символы с 6 по 15 (10 символов)
            "sep": (4, 4, 4, 4, 3),  # Разбиваем на блоки: 4, 4, 4, 4, 3
        },
    }

    # Проверяем, поддерживается ли длина номера карты
    if len_card_number in list(mask_patterns.keys()):
        # Получаем позиции для маскирования из шаблона
        masking_position_start: int = mask_patterns[len_card_number]["masking"][0]
        masking_position_end: int = mask_patterns[len_card_number]["masking"][1]

        # Вычисляем количество символов для маскирования
        masking_count: int = masking_position_end - masking_position_start

        # Создаём замаскированную строку: начало + звёздочки + конец
        mask_card_number: str = (
            card_number_str[:masking_position_start] + "*" * masking_count + card_number_str[masking_position_end:]
        )

        # Разделяем замаскированный номер на блоки согласно шаблону
        dividing_start_position: int = 0
        dividing_end_position: int = mask_patterns[len_card_number]["sep"][0]

        dividing_card_number_by_blocks: list[str] = []

        # Разбиваем номер на части по заданным в шаблоне длинам блоков
        for index in range(len(mask_patterns[len_card_number]["sep"])):
            if index == 0:
                # Первый блок (от 0 до dividing_end_position)
                dividing_card_number_by_blocks.append(mask_card_number[:dividing_end_position])
            else:
                # Сдвигаем позиции начала и конца для текущего блока
                dividing_start_position += mask_patterns[len_card_number]["sep"][index - 1]
                dividing_end_position += mask_patterns[len_card_number]["sep"][index]

                if index == len(mask_patterns[len_card_number]["sep"]) - 1:
                    # Последний блок (до конца строки)
                    dividing_card_number_by_blocks.append(mask_card_number[dividing_start_position:])
                else:
                    # Промежуточные блоки
                    dividing_card_number_by_blocks.append(
                        mask_card_number[dividing_start_position:dividing_end_position]
                    )
    else:
        # Длина номера карты не поддерживается
        raise ValueError("Указан некорректный номер карты или счёта. Проверьте количество цифр")

    # Собираем блоки в одну строку с разделением пробелами
    return " ".join(dividing_card_number_by_blocks)


def get_mask_account(account_number: int) -> str:
    """Функция для маскировки номера счёта.

    Возвращает строку, в которой первые 16 цифр заменены на '*', а оставлены только последние 4 цифры.
    Номер счёта должен состоять из 20 цифр и может быть передан как целое число, либо как строка из цифр.

    Args:
        account_number (int): Номер счёта для маскировки. Может быть целым числом или строкой.

    Returns:
        str: Замаскированный номер счёта в формате **XXXX, где XXXX - последние 4 цифры номера.
             В случае ошибки возвращает соответствующее сообщение.
    """
    # Проверка на None
    if account_number is None:
        return "Не указан номер карты или счёта"

    # Преобразование номера счёта в строку с проверкой типа
    if isinstance(account_number, int):
        account_number_str = str(account_number)
    elif isinstance(account_number, str):
        if not account_number.isdigit():
            return "Номер карты или счёта должен состоять только из цифр"
        else:
            account_number_str = account_number
    else:
        return "Номер карты или счёта должен быть целым числом"

    # Проверка длины номера счёта
    len_account_number = len(account_number_str)

    # Маскировка номера счёта (оставляем только последние 4 цифры)
    if len_account_number == 20:
        mask_account_number: str = "*" * 2 + str(account_number)[-4:]
    else:
        return "Указан некорректный номер карты или счёта. Проверьте количество цифр"

    return mask_account_number
