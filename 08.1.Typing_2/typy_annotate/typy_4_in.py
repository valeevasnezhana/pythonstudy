import typing as tp

T = tp.TypeVar("T", int, str)


def f(a: tp.Container[T], b: T) -> tp.Optional[T]:
    return b if b in a else None


TEST_SAMPLES = """
# SUCCESS

a: tp.Optional[float]
a = f([1, 2, 3], 1)
if a is not None:
    a += 1

# SUCCESS
a: tp.Optional[float]
a = f({1, 2, 3}, 1)


# SUCCESS
a: tp.Optional[str]
a = f("abcd", "a")

# SUCCESS
class A:
    def __contains__(self, a: object) -> bool:
        return True

a: tp.Optional[int]
a = f(A(), 10)

b: tp.Optional[str]
b = f(A(), "qwerty")

# ERROR
f([1, 2, 3], "h")

# ERROR
f([1, 2, 3], 1.3)

# ERROR
f([1.4, 2, 3], 1)

# ERROR
f(["a", "b", "c"], 1)
"""
