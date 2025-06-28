from src.utils import get_transactions
from src.transactions_from_files import get_transactions_from_csv, get_transactions_from_xlsx
from src.processing import filter_by_state
from src.widget import get_date, mask_account_card


def select_file(question_and_correct_answer: dict) -> list[dict]:
    """Функция запрашивает у пользователя откуда получать данные и возвращает список операций"""
    while True:
        selected_file = input(question_and_correct_answer["question"])
        if selected_file in question_and_correct_answer["options"]:
            break

    if selected_file == question_and_correct_answer["options"][0]:
        src_operations = get_transactions("data/operations.json")
        print("Для обработки выбран JSON-файл.")
    elif selected_file == question_and_correct_answer["options"][1]:
        src_operations = get_transactions_from_csv("data/transactions.csv")
        print("Для обработки выбран CSV-файл.")
    elif selected_file == question_and_correct_answer["options"][2]:
        src_operations = get_transactions_from_xlsx("data/transactions_excel.xlsx")
        print("Для обработки выбран XLSX-файл.")

    return src_operations


def select_status(question_and_correct_answer: dict, operations: list[dict]) -> list[dict]:
    """Функция запрашивает у пользователя статус для фильтрации и возвращает список операций"""
    while True:
        selected_status = input(question_and_correct_answer["question"]).lower()

        if selected_status in question_and_correct_answer["options"]:
            break
        else:
            print(f"Статус операции {selected_status} недоступен.")

    filtered_operations = filter_by_state(operations, selected_status.upper())

    print(f"Операции отфильтрованы по статусу {selected_status}")

    return filtered_operations


def select_need_sort_by_date(question_and_correct_answer: list[dict], operations: list[dict]) -> list[dict]:
    """Функция запрашивает у пользователя необходимость сортировки по дате и направление сортировки и возвращает список операций"""
    while True:
        needed_sorted_by_date = input(question_and_correct_answer[0]["question"]).lower()

        if needed_sorted_by_date in question_and_correct_answer[0]["options"]:
            break

    if needed_sorted_by_date == "нет":
        return operations


def select_need_just_rub_operations(question_and_correct_answer: dict, operations: list[dict]) -> list[dict]:
    """Функция запрашивает у пользователя необходимость выбора только рублёвых транзакций и возвращает список операций"""
    while True:
        needed_print_just_rub = input(question_and_correct_answer["question"]).lower()

        if needed_print_just_rub in question_and_correct_answer["options"]:
            break

    if needed_print_just_rub == "нет":
        return operations


def select_filter_by_description(question_and_correct_answer: list[dict], operations: list[dict]) -> list[dict]:
    """Функция запрашивает у пользователя необходимость фильтрации по слову в описании и возвращает список операций"""
    while True:
        needed_filter_by_description = input(question_and_correct_answer["question"]).lower()

        if needed_filter_by_description in question_and_correct_answer["options"]:
            break

    if needed_filter_by_description == "нет":
        return operations


def prepare_result(operations: list[dict]) -> list:
    """Функция подготавливает отфильтрованные операции к выводу в консоль"""
    result = []

    for i in range(len(operations)):
        temp_date_and_type = f"{get_date(operations[i]["date"])} {operations[i]["description"]}\n"

        if "from" not in operations[i].keys():
            temp_from_to = f"{mask_account_card(operations[i]["to"])}\n"
        else:
            temp_from_to = f"{mask_account_card(operations[i]["from"])} -> {mask_account_card(operations[i]["to"])}\n"

        temp_amount = f"Сумма: {operations[i]["operationAmount"]["amount"]} {operations[i]["operationAmount"]["currency"]["name"]}"

        result.append(temp_date_and_type + temp_from_to + temp_amount)

    return result


def main() -> None:
    """Функция возвращает отфильтрованные операции"""
    QUESTIONS_AND_CORRECT_ANSWERS = {
        1: {
            "question": """Выберите необходимый пункт меню:
            1. Получить информацию о транзакциях из JSON-файла
            2. Получить информацию о транзакциях из CSV-файла
            3. Получить информацию о транзакциях из XLSX-файла""",
            "options": ["1", "2", "3"]
        },
        2: {
            "question": """Введите статус, по которому необходимо выполнить фильтрацию.
            Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING""",
            "options": ["executed", "canceled", "pending"]
        },
        3: {
            "question": "Отсортировать операции по дате? Да/Нет",
            "options": ["да", "нет"]
        },
        4: {
            "question": "Отсортировать по возрастанию или по убыванию",
            "options": ["по возрастанию", "по убыванию"]
        },
        5: {
            "question": "Выводить только рублевые транзакции? Да/Нет",
            "options": ["да", "нет"]
        },
        6: {
            "question": "Отфильтровать список транзакций по определенному слову в описании? Да/Нет",
            "options": ["да", "нет"]
        },
    }

    # Приветствие (начало работы программы)
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # Выбор откуда получаем данные (шаг 1)
    src_operations = select_file(QUESTIONS_AND_CORRECT_ANSWERS[1])

    # Выбор статуса операции (шаг 2)
    filtered_by_status = select_status(QUESTIONS_AND_CORRECT_ANSWERS[2], src_operations)

    # Сортировка по дате (шаг 3 и 4)
    sorted_by_date = select_need_sort_by_date([QUESTIONS_AND_CORRECT_ANSWERS[3], QUESTIONS_AND_CORRECT_ANSWERS[4]], filtered_by_status)

    # Выбор только рублёвых операций (шаг 5)
    selected_just_rub_operations = select_need_just_rub_operations(QUESTIONS_AND_CORRECT_ANSWERS[5], sorted_by_date)

    # Фильтрация по слову в описании (шаг 6)
    filtered_by_description = select_filter_by_description(QUESTIONS_AND_CORRECT_ANSWERS[6], selected_just_rub_operations)

    # Подготавливаем операции к выводу в консоль
    result = prepare_result(filtered_by_description)

    print("Распечатываю итоговый список транзакций...")

    print(f"""Всего банковских операций в выборке: {len(result)}
    
    {"\n".join(result)}
    """)
