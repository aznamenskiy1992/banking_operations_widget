from src.filter_transactions import process_bank_search
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.transactions_from_files import get_transactions_from_csv, get_transactions_from_xlsx
from src.utils import get_transactions
from src.widget import get_date, mask_account_card


def main() -> None:
    """
    Основная функция программы для работы с банковскими транзакциями.

    Функция предоставляет интерактивный интерфейс для:
    - Выбора источника данных (JSON/CSV/XLSX)
    - Фильтрации транзакций по статусу
    - Сортировки по дате
    - Фильтрации по валюте
    - Поиска по описанию
    - Форматированного вывода результатов

    Возвращает:
        None: Функция не возвращает значений, только выводит результаты в консоль

    Особенности:
        - Интерактивное меню с валидацией ввода
        - Поддержка нескольких форматов исходных данных
        - Многоступенчатая фильтрация транзакций
        - Форматированный вывод результатов
        - Обработка всех возможных ошибок ввода

    Пример использования:
        >>> main()
        Привет! Добро пожаловать в программу работы с банковскими транзакциями.
        [Выводится интерактивное меню...]
    """
    # Словарь с вопросами и допустимыми ответами для меню
    QUESTIONS_AND_CORRECT_ANSWERS = {
        1: {
            "question": """Выберите необходимый пункт меню:
            1. Получить информацию о транзакциях из JSON-файла
            2. Получить информацию о транзакциях из CSV-файла
            3. Получить информацию о транзакциях из XLSX-файла""",
            "options": ["1", "2", "3"],
        },
        2: {
            "question": """Введите статус, по которому необходимо выполнить фильтрацию.
            Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING""",
            "options": ["executed", "canceled", "pending"],
        },
        3: {"question": "Отсортировать операции по дате? Да/Нет", "options": ["да", "нет"]},
        4: {"question": "Отсортировать по возрастанию или по убыванию", "options": ["по возрастанию", "по убыванию"]},
        5: {"question": "Выводить только рублевые транзакции? Да/Нет", "options": ["да", "нет"]},
        6: {
            "question": "Отфильтровать список транзакций по определенному слову в описании? Да/Нет",
            "options": ["да", "нет"],
        },
    }

    EMPTY_RESULTS_MESSAGE = "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации"

    # Приветствие пользователя
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # Шаг 1: Выбор источника данных
    while True:
        selected_file = input(QUESTIONS_AND_CORRECT_ANSWERS[1]["question"])
        if selected_file in QUESTIONS_AND_CORRECT_ANSWERS[1]["options"]:
            break

    # Загрузка данных из выбранного файла
    if selected_file == QUESTIONS_AND_CORRECT_ANSWERS[1]["options"][0]:
        operations = get_transactions("data/operations.json")
        print("Для обработки выбран JSON-файл.")
    elif selected_file == QUESTIONS_AND_CORRECT_ANSWERS[1]["options"][1]:
        operations = get_transactions_from_csv("data/transactions.csv")
        print("Для обработки выбран CSV-файл.")
    elif selected_file == QUESTIONS_AND_CORRECT_ANSWERS[1]["options"][2]:
        operations = get_transactions_from_xlsx("data/transactions_excel.xlsx")
        print("Для обработки выбран XLSX-файл.")

    # Шаг 2: Фильтрация по статусу операции
    while True:
        selected_status = input(QUESTIONS_AND_CORRECT_ANSWERS[2]["question"]).lower()
        if selected_status in QUESTIONS_AND_CORRECT_ANSWERS[2]["options"]:
            break
        else:
            print(f"Статус операции {selected_status} недоступен.")

    filtered_operations = filter_by_state(operations, selected_status.upper())

    # Проверка наличия операций после фильтрации
    if filtered_operations == "Нет словарей со значением state":
        print(EMPTY_RESULTS_MESSAGE, end="")
        return
    else:
        print(f"Операции отфильтрованы по статусу {selected_status}")

    # Шаг 3-4: Сортировка по дате
    while True:
        needed_sorted_by_date = input(QUESTIONS_AND_CORRECT_ANSWERS[3]["question"]).lower()
        if needed_sorted_by_date in QUESTIONS_AND_CORRECT_ANSWERS[3]["options"]:
            break

    if needed_sorted_by_date == "да":
        while True:
            sorting_direction = input(QUESTIONS_AND_CORRECT_ANSWERS[4]["question"]).lower()
            if sorting_direction in QUESTIONS_AND_CORRECT_ANSWERS[4]["options"]:
                break

        # Применение сортировки
        if sorting_direction == "по возрастанию":
            filtered_operations = sort_by_date(filtered_operations, "False")
        else:
            filtered_operations = sort_by_date(filtered_operations)

    # Шаг 5: Фильтрация по рублевым операциям
    while True:
        needed_print_just_rub = input(QUESTIONS_AND_CORRECT_ANSWERS[5]["question"]).lower()
        if needed_print_just_rub in QUESTIONS_AND_CORRECT_ANSWERS[5]["options"]:
            break

    if needed_print_just_rub == "да":
        generator = filter_by_currency(filtered_operations, "руб.")
        filtered_operations = [element for element in generator]

        if not filtered_operations:
            print(EMPTY_RESULTS_MESSAGE, end="")
            return

    # Шаг 6: Фильтрация по описанию
    while True:
        needed_filter_by_description = input(QUESTIONS_AND_CORRECT_ANSWERS[6]["question"]).lower()
        if needed_filter_by_description in QUESTIONS_AND_CORRECT_ANSWERS[6]["options"]:
            break

    if needed_filter_by_description == "да":
        search_str = input("Введите слово по которому нужно отсортировать транзакции")
        filtered_operations = process_bank_search(filtered_operations, search_str)

        if not filtered_operations:
            print(EMPTY_RESULTS_MESSAGE, end="")
            return

    # Подготовка результатов для вывода
    result = []
    for i in range(len(filtered_operations)):
        # Форматирование даты и типа операции
        temp_date_and_type = f"{get_date(filtered_operations[i]["date"])} {filtered_operations[i]["description"]}\n"

        # Форматирование информации об отправителе/получателе
        if "from" not in filtered_operations[i].keys():
            temp_from_to = f"{mask_account_card(filtered_operations[i]["to"])}\n"
        else:
            temp_from_to = (
                f"{mask_account_card(filtered_operations[i]["from"])}"
                + " -> "
                + f"{mask_account_card(filtered_operations[i]["to"])}\n"
            )

        # Форматирование суммы операции
        temp_amount = (
            "Сумма: "
            + f"{filtered_operations[i]["operationAmount"]["amount"]} "
            + f"{filtered_operations[i]["operationAmount"]["currency"]["name"]}"
        )

        result.append(temp_date_and_type + temp_from_to + temp_amount)

    # Вывод результатов
    print("Распечатываю итоговый список транзакций...")
    print(
        f"""Всего банковских операций в выборке: {len(result)}

{"\n\n".join(result)}""",
        end="",
    )

    return
