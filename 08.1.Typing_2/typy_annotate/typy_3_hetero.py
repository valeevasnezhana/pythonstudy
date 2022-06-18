import typing as tp

T1 = tp.TypeVar("T1", bound=str)
T2 = tp.TypeVar("T2", str, tp.List[str])


def f(a: tp.Tuple[tp.Sized, T1, T2]) -> T1:
    return a[1]


TEST_SAMPLES = """
# SUCCESS
f(("a", "b", "c"))

# SUCCESS
f(("a", "b", ["c", "d", "e"]))

# ERROR
f(("a", "b", "c", "d"))

# SUCCESS
class A(str):
    pass

a: A
a = f(("a", A(), A()))

# SUCCESS
f((["a", "b"], "c", "d"))

# SUCCESS
class A:
    def __len__(self) -> int:
        return 1

f((A(), "c", "d"))

# ERROR
class A:
    def __len__(self) -> int:
        return 1

f((A(), "c", {"d", "e"}))
"""
