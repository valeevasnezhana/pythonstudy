import numpy as np


def add_zeros(x: np.ndarray) -> np.ndarray:
    """
    Add zeros between values of given array
    :param x: array,
    :return: array with zeros inserted
    """
    return np.insert(x, range(1, len(x)), 0)

