import os
from functools import wraps


def log(filename=None):
    """
    Декоратор для логирования результатов выполнения функций.

    Логи могут записываться в файл 'в директории data/logs,
    либо выводиться в консоль, если filename не указан.

    Параметры:
        filename: str | None - имя файла для записи логов. Должно быть либо None,
                  либо строго 'mylog.txt'. Если None - логи выводятся в консоль.

    Возвращает:
        Декоратор функции, который добавляет логирование работы обернутой функции.

    Особенности:
        1. Логирует как успешное выполнение, так и ошибки
        2. Для ошибок дополнительно записывает информацию об исключении и входных данных
        3. Сохраняет оригинальное имя и docstring обернутой функции (благодаря @wraps)
        4. Файлы логов создаются в директории data/logs относительно расположения скрипта
    """

    def log_inner(func):
        @wraps(func)  # Сохраняем метаинформацию оригинальной функции
        def wrapper(*args, **kwargs):
            try:
                # Пытаемся выполнить декорируемую функцию
                func(*args, **kwargs)
            except Exception as exc_info:
                # Формируем информацию о входных данных
                inputs = args[0] if len(args) == 1 and not kwargs else (args if args else kwargs)

                if filename is not None:
                    # Формируем путь к файлу логов
                    log_path = os.path.join(
                        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "logs", filename
                    )
                    # Записываем ошибку в лог-файл
                    with open(log_path, "a", encoding="utf-8") as file:
                        file.write(f"{func.__name__} error: {str(exc_info)}. Inputs: {inputs}\n")
                else:
                    # Выводим ошибку в консоль
                    print(f"{func.__name__} error: {str(exc_info)}. Inputs: {inputs}")
            else:
                # Если выполнение прошло без ошибок
                if filename is not None:
                    log_path = os.path.join(
                        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "logs", filename
                    )
                    with open(log_path, "a", encoding="utf-8") as file:
                        file.write(f"{func.__name__} ok\n")
                else:
                    print(f"{func.__name__} ok")
            return None

        return wrapper

    return log_inner
