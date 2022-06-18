import pytest

from .range import Range


def test_basic() -> None:
    n = 0
    for i in Range(10):
        n += i
    assert n == 45

    n = 0
    for i in Range(0, 10, 2):
        n += i
    assert n == 20


def test_renewable() -> None:
    range_ = Range(3)
    n = 0
    for i in range_:
        n += 1
    assert n == 3

    for i in range_:
        n += 1
    assert n == 6


def test_fast() -> None:
    for i in range(10000):
        assert 1000000 not in range(1000000)
        assert 1000000 not in Range(1000000)


def test_repr() -> None:
    assert str(range(10)) == str(Range(10))
    assert str(range(10, 20)) == str(Range(10, 20))
    assert str(range(10, 20, 2)) == str(Range(10, 20, 2))
    assert str(range(10, 20, 1)) == str(Range(10, 20, 1))


def test_len() -> None:
    assert len(range(100)) == len(Range(100))
    assert len(range(3, 33, 7)) == len(Range(3, 33, 7))
    assert len(range(10, 3, -3)) == len(Range(10, 3, -3))
    assert len(range(10, 0, -1)) == len(Range(10, 0, -1))
    assert len(range(10, 0)) == len(Range(10, 0))
    assert len(range(0, 10, -1)) == len(Range(0, 10, -1))


def test_stop() -> None:
    with pytest.raises(StopIteration):
        range_ = iter(Range(3))
        for _ in range(4):
            next(range_)


def test_access() -> None:
    for i in range(2):
        assert range(1, 3)[i] == Range(1, 3)[i]


def test_negative() -> None:
    assert list(range(3, 0, -1)) == list(Range(3, 0, -1))
    assert list(range(3, -10, -3)) == list(Range(3, -10, -3))
    assert 5 in Range(10, 0, -1)
