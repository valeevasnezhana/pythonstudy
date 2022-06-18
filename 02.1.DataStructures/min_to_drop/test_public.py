import copy
import dataclasses
import dis
import inspect
import types
import typing as tp

import pytest

from .min_to_drop import get_min_to_drop


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


def assert_use_regexp(func: tp.Callable[..., tp.Any], substr: str) -> None:
    assert substr in inspect.getsource(func), f"You should use {substr}"


###################
# Tests
###################


@dataclasses.dataclass
class Case:
    a: tp.Sequence[tp.Any]
    result: int

    def __str__(self) -> str:
        return 'min_to_drop_{}'.format(self.a)


TEST_CASES = [
    Case(a=[], result=0),
    Case(a=[1, 2, 3, 1], result=2),
    Case(a=[1, 2, 1], result=1),
    Case(a=[1, 1], result=0),
    Case(a=[1], result=0),
    Case(a=[2*30, 2*30], result=0),
    Case(a=["a"], result=0),
    Case(a=["a", "a"], result=0),
    Case(a=["a", "a", "b", "c"], result=2),
    Case(a=[1, 2, 3, 4], result=3),
    Case(a=[2, 3, 4, 1], result=3),
    Case(a=[1, 2, 3, 4, 5, 6, 1], result=5),
    Case(a=[1, 1, 1, 1, 2, 2, 1], result=2),
    Case(a=[1, 1, 1, 2, 2, 2, 2], result=3),
    Case(a=[2, 2, 2, 2, 1, 1, 1], result=3),
    Case(a=[1, 1, 2, 2, 3, 3], result=4),
    Case(a=[1, 1, 1, 2, 3, 3, 1], result=3),
    Case(a=[-1, 1, 1, -1, 3, 3, -1], result=4),
    Case(a=[-1, 1] * 1024, result=1024),
    Case(a=list(range(1024)), result=1024-1),
]


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_min_to_drop(t: Case) -> None:
    given_a = copy.deepcopy(t.a)

    answer = get_min_to_drop(given_a)

    assert t.a == given_a, "You shouldn't change inputs"
    assert answer == t.result


def test_doc() -> None:
    assert_exists_doc(get_min_to_drop)
