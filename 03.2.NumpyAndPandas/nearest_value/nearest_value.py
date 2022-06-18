import typing as tp

import numpy as np


def nearest_value(matrix: np.ndarray, value: float) -> tp.Optional[float]:
    """
    Find nearest value in matrix.
    If matrix is empty return None
    :param matrix: input matrix
    :param value: value to find
    :return: nearest value in matrix or None
    """
    arr = matrix.ravel()
    if len(arr) != 0:
        nearest_value_id = np.argmin(np.abs(arr - value))
        return arr[nearest_value_id]
