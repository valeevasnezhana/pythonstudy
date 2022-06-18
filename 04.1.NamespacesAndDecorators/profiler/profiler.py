import functools
from datetime import datetime


def profiler(func):  # type: ignore
    """
    Returns profiling decorator, which counts calls of function
    and measure last function execution time.
    Results are stored as function attributes: `calls`, `last_time_taken`
    :param func: function to decorate
    :return: decorator, which wraps any function passed
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        flag = not wrapper.in_recursion
        if flag:
            wrapper.calls = 0
            wrapper.in_recursion = True
        wrapper.calls += 1
        start_time = datetime.now()
        value = func(*args, **kwargs)
        func_time = datetime.now() - start_time
        wrapper.last_time_taken = float(func_time.seconds) + func_time.microseconds/1000000
        if flag:
            wrapper.in_recursion = False
        return value
    wrapper.in_recursion = False
    return wrapper
