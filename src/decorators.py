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
            log_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "data", "logs", filename
            ) if filename else None

            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok"
                return result

            except Exception as exc_info:
                inputs = args[0] if len(args) == 1 and not kwargs else (args if args else kwargs)
                log_message = f"{func.__name__} error: {str(exc_info)}. Inputs: {inputs}"
                raise
            finally:
                if filename:
                    with open(log_path, "a", encoding="utf-8") as file:
                        file.write(f"{log_message}\n")
                else:
                    print(log_message)

        return wrapper

    return log_inner
