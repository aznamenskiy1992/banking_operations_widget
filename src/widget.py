from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_or_account_number: str) -> str:
    """Маскирует номер банковской карты или счета в переданной строке.

    Функция определяет тип номера (карта или счет) по ключевым словам и применяет
    соответствующую маскировку, сохраняя исходный формат строки.

    Args:
        card_or_account_number (str): Строка с номером карты или счета.
            Должна быть в одном из форматов:
            - Для счета: 'Счёт 79053641285349013572' или 'счет 79053641285349013572'
            - Для карты: 'Visa Classic 5543812355785' или 'Maestro 1596837868705199'

    Returns:
        str: Замаскированная строка в исходном формате или сообщение об ошибке.
    """

    # Проверка на None (отсутствие номера)
    if card_or_account_number is None:
        return "Не указан номер карты или счёта"

    # Проверка типа входных данных (должна быть строка)
    if not isinstance(card_or_account_number, str):
        return """Номер карты или счёта должен быть строкой.
    Маска ввода:
    Для счёта - 'Счёт 79053641285349013572'
    Для Карты - 'Visa Classic 5543812355785'"""

    # Разделение входной строки на части по пробелам
    card_or_account_number_split: list[str] = card_or_account_number.split()

    # Определение типа номера (счет или карта) и вызов соответствующей функции маскировки
    if "счет" in card_or_account_number.lower() or "счёт" in card_or_account_number.lower():
        # Если это счет, вызываем функцию маскировки счета
        masked_data: str = get_mask_account(int(card_or_account_number_split[-1]))
    else:
        # Если это карта, вызываем функцию маскировки номера карты
        masked_data: str = get_mask_card_number(int(card_or_account_number_split[-1]))

    # Формирование результата в зависимости от структуры входной строки
    if len(card_or_account_number_split) == 2:
        # Тип в одно слово: "Счёт 79053641285349013572"" → "Счёт **3572"
        return card_or_account_number_split[0] + " " + masked_data
    else:
        # Тип в несколько слов: "Расчётный счёт 79053641285349013572" → "Расчётный счёт **3572"
        return " ".join(card_or_account_number_split[:-1]) + " " + masked_data


def get_date(date_: str) -> str:
    """Преобразует дату из строкового формата YYYY-MM-DDTHH:MM:SS в формат DD.MM.YYYY.

    Функция принимает строку с датой, обрабатывает её и возвращает в новом формате.
    Также обрабатывает случаи, когда дата не указана или указана в неверном формате.

    Args:
        date_ (str): Строка с датой в формате YYYY-MM-DD. Может содержать пробелы
                     или быть частью строки с временем (разделитель 'T').

    Returns:
        str: Дата в формате DD.MM.YYYY, либо сообщение об ошибке, если дата
             не указана или указана в неверном формате.
    """
    # Проверка на None (дата не указана)
    if date_ is None:
        return "Дата не указана"

    # Удаление пробелов в строке, если они есть
    if " " in date_:
        date_ = date_.replace(" ", "")

    # Разделение строки по 'T' (если дата включает время)
    date_split: list[str] = date_.split("T")

    try:
        # Парсинг даты из формата YYYY-MM-DD и преобразование в строку
        formatted_date_by_y_m_d: str = str(datetime.strptime(date_split[0], "%Y-%m-%d").date())
    except:
        # Обработка ошибки парсинга (неверный формат даты)
        return "Дата не указана или указана неверно. Формат ввода даты YYYY-MM-DD"
    else:
        # Разделение даты на компоненты (год, месяц, день)
        formatted_date_by_y_m_d_split: list[str] = formatted_date_by_y_m_d.split("-")

        # Сборка даты в формате DD.MM.YYYY
        formatted_date_by_d_m_y: str = ".".join(
            [formatted_date_by_y_m_d_split[-1], formatted_date_by_y_m_d_split[1], formatted_date_by_y_m_d_split[0]]
        )

        return formatted_date_by_d_m_y