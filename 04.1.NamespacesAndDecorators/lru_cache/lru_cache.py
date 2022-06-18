import functools
from collections import OrderedDict
from typing import Callable, Any, TypeVar, cast

Function = TypeVar('Function', bound=Callable[..., Any])


def cache(max_size: int) -> Callable[[Function], Function]:
    """
    Returns decorator, which stores result of function
    for `max_size` most recent function arguments.
    :param max_size: max amount of unique arguments to store values for
    :return: decorator, which wraps any function passed
    """
    def _cache(func):
        cache_dict = OrderedDict([])
        sentinel = object()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_dict_key = (
                args,
                tuple((key, kwargs[key]) for key in sorted(kwargs))
            )
            value = cache_dict.get(cache_dict_key, sentinel)
            if value is not sentinel:
                cache_dict.move_to_end(cache_dict_key, last=True)
                return value
            value = func(*args, **kwargs)
            cache_dict[cache_dict_key] = value
            if len(cache_dict) > max_size:
                cache_dict.popitem(last=False)
            return value

        return cast(Function, wrapper)
    return _cache


