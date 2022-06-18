import dataclasses
import dis
import inspect
import types
import typing as tp
from os.path import normpath
import timeit

import pytest

from .normalize_path import normalize_path


@dataclasses.dataclass
class Case:
    path: str
    result: str


TEST_CASES = [
    Case(path='foo', result='foo'),
    Case(path='./bar', result='bar'),
    Case(path='', result='.'),
    Case(path='.', result='.'),
    Case(path='/', result='/'),
    Case(path='//', result='/'),
    Case(path='/..//..//././///././/..//../', result='/'),
    Case(path='..', result='..'),
    Case(path='../', result='..'),
    Case(path='../..', result='../..'),
    Case(path='a/b/c/d/../../../..', result='.'),
    Case(path='zog/..', result='.'),
    Case(path='./config/../etc', result='etc'),
    Case(path='foo/./bar', result='foo/bar'),
    Case(path='a/..///../b', result='../b'),
    Case(path='./../../../zog', result='../../../zog'),
    Case(path='/////documents/root/.././../etc', result='/etc'),
    Case(path='/../../../zog', result='/zog'),
    Case(path='/foo/bar//baz/asdf/quux/..', result='/foo/bar/baz/asdf'),
    Case(path='/h/../a/..' * 1_000, result='/'),
    Case(path='/a/b//c/d/..//../..//..' * 1_000, result='/'),
    Case(path='a/b//c/d/..//../..//../' * 1_000, result='.'),
]


@dataclasses.dataclass
class LoadCase:
    path: str
    num: int


LOAD_TEST_CASES = [
    LoadCase(path='/h/..' * 100000, num=1),
    #LoadCase(path='/h/../a/..' * 100000, num=1),
    #LoadCase(path='/a/b//..//../' * 10000, num=1),
    #LoadCase(path='/a/b//c/d/..//../..//..' * 10000, num=1),
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


def test_structural_staff() -> None:
    assert_exists_doc(normalize_path)
    assert_not_use(normalize_path, "argval", "normpath")
    assert_not_use(normalize_path, "argval", "Path")


@pytest.mark.parametrize('case', TEST_CASES)
def test_normalize(case: Case) -> None:
    answer = normalize_path(case.path)

    assert answer == case.result


@pytest.mark.parametrize('case', LOAD_TEST_CASES)
def test_speed(case: LoadCase) -> None:
    solution_time = timeit.timeit(lambda: normalize_path(case.path), number=case.num) / case.num
    normpath_time = timeit.timeit(lambda: normpath(case.path), number=case.num) / case.num

    # add 1.5 multiplayer just to help you to cope with testing system conditions
    assert solution_time < normpath_time * 1.5, 'You should do this in a more optimal way'
    print('\n', normpath_time / solution_time)
