import dataclasses

import numpy as np
import pytest
from numpy import nan
from numpy.testing import assert_array_equal

from .replace_nans import replace_nans


@dataclasses.dataclass
class ReplaceNansCase:
    matrix: np.ndarray
    result: np.ndarray


REPLACE_NANS_TEST_CASES = [
    ReplaceNansCase(
        matrix=np.array([[nan,  1,  2,  3], [4, nan,  5, nan]]),
        result=np.array([[3, 1, 2, 3], [4, 3, 5, 3]])),
    ReplaceNansCase(
        matrix=np.ones((3, 14)) * nan,
        result=np.zeros((3, 14))),
    ReplaceNansCase(
        matrix=np.array([[]]),
        result=np.array([[]])),
    ReplaceNansCase(
        matrix=np.array([[3]]),
        result=np.array([[3]])),
    ReplaceNansCase(
        matrix=np.array([[nan]]),
        result=np.array([[0]])),
    ReplaceNansCase(
        matrix=np.array([[1, nan]]),
        result=np.array([[1, 1]])),
    ReplaceNansCase(
        matrix=np.array([[0, nan,  2,  3,  4.],
                         [5,  6,  7,  8, nan],
                         [nan, 11, 12, 13, 14.],
                         [15, 16, 17, nan, 19.],
                         [20, 21, nan, 23, 24.]]),
        result=np.array([[0, 12,  2,  3,  4.],
                         [5,  6,  7,  8, 12.],
                         [12, 11, 12, 13, 14.],
                         [15, 16, 17, 12, 19.],
                         [20, 21, 12, 23, 24.]]))

]


@pytest.mark.parametrize('t', REPLACE_NANS_TEST_CASES, ids=str)
def test_construct_matrix(t: ReplaceNansCase) -> None:
    assert_array_equal(replace_nans(t.matrix), t.result)
