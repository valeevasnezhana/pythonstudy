from typing import Generator, Any
from itertools import chain


def transpose(matrix: list[list[Any]]) -> list[list[Any]]:
    """
    :param matrix: rectangular matrix
    :return: transposed matrix
    """
    return [list(cells) for cells in zip(*matrix)]


def uniq(sequence: list[Any]) -> Generator[Any, None, None]:
    """
    :param sequence: arbitrary sequence of comparable elements
    :return: generator of elements of `sequence` in
    the same order without duplicates
    """
    uniques: set[Any] = set()
    for element in sequence:
        if element not in uniques:
            uniques.add(element)
            yield element


def dict_merge(*dicts: dict[Any, Any]) -> dict[Any, Any]:
    """
    :param *dicts: flat dictionaries to be merged
    :return: merged dictionary
    """
    return dict(chain.from_iterable(dict_.items() for dict_ in dicts))


def product(lhs: list[int], rhs: list[int]) -> int:
    """
    :param rhs: first factor
    :param lhs: second factor
    :return: scalar product
    """
    return sum(x * y for x, y in zip(lhs, rhs))
