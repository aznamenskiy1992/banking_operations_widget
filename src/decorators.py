import os
from functools import wraps


def log(filename=None):
    """
    Декоратор для логирования выполнения функций с записью в файл или выводом в консоль.

    Параметры:
        filename (str|None): Имя файла для логирования. Допустимые значения:
            - None: вывод логов в консоль
            - Запись логов в файл в директории data/logs
            Другие значения не допускаются

    Возвращает:
        function: Декоратор, добавляющий логирование к целевой функции

    Особенности:
        - Логирует успешное выполнение и ошибки
        - Для ошибок сохраняет тип исключения и входные параметры
        - Сохраняет оригинальные атрибуты функции (__name__, __doc__)
        - При ошибках пробрасывает исключение после логирования
        - Возвращает результат оригинальной функции
    """

    def log_inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Формируем путь к файлу логов (если filename указан)
            log_path = (
                os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "logs", filename)
                if filename
                else None
            )

            try:
                # Пытаемся выполнить декорируемую функцию
                result = func(*args, **kwargs)
                # Формируем сообщение об успешном выполнении
                log_message = f"{func.__name__} ok"
                return result  # Возвращаем результат оригинальной функции

            except Exception as exc_info:
                # Формируем информацию о входных параметрах:
                # Если передан один позиционный аргумент и нет именованных - берем первый аргумент
                # Иначе берем все аргументы или именованные параметры
                inputs = args[0] if len(args) == 1 and not kwargs else (args if args else kwargs)
                # Формируем сообщение об ошибке
                log_message = f"{func.__name__} error: {str(exc_info)}. Inputs: {inputs}"
                raise  # Пробрасываем исключение дальше после логирования

            finally:
                # Записываем лог в файл или выводим в консоль
                if filename:
                    # Открываем файл в режиме добавления (append)
                    with open(log_path, "a", encoding="utf-8") as file:
                        file.write(f"{log_message}\n")  # Записываем сообщение
                else:
                    print(log_message)  # Выводим сообщение в консоль

        return wrapper

    return log_inner
