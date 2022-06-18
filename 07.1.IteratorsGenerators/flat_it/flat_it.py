from typing import Iterable, Generator, Any


def flat_it_recursive(sequence: Iterable[Any]) -> Generator[Any, None, None]:
    """
    :param sequence: sequence with arbitrary level of nested iterables
    :return: generator producing flatten sequence
    """
    try:
        for element in sequence:
            if element != sequence:
                yield from flat_it_recursive(element)
            else:  # for strings with 1 symbol
                yield element
    except TypeError:
        yield sequence


def flat_it(sequence: Iterable[Any]) -> Generator[Any, None, None]:
    """
    :param sequence: sequence with arbitrary level of nested iterables
    :return: generator producing flatten sequence
    """
    stack = [(sequence, iter(sequence))]
    while stack:
        sequence, sequence_iter = stack.pop()
        while True:
            try:
                element = next(sequence_iter)
            except StopIteration:
                break

            try:
                element_iter = iter(element)
            except TypeError:
                yield element
                continue

            if element != sequence:
                stack.append((sequence, sequence_iter))
                stack.append((element, element_iter))
            else:  # for string with 1 symbol
                yield element
            break
