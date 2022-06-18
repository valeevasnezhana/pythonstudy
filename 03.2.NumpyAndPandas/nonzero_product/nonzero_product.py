import typing as tp

import numpy as np


def nonzero_product(matrix: np.ndarray) -> tp.Optional[float]:
    """
    Compute product of nonzero diagonal elements of matrix
    If all diagonal elements are zeros, then return None
    :param matrix: array,
    :return: product value or None
    """
    nonzero = np.diagonal(matrix)
    nonzero = nonzero[nonzero != 0]
    if nonzero.any():
        return np.product(nonzero)
