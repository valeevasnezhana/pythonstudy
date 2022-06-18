import numpy as np


def vander(array: np.ndarray) -> np.ndarray:
    """
    Create a Vandermonde matrix from the given vector.
    :param array: input array,
    :return: vandermonde matrix
    """
    degrees = np.arange(len(array))
    return np.power(array[:, np.newaxis], degrees)
