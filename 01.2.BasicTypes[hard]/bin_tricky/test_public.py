import copy
import dis
import dataclasses
import inspect
import itertools

import types
import typing as tp

import pytest


from .bin_tricky import find_median


@dataclasses.dataclass
class Case:
    nums1: list[int]
    nums2: list[int]

    def __str__(self) -> str:
        return 'find_median_in_{}_and_{}'.format(self.nums1, self.nums2)


BIG_VALUE = 10**5


def get_range_with_peak_on_position(range_size: int, position: int) -> list[int]:
    if position >= range_size or position < 0:
        raise ValueError("Position should be in [0, range_size)")

    return list(itertools.chain(range(position), [range_size + 1], range(range_size - position - 1, position, -1)))


TEST_CASES = [
    Case(nums1=[1], nums2=[2]),
    Case(nums1=[], nums2=[2]),
    Case(nums1=[1], nums2=[]),
    Case(nums1=[1, 2], nums2=[]),
    Case(nums1=[1, 2, 3], nums2=[]),
    Case(nums1=[1, 2, 3, 5], nums2=[]),
    Case(nums1=[1, 2, 3, 5, 7], nums2=[]),
    Case(nums1=[-1, -1, -1], nums2=[-1, -1, -1]),
    Case(nums1=[1, 2],  nums2=[1, 2]),
    Case(nums1=[1, 1], nums2=[1, 1]),
    Case(nums1=[1, 3], nums2=[2]),
    Case(nums1=[2], nums2=[1, 3, 4]),
    Case(nums1=[3], nums2=[1, 2, 4]),
    Case(nums1=[2, 6], nums2=[3, 4]),
    Case(nums1=[1, 2, 2, 2, 3, 4, 5], nums2=[1, 2, 6, 7, 8, 8, 9]),
    Case(nums1=[1, 2, 2, 2, 3, 4, 5], nums2=[1, 2, 6]),
    Case(nums1=[1, 2, 2, 2, 2, 2, 5], nums2=[1, 2, 6]),
    Case(nums1=[1, 2, 3, 4, 5], nums2=[1, 2, 3]),
    Case(nums1=[2, 2, 2, 2, 2, 2, 2, 2], nums2=[2, 2, 2]),
    Case(nums1=[2, 2, 2, 2, 2, 2, 2, 2], nums2=[2, 2, 2, 2]),
    Case(nums1=[1, 2, 3, 4], nums2=[3, 4, 5, 6]),
    Case(nums1=[1, 2, 3, 4], nums2=[1, 2, 3, 4]),
    Case(nums1=[1, 3, 5, 7], nums2=[2, 4, 6, 8]),
    Case(nums1=[1, 3, 5, 7], nums2=[-1, 2, 4, 6, 8]),
    Case(nums1=[1, 3, 5, 7], nums2=[-1, -1, -1]),
    Case(nums1=[-1, 5, 8, 17], nums2=[-7, 15, 20]),
    Case(nums1=[-1, 5, 8, 17], nums2=[21, 25, 38]),
    Case(nums1=[1, 3, 5, 7], nums2=[-5, -4, 0]),
    Case(nums1=[1, 2], nums2=[3]),
    Case(nums1=[1], nums2=[2, 3]),
    Case(nums1=[1, 2], nums2=[3, 4]),
    Case(nums1=[3, 4, 5], nums2=[1]),
    Case(nums1=[3, 4, 5, 6, 7, 8], nums2=[1, 2]),
    Case(nums1=[1, 1, 2, 5, 6], nums2=[1, 9, 10]),
    Case(nums1=list(range(0, 100, 2)), nums2=list(range(-100, 100, 5))),
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


def dummy_implementation(nums1: list[int], nums2: list[int]) -> float:
    combined_nums = sorted(nums1 + nums2)
    m = len(nums1)
    n = len(nums2)
    return (combined_nums[(m + n) // 2] + combined_nums[(m + n - 1) // 2]) / 2


def test_illegal_staff() -> None:
    is_used_sorted = any(i.argval == 'sorted' for i in get_instructions(find_median))
    assert not is_used_sorted, "You should use iteration ONLY, not manually sorting"

    is_used_in = any(getattr(instr, 'opname') == 'CONTAINS_OP' for instr in get_instructions(find_median))
    assert not is_used_in, "You, don't even dare to use `in`! It's plainly illegal, you got that?!"


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_find_value(t: Case) -> None:
    nums1_copy = copy.deepcopy(t.nums1)
    nums2_copy = copy.deepcopy(t.nums2)

    answer = find_median(nums1_copy, nums2_copy)

    assert t.nums1 == nums1_copy and t.nums2 == nums2_copy, "You shouldn't change inputs"
    assert type(answer) == float, "You shouldn't return different types from the same function"

    ground_truth = dummy_implementation(t.nums1, t.nums2)

    assert answer == ground_truth

    swapped_args_answer = find_median(nums2_copy, nums1_copy)
    assert swapped_args_answer == ground_truth, "You should get the same result if you swap the arguments"


def test_doc() -> None:
    assert_exists_doc(find_median)
