from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_or_account_number: str) -> str:
    """Функция, которая маскирует номер карты и счёта"""
    if card_or_account_number is None:
        return "Не указан номер карты или счёта"

    if not isinstance(card_or_account_number, str):
        return """Номер карты или счёта должен быть строкой.
    Маска ввода:
    Для счёта - 'Счёт 79053641285349013572'
    Для Карты - 'Visa Classic 5543812355785'"""

    card_or_account_number_split: list[str] = card_or_account_number.split()

    if "счет" in card_or_account_number.lower() or "счёт" in card_or_account_number.lower():
        masked_data: str = get_mask_account(int(card_or_account_number_split[-1]))
    else:
        masked_data: str = get_mask_card_number(int(card_or_account_number_split[-1]))

    if len(card_or_account_number_split) == 2:
        return card_or_account_number_split[0] + " " + masked_data
    else:
        return " ".join(card_or_account_number_split[:-1]) + " " + masked_data


def get_date(date_: str) -> str:
    """Функция, которая преобразовывает дату из строки в формат DD.MM.YYYY"""
    date_split: list[str] = date_.split("T")
    formatted_date_by_y_m_d: str = str(datetime.strptime(date_split[0], "%Y-%m-%d").date())
    formatted_date_by_y_m_d_split: list[str] = formatted_date_by_y_m_d.split("-")
    formatted_date_by_d_m_y: str = ".".join(
        [formatted_date_by_y_m_d_split[-1], formatted_date_by_y_m_d_split[1], formatted_date_by_y_m_d_split[0]]
    )
    return formatted_date_by_d_m_y