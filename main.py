from src.utils import get_transactions
from src.transactions_from_files import get_transactions_from_csv, get_transactions_from_xlsx
from src.processing import filter_by_state, sort_by_date
from src.widget import get_date, mask_account_card
from src.generators import filter_by_currency


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
    while True:
        selected_file = input(QUESTIONS_AND_CORRECT_ANSWERS[1]["question"])
        if selected_file in QUESTIONS_AND_CORRECT_ANSWERS[1]["options"]:
            break

    # Получаем данные из файлов
    if selected_file == QUESTIONS_AND_CORRECT_ANSWERS[1]["options"][0]:
        operations = get_transactions("data/operations.json")
        print("Для обработки выбран JSON-файл.")
    elif selected_file == QUESTIONS_AND_CORRECT_ANSWERS[1]["options"][1]:
        operations = get_transactions_from_csv("data/transactions.csv")
        print("Для обработки выбран CSV-файл.")
    elif selected_file == QUESTIONS_AND_CORRECT_ANSWERS[1]["options"][2]:
        operations = get_transactions_from_xlsx("data/transactions_excel.xlsx")
        print("Для обработки выбран XLSX-файл.")

    # Выбор статуса операции (шаг 2)
    while True:
        selected_status = input(QUESTIONS_AND_CORRECT_ANSWERS[2]["question"]).lower()
        if selected_status in QUESTIONS_AND_CORRECT_ANSWERS[2]["options"]:
            break
        else:
            print(f"Статус операции {selected_status} недоступен.")

    # Фильтруем операции по статусу
    filtered_operations = filter_by_state(operations, selected_status.upper())
    print(f"Операции отфильтрованы по статусу {selected_status}")

    # Необходимость сортировки по дате (шаг 3)
    while True:
        needed_sorted_by_date = input(QUESTIONS_AND_CORRECT_ANSWERS[3]["question"]).lower()
        if needed_sorted_by_date in QUESTIONS_AND_CORRECT_ANSWERS[3]["options"]:
            break

    # Выбор направления сортировки (шаг 4)
    if needed_sorted_by_date == "да":
        while True:
            sorting_direction = input(QUESTIONS_AND_CORRECT_ANSWERS[4]["question"]).lower()
            if sorting_direction in QUESTIONS_AND_CORRECT_ANSWERS[4]["options"]:
                break

        # Сортируем по дате
        if sorting_direction == "по возрастанию":
            filtered_operations = sort_by_date(filtered_operations, "False")
        else:
            filtered_operations = sort_by_date(filtered_operations)

    # Необходимость вывода только рублёвых операций (шаг 5)
    while True:
        needed_print_just_rub = input(QUESTIONS_AND_CORRECT_ANSWERS[5]["question"]).lower()
        if needed_print_just_rub in QUESTIONS_AND_CORRECT_ANSWERS[5]["options"]:
            break

    if needed_print_just_rub == "да":
        # Выводим только рублёвые операции
        generator = filter_by_currency(filtered_operations, "руб.")
        filtered_operations = [element for element in generator]

    # Необходимость отфильтровать операции по слову в описании (шаг 6)
    while True:
        needed_filter_by_description = input(QUESTIONS_AND_CORRECT_ANSWERS[6]["question"]).lower()
        if needed_filter_by_description in QUESTIONS_AND_CORRECT_ANSWERS[6]["options"]:
            break

    # Подготавливаем операции к выводу в консоль
    result = []

    for i in range(len(filtered_operations)):
        temp_date_and_type = f"{get_date(filtered_operations[i]["date"])} {filtered_operations[i]["description"]}\n"

        if "from" not in filtered_operations[i].keys():
            temp_from_to = f"{mask_account_card(filtered_operations[i]["to"])}\n"
        else:
            temp_from_to = f"{mask_account_card(filtered_operations[i]["from"])} -> {mask_account_card(filtered_operations[i]["to"])}\n"

        temp_amount = f"Сумма: {filtered_operations[i]["operationAmount"]["amount"]} {filtered_operations[i]["operationAmount"]["currency"]["name"]}"

        result.append(temp_date_and_type + temp_from_to + temp_amount)

    # Выводим результат в консоль
    print("Распечатываю итоговый список транзакций...")
    print(f"""Всего банковских операций в выборке: {len(result)}

{"\n\n".join(result)}""", end="")
