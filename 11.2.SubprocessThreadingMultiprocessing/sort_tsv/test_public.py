import dataclasses
import dis
import filecmp
import os
import types
from pathlib import Path
import timeit
import typing as tp

import pytest

from .sort_tsv import python_sort, util_sort


TESTDATA_DIR = Path(__file__).parent / 'testdata'


###################
# Structure asserts
###################

def extract_global(
        func: tp.Callable[..., tp.Any],
        name: str) -> tp.Optional[tp.Callable[..., tp.Any]]:
    func = tp.cast(types.FunctionType, func)
    some_global = func.__globals__.get(name, None)
    if some_global is not None \
            and isinstance(some_global, types.FunctionType) \
            and not isinstance(some_global, types.BuiltinFunctionType):
        return some_global
    return None


def get_instructions(
        func: tp.Union[tp.Callable[..., tp.Any], types.CodeType],
        visited_names: tp.Optional[tp.Set[str]] = None,
        base_func: tp.Optional[tp.Callable[..., tp.Any]] = None
) -> tp.Generator[dis.Instruction, None, None]:

    if base_func is None:
        assert not isinstance(func, types.CodeType)
        base_func = func

    visited_names = visited_names or set()

    for inst in dis.get_instructions(func):
        yield inst
        if inst.opname == "LOAD_GLOBAL" and inst.argval not in visited_names:
            visited_names.add(inst.argval)
            some_global = extract_global(base_func, inst.argval)
            if some_global is not None:
                yield from get_instructions(some_global, visited_names, base_func)

    func_code = func if isinstance(func, types.CodeType) else func.__code__
    for const in func_code.co_consts:
        if isinstance(const, types.CodeType):
            yield from get_instructions(const, visited_names, base_func)


def assert_use(func: tp.Callable[..., tp.Any], param: str, value: str) -> None:
    is_used = any(getattr(instr, param) == value for instr in get_instructions(func))
    assert is_used, f"You should use {value}"


def test_used_subprocess() -> None:
    assert_use(util_sort, "argval", "subprocess")


@dataclasses.dataclass
class Case:
    name: str
    file_out: str
    func: tp.Any


TEST_CASES = [
    Case(name='python', file_out='/tmp/data_sorted_python.tsv', func=python_sort),
    Case(name='util', file_out='/tmp/data_sorted_util.tsv', func=util_sort),
]


@pytest.mark.parametrize('case', TEST_CASES)
def test_sort(case: Case) -> None:
    file_in = TESTDATA_DIR / 'data.tsv'
    file_out = case.file_out

    # Чтобы посмотреть затраченное время для каждой функции,
    # можно запустить pytest с опцией '-s'
    repeat_count = 3
    t = timeit.timeit(lambda: case.func(file_in, file_out), number=repeat_count) / repeat_count
    print(f'\n{case.name} sorting took {t:.3f}s')

    file_ground_truth = TESTDATA_DIR / 'data_sorted_ground_truth.tsv'
    assert filecmp.cmp(file_ground_truth, file_out)

    os.remove(file_out)
