import os
from functools import wraps


def log(filename=None):
    """Декоратор, который логирует информацию об операциях в файл mylog.txt или в консоль"""

    def log_inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if filename is not None and filename != "mylog.txt":
                raise ValueError("Неверное название файла логов. Должно быть 'mylog.txt'")

            try:
                func(*args, **kwargs)
            except Exception as exc_info:
                inputs = args[0] if len(args) == 1 and not kwargs else (args if args else kwargs)

                if filename is not None:
                    with open(
                        os.path.join(
                            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "logs", filename
                        ),
                        "a",
                        encoding="utf-8",
                    ) as file:
                        file.write(f"{func.__name__} error: {str(exc_info)}. Inputs: {inputs}\n")

                else:
                    print(f"{func.__name__} error: {str(exc_info)}. Inputs: {inputs}")
            else:
                if filename is not None:
                    with open(
                        os.path.join(
                            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "logs", filename
                        ),
                        "a",
                        encoding="utf-8",
                    ) as file:
                        file.write(f"{func.__name__} ok\n")

                else:
                    print(f"{func.__name__} ok")
            return None

        return wrapper

    return log_inner
