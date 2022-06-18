import copy
import dataclasses
import dis
import inspect
import types
import typing as tp

import pytest


from .bin_basic import find_value


@dataclasses.dataclass
class Case:
    nums: tp.Union[list[int], range]
    value: int
    result: bool
    name: tp.Optional[str] = None

    def __str__(self) -> str:
        if self.name is not None:
            return self.name
        return 'find_{}_in_{}'.format(self.value, self.nums)


BIG_VALUE = 10**15

TEST_CASES = [
    Case(nums=[], value=2, result=False),
    Case(nums=[1], value=2, result=False),
    Case(nums=[1, 3, 5], value=0, result=False),
    Case(nums=[1, 3, 5], value=2, result=False),
    Case(nums=[1, 3, 5], value=4, result=False),
    Case(nums=[1, 3, 5], value=6, result=False),
    Case(nums=[1, 3, 5], value=1, result=True),
    Case(nums=[1, 3, 5], value=3, result=True),
    Case(nums=[1, 3, 5], value=5, result=True),
    Case(nums=[3], value=3, result=True),
    Case(nums=[1, 3], value=1, result=True),
    Case(nums=[1, 3], value=3, result=True),
    Case(nums=[1, 3, 5, 7], value=0, result=False),
    Case(nums=[1, 3, 5, 7], value=2, result=False),
    Case(nums=[1, 3, 5, 7], value=4, result=False),
    Case(nums=[1, 3, 5, 7], value=6, result=False),
    Case(nums=[1, 3, 5, 7], value=8, result=False),
    Case(nums=[1, 3, 5, 7], value=1, result=True),
    Case(nums=[1, 3, 5, 7], value=3, result=True),
    Case(nums=[1, 3, 5, 7], value=5, result=True),
    Case(nums=[1, 3, 5, 7], value=7, result=True),
    Case(nums=[1, 3, 5, 7, 9], value=0, result=False),
    Case(nums=[1, 3, 5, 7, 9], value=2, result=False),
    Case(nums=[1, 3, 5, 7, 9], value=4, result=False),
    Case(nums=[1, 3, 5, 7, 9], value=6, result=False),
    Case(nums=[1, 3, 5, 7, 9], value=8, result=False),
    Case(nums=[1, 3, 5, 7, 9], value=10, result=False),
    Case(nums=[1, 3, 5, 7, 9], value=1, result=True),
    Case(nums=[1, 3, 5, 7, 9], value=3, result=True),
    Case(nums=[1, 3, 5, 7, 9], value=5, result=True),
    Case(nums=[1, 3, 5, 7, 9], value=7, result=True),
    Case(nums=[1, 3, 5, 7, 9], value=9, result=True),
    Case(nums=[1, 5, 5, 5, 9], value=1, result=True),
    Case(nums=[1, 5, 5, 5, 9], value=5, result=True),
    Case(nums=[1, 5, 5, 5, 9], value=9, result=True),
    Case(nums=[1, 5, 5, 5, 9], value=7, result=False),
    Case(nums=range(0, BIG_VALUE, 2), value=BIG_VALUE - 2, result=True, name="max_in_big_range"),
    Case(nums=range(0, BIG_VALUE, 2), value=0, result=True, name="min_in_big_range"),
    Case(nums=range(0, BIG_VALUE, 2), value=BIG_VALUE, result=False, name="greater_than_max_in_big_range"),
    Case(nums=range(0, BIG_VALUE, 2), value=-1, result=False, name="less_than_min_in_big_range"),
    Case(nums=range(0, BIG_VALUE, 2), value=BIG_VALUE // 2, result=True, name="middle_in_big_range"),
    Case(nums=range(0, BIG_VALUE, 2), value=BIG_VALUE // 2 + 1, result=False, name="middle_not_exists_in_big_range"),
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


def test_banned_functions() -> None:
    assert_not_use(find_value, "argval", "bisect_left")
    assert_not_use(find_value, "argval", "bisect_right")
    assert_not_use(find_value, "argval", "bisect")


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_find_value(t: Case) -> None:
    nums_copy = copy.deepcopy(t.nums)
    answer = find_value(nums_copy, t.value)
    assert t.nums == nums_copy, "You shouldn't change inputs"
    assert answer == t.result


def test_doc() -> None:
    assert_exists_doc(find_value)
