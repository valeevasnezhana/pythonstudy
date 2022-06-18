import typing as tp

R = tp.TypeVar("R", bool, int, float)
T1 = tp.TypeVar("T1")
T2 = tp.TypeVar("T2")
T3 = tp.TypeVar("T3")


def f(a: tp.Callable[[T1, T2, T3], R], b: T1, c: T2, d: T3) -> R:
    return a(b, c, d)


TEST_SAMPLES = """
# SUCCESS
def g(a: float, b: float, c: complex) -> int:
    return 1

f(g, 1, 4.5, 1j)

# SUCCESS
def g(a: complex, b: complex, c: complex) -> bool:
    return True

f(g, 1, 4, True)

# ERROR
def g(a: bool, b: float, c: complex) -> int:
    return 1

f(g, 1, 4.5, 1j)

# ERROR
def g(a: int, b: int, c: complex) -> int:
    return 1

f(g, 1, 4.5, 1j)

# ERROR
def g(a: int, b: float, c: float) -> int:
    return 1

f(g, 1, 4.5, 1j)

# SUCCESS
def g(a: float, b: float, c: complex) -> float:
    return 1.0

f(g, True, True, True)

# ERROR
def g(a: float, b: float, c: complex) -> complex:
    return 1j

f(g, True, True, True)
"""
