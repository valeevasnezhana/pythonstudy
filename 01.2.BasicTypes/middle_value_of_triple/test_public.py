import dataclasses
import dis
import inspect

import types
import typing as tp

import pytest

from .middle_value_of_triple import get_middle_value


@dataclasses.dataclass
class Case:
    a: int
    b: int
    c: int
    result: int

    def __str__(self) -> str:
        return 'median_of_{}_{}_{}'.format(self.a, self.b, self.c)


TEST_CASES = [
    Case(a=1, b=2, c=3, result=2),
    Case(a=3, b=2, c=1, result=2),
    Case(a=2, b=3, c=1, result=2),
    Case(a=2, b=1, c=3, result=2),
    Case(a=3, b=1, c=2, result=2),
    Case(a=1, b=3, c=2, result=2),
    Case(a=-100, b=-10, c=100, result=-10),
    Case(a=100, b=-10, c=-100, result=-10),
    Case(a=-10, b=-10, c=-5, result=-10),
    Case(a=-10, b=-10, c=-10, result=-10),
    Case(a=-100, b=10, c=100, result=10),
    Case(a=0, b=0, c=0, result=0),
    Case(a=10**12, b=-10**12, c=10**10, result=10**10)
]


###################
# Structure asserts
###################


def get_instructions(
        func: tp.Union[tp.Callable[..., tp.Any], types.CodeType],
        visited_names: tp.Optional[set[str]] = None
) -> tp.Generator[dis.Instruction, None, None]:

    yield from dis.get_instructions(func)
    visited_names = visited_names or set()
    if not isinstance(func, types.CodeType):
        func = tp.cast(types.FunctionType, func)
        for name in func.__code__.co_names:
            some_global = func.__globals__.get(name, None)
            if some_global is not None \
                    and isinstance(some_global, types.FunctionType) \
                    and not isinstance(some_global, types.BuiltinFunctionType) \
                    and name not in visited_names:
                visited_names.add(name)
                yield from get_instructions(some_global, visited_names)
        func_code = func.__code__
    else:
        func_code = func

    for const in func_code.co_consts:
        if isinstance(const, types.CodeType):
            yield from get_instructions(const, visited_names)


def assert_exists_doc(func: tp.Callable[..., tp.Any]) -> None:
    assert inspect.getdoc(func) is not None, "You shouldn't drop doc"


def assert_not_changed_inputs(input_value: tp.Any, input_value_after_func_run: tp.Any) -> None:
    assert input_value == input_value_after_func_run, "You shouldn't change inputs"


def assert_not_use(func: tp.Callable[..., tp.Any], param: str, value: str) -> None:
    is_used = any(getattr(instr, param) == value for instr in get_instructions(func))
    assert not is_used, f"You shouldn't use {value}"


def assert_use(func: tp.Callable[..., tp.Any], param: str, value: str) -> None:
    is_used = any(getattr(instr, param) == value for instr in get_instructions(func))
    assert is_used, f"You should use {value}"


###################
# Tests
###################


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_get_middle_value(t: Case) -> None:
    answer = get_middle_value(t.a, t.b, t.c)
    assert answer == t.result


def test_doc() -> None:
    assert_exists_doc(get_middle_value)
