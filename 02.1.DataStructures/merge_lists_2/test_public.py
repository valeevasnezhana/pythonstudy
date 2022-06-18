import copy
import dataclasses
import dis
import inspect
import itertools
import types
import typing as tp

import pytest

from .merge_lists import merge


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
    lists: tp.Sequence[tp.Sequence[int]]
    name: str

    def __str__(self) -> str:
        return 'merge_{}'.format(self.name)


def make_test_cases() -> tp.Generator[Case, None, None]:
    for i in range(10):
        lists: list[list[int]] = [[] for i in range(i + 1)]

        for j in range(2000):
            basket = j % (i + 1)
            lists[basket].append(j)
        yield Case(lists=lists, name="list_" + str(i))

    yield Case(lists=[], name="list_empty")
    yield Case(lists=[[], [], []], name="list_with_empty_lists")

    for i in range(10):
        lists = [[] for i in range(i + 1)]
        for j in range(2000):
            basket = j // (2000 // (i + 1) + 1)
            lists[basket].append(j)

        yield Case(lists=lists, name="list_by_blocks_" + str(i))

    for i in range(10):
        lists = [[] for i in range(i + 1)]
        for j in range(2000):
            basket = j // (2000 // (i + 1) + 1)
            lists[basket - (basket % 2)].append(j)

        yield Case(lists=lists, name="list_by_blocks_with_gaps" + str(i))

    yield Case(lists=[[1], [1]], name="lists_with_same_elements")


def test_function_structure() -> None:
    is_used_sorted = any(i.argval == 'sorted' for i in dis.get_instructions(merge))
    assert not is_used_sorted, "You should use iteration ONLY, not manually sorting"

    is_used_build_slice = any(i.opname == 'BUILD_SLICE' for i in dis.get_instructions(merge))
    assert not is_used_build_slice, "You should use iteration ONLY, not slicing"

    is_used_heapq = any(i.argval == 'heapq' for i in dis.get_instructions(merge))
    assert is_used_heapq, "You should use heapq"


@pytest.mark.parametrize('t', list(make_test_cases()), ids=str)
def test_merge(t: Case) -> None:

    given_lists = copy.deepcopy(t.lists)
    answer = merge(given_lists)

    assert t.lists == given_lists, "You shouldn't change inputs"
    assert answer == sorted(itertools.chain(*t.lists))


def test_doc() -> None:
    assert_exists_doc(merge)
