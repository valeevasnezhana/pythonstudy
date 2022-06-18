import typing as tp


def traverse_dictionary_immutable(
        dct: tp.Mapping[str, tp.Any],
        prefix: str = "") -> list[tuple[str, int]]:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :param prefix: prefix for key used for passing total path through recursion
    :return: list with pairs: (full key from root to leaf joined by ".", value)
    """
    result = []

    for key, value in dct.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            result += traverse_dictionary_immutable(value, full_key)
        else:
            result.append((full_key, value))

    return result


def traverse_dictionary_mutable(
        dct: tp.Mapping[str, tp.Any],
        result: list[tuple[str, int]],
        prefix: str = "") -> None:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :param result: list with pairs: (full key from root to leaf joined by ".", value)
    :param prefix: prefix for key used for passing total path through recursion
    :return: None
    """
    for key, value in dct.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            traverse_dictionary_mutable(value, result, full_key)
        else:
            result.append((full_key, value))


def traverse_dictionary_iterative(
        dct: tp.Mapping[str, tp.Any]
        ) -> list[tuple[str, int]]:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :return: list with pairs: (full key from root to leaf joined by ".", value)
    """
    stack = [(dct, "")]
    result = []
    while stack:
        dct, prefix = stack.pop()
        for key, value in dct.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                stack.append((value, full_key))
            else:
                result.append((full_key, value))
    return result
