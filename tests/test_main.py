import pytest
from unittest.mock import patch

from main import main


@patch("builtins.input")
@patch("main.get_transactions_from_csv")
@patch("main.get_transactions")
@pytest.mark.parametrize(
    "input_values, filtered_operations",
    [
        # Без сортировки по дате
        # Без вывода только RUB транзакций
        # Без фильтрации по слову в описании
        (
            {
                "Пункт меню": "1",
                "Статус для фильтрации": "Executed",
                "Сортировка по дате": "нет",
                "Вывод только руб": "нет",
                "Фильтрация по слову": "нет",
            },
            """Всего банковских операций в выборке: 4

26.08.2019 Перевод организации
Maestro 1596 83** **** 5199 -> Счет **9589
Сумма: 31957.58 руб.

30.06.2018 Перевод организации
Счет **6952 -> Счет **6702
Сумма: 9824.07 USD

23.03.2018 Открытие вклада
Счет **2431
Сумма: 48223.05 руб.

19.08.2018 Перевод с карты на карту
Visa Classic 6831 98** **** 7658 -> Visa Platinum 8990 92** **** 5229
Сумма: 56883.54 USD"""
        ),
        # C сортировкой по дате
        # Без вывода только RUB транзакций
        # Без фильтрации по слову в описании
        (
            {
                "Пункт меню": "2",
                "Статус для фильтрации": "Executed",
                "Сортировка по дате": "да",
                "Направление сортировки": "По убыванию",
                "Вывод только руб": "нет",
                "Фильтрация по слову": "нет",
            },
            """Всего банковских операций в выборке: 4

26.08.2019 Перевод организации
Maestro 1596 83** **** 5199 -> Счет **9589
Сумма: 31957.58 руб.

19.08.2018 Перевод с карты на карту
Visa Classic 6831 98** **** 7658 -> Visa Platinum 8990 92** **** 5229
Сумма: 56883.54 USD

30.06.2018 Перевод организации
Счет **6952 -> Счет **6702
Сумма: 9824.07 USD

23.03.2018 Открытие вклада
Счет **2431
Сумма: 48223.05 руб."""
        )
    ]
)
def test_print_filtered_operation(mock_json, mock_csv, mock_input, input_values, filtered_operations, operations_for_main, capsys):
    """Тестирует вывод отфильтрованных операций в консоль"""

    # Значения из файлов
    mock_json.return_value = operations_for_main
    mock_csv.return_value = operations_for_main

    # Значения для input
    input_values_list = [value for value in input_values.values()]
    mock_input.side_effect = input_values_list

    main()

    captured = capsys.readouterr()
    assert filtered_operations in captured.out
