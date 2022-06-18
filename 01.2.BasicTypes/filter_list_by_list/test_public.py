import copy
import dataclasses
import dis
import inspect
import types
import typing as tp

import pytest


from .filter_list_by_list import filter_list_by_list


@dataclasses.dataclass
class Case:
    lst_a: tp.Union[list[int], range]
    lst_b: tp.Union[list[int], range]
    result: list[int]


TEST_CASES = [
    Case(lst_a=[], lst_b=[], result=[]),
    Case(lst_a=[1, 2, 3], lst_b=[], result=[1, 2, 3]),
    Case(lst_a=[], lst_b=[1, 2, 3], result=[]),
    Case(lst_a=[], lst_b=[1], result=[]),
    Case(lst_a=[1], lst_b=[], result=[1]),
    Case(lst_a=[1], lst_b=[1], result=[]),
    Case(lst_a=[1, 2], lst_b=[3, 4], result=[1, 2]),
    Case(lst_a=[1, 3], lst_b=[2, 4], result=[1, 3]),
    Case(lst_a=[3, 4], lst_b=[1, 2], result=[3, 4]),
    Case(lst_a=[1, 3], lst_b=[2, 4], result=[1, 3]),
    Case(lst_a=[2, 3], lst_b=[1, 2], result=[3]),
    Case(lst_a=[1, 1], lst_b=[1, 1], result=[]),
    Case(lst_a=[1, 2], lst_b=[1, 1], result=[2]),
    Case(lst_a=[1, 2], lst_b=[1, 2], result=[]),
    Case(lst_a=[2, 3], lst_b=[1, 4], result=[2, 3]),
    Case(lst_a=[1, 4], lst_b=[4, 4], result=[1]),
    Case(lst_a=range(10**5), lst_b=[0] * 10**5, result=list(range(1, 10**5)))
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

@pytest.mark.parametrize('t', TEST_CASES)
def test_filter_list_by_list(t: Case) -> None:
    given_lst_a = copy.deepcopy(t.lst_a)
    given_lst_b = copy.deepcopy(t.lst_b)

    answer = filter_list_by_list(t.lst_a, t.lst_b)

    assert_not_changed_inputs(list(t.lst_a), list(given_lst_a))
    assert_not_changed_inputs(list(t.lst_b), list(given_lst_b))

    assert_not_use(filter_list_by_list, "argval", "set")
    assert answer == t.result


def test_doc() -> None:
    assert_exists_doc(filter_list_by_list)
