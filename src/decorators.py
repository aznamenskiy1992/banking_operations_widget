from typing import Union
from functools import wraps


def log(filename = None):
    def log_inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            return None
        return wrapper
    return log_inner
