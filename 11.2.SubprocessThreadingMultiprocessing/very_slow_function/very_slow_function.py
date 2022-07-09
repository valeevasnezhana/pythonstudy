import time
import typing as tp
import multiprocessing
from concurrent.futures import ThreadPoolExecutor


def very_slow_function(x: int) -> int:
    """Function which calculates square of given number really slowly
    :param x: given number
    :return: number ** 2
    """
    time.sleep(0.3)
    return x ** 2

def calc_squares_simple(bound: int) -> tp.List[int]:
    """Function that calculates squares of numbers in range [0; bound)
    :param bound: positive upper bound for range
    :return: list of squared numbers
    """
    result = []
    for i in range(bound):
        result.append(very_slow_function(i))
    return result


def _part_calc_squares(_args: tuple[int, int, int]) -> list[tuple[int, int]]:
    result = []
    for i in range(*_args):
        result.append((i, very_slow_function(i)))
    return result


def calc_squares_multithreading(bound: int) -> tp.List[int]:
    """Function that calculates squares of numbers in range [0; bound)
    using threading.Thread
    :param bound: positive upper bound for range
    :return: list of squared numbers
    """
    threads_count = multiprocessing.cpu_count()
    result = [0] * bound
    with ThreadPoolExecutor(max_workers=threads_count) as executor:
        results = executor.map(
            _part_calc_squares,
            ((i, bound, threads_count) for i in range(threads_count))
        )
        for r in results:
            for i, square in r:
                result[i] = square
    return result


def calc_squares_multiprocessing(bound: int) -> tp.List[int]:
    """Function that calculates squares of numbers in range [0; bound)
    using multiprocessing.Pool
    :param bound: positive upper bound for range
    :return: list of squared numbers
    """
    processes_count = multiprocessing.cpu_count()
    result = [0] * bound
    with multiprocessing.Pool(processes_count) as pool:
        results = pool.map(
            _part_calc_squares,
            ((i, bound, processes_count) for i in range(processes_count))
        )
        for r in results:
            for i, square in r:
                result[i] = square
    return result
