import numpy as np


def replace_nans(matrix: np.ndarray) -> np.ndarray:
    """
    Replace all nans in matrix with average of other values.
    If all values are nans, then return zero matrix of the same size.
    :param matrix: matrix,
    :return: replaced matrix
    """
    replaced_matrix = matrix.flatten()
    ids = np.array(np.where(np.isnan(replaced_matrix))[0])
    mean = np.nanmean(replaced_matrix)
    if np.isnan(mean):
        return np.zeros(matrix.shape)
    replaced_matrix[ids] = mean
    return replaced_matrix.reshape(matrix.shape)
