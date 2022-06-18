import copy
import dis
import dataclasses
import inspect

import types
import typing as tp

import pytest


from .reverse_list import reverse_iterative, reverse_inplace_iterative, reverse_inplace, reverse_reversed, reverse_slice


@dataclasses.dataclass
class Case:
    lst: list[int]
    result: list[int]

    def __str__(self) -> str:
        return 'reverse_{}'.format(self.lst)


TEST_CASES = [
    Case(lst=[], result=[]),
    Case(lst=[1, 2, 3], result=[3, 2, 1]),
    Case(lst=[1, 2, 1], result=[1, 2, 1]),
    Case(lst=[1, 2, 3, 4], result=[4, 3, 2, 1]),
    Case(lst=[1], result=[1]),
    Case(lst=[2, 2, 2, 2], result=[2, 2, 2, 2]),
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
def test_reverse_iterative(t: Case) -> None:
    given_lst = copy.deepcopy(t.lst)

    answer = reverse_iterative(given_lst)

    assert_not_changed_inputs(t.lst, given_lst)
    assert_not_use(reverse_iterative, "argval", "reversed")
    assert_not_use(reverse_iterative, "opname", "BUILD_SLICE")

    assert answer == t.result


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_reverse_inplace_iterative(t: Case) -> None:
    given_lst = copy.deepcopy(t.lst)

    reverse_inplace_iterative(given_lst)

    assert_not_use(reverse_inplace_iterative, "argval", "reverse")
    assert_not_use(reverse_inplace_iterative, "opname", "BUILD_SLICE")

    assert given_lst == t.result


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_reverse_inplace(t: Case) -> None:
    given_lst = copy.deepcopy(t.lst)

    reverse_inplace(given_lst)

    assert_use(reverse_inplace, "argval", "reverse")

    assert given_lst == t.result


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_reverse_reversed(t: Case) -> None:
    given_lst = copy.deepcopy(t.lst)

    answer = reverse_reversed(given_lst)

    assert_not_changed_inputs(t.lst, given_lst)
    assert_use(reverse_reversed, "argval", "reversed")
    assert_not_use(reverse_reversed, "opname", "BUILD_SLICE")

    assert answer == t.result


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_reverse_slice(t: Case) -> None:
    given_lst = copy.deepcopy(t.lst)

    answer = reverse_slice(given_lst)

    assert_not_changed_inputs(t.lst, given_lst)
    assert_not_use(reverse_slice, "argval", "reversed")
    assert_use(reverse_slice, "opname", "BUILD_SLICE")

    assert answer == t.result


def test_doc() -> None:
    assert_exists_doc(reverse_inplace)
    assert_exists_doc(reverse_inplace_iterative)
    assert_exists_doc(reverse_iterative)
    assert_exists_doc(reverse_reversed)
    assert_exists_doc(reverse_slice)
