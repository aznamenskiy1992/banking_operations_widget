from typing import Union
from functools import wraps
import os


project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_address = os.path.join(project_root, "data", "logs", "mylog.txt")

def log(filename = None):
    """Декоратор, который логирует информацию об операциях в файл mylog.txt или в консоль"""
    def log_inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if filename is not None:
                try:
                    result = func(*args, **kwargs)
                except Exception as exc_info:
                    inputs = args[0] if len(args) == 1 and not kwargs else (args if args else kwargs)
                    with open(file_address, "a", encoding="utf-8") as file:
                        file.write(f"{func.__name__} error: {str(exc_info)}. Inputs: {inputs}\n")
                else:
                    with open(file_address, "a", encoding="utf-8") as file:
                        file.write(f"{func.__name__} ok\n")
            return None
        return wrapper
    return log_inner
