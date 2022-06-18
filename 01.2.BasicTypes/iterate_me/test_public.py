import copy
import dis
import inspect
import types
import typing as tp

from .iterate_me import get_squares, get_indices_from_one, get_max_element_index, \
    get_every_second_element, get_first_three_index, get_last_three_index, get_sum, get_min_max, \
    get_by_index


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


def test_get_squares() -> None:
    lst_a = [-2, 0, 5, 2, 3, 4, 3]
    lst_a_copy = copy.deepcopy(lst_a)
    assert get_squares(lst_a_copy) == [4, 0, 25, 4, 9, 16, 9]
    assert_use(get_squares, "opname", "BINARY_POWER")
    assert_not_changed_inputs(lst_a_copy, lst_a)


def test_get_squares_empty_list() -> None:
    lst_a: list[int] = []
    lst_a_copy = copy.deepcopy(lst_a)
    assert get_squares(lst_a_copy) == []
    assert_not_changed_inputs(lst_a_copy, lst_a)


def test_get_indices() -> None:
    lst_a = [-2, 0, 5, 2, 3, 4, 3]
    lst_a_copy = copy.deepcopy(lst_a)
    assert get_indices_from_one(lst_a_copy) == [1, 2, 3, 4, 5, 6, 7]
    assert_not_changed_inputs(lst_a_copy, lst_a)


def test_get_indices_empty_list() -> None:
    lst_a: list[int] = []
    lst_a_copy = copy.deepcopy(lst_a)
    assert get_indices_from_one(lst_a_copy) == []
    assert_not_changed_inputs(lst_a_copy, lst_a)


def test_get_max_element_index() -> None:
    lst_a = [-2, 0, 5, 2, 3, 4, 3]
    lst_a_copy = copy.deepcopy(lst_a)
    assert get_max_element_index(lst_a_copy) == 2
    assert_not_changed_inputs(lst_a_copy, lst_a)


def test_get_max_element_index_empty_list() -> None:
    lst_a: list[int] = []
    lst_a_copy = copy.deepcopy(lst_a)
    assert get_max_element_index(lst_a_copy) is None
    assert_not_changed_inputs(lst_a_copy, lst_a)


def test_get_every_second_element() -> None:
    lst_a = [-2, 0, 5, 2, 3, 4, 3]
    lst_a_copy = copy.deepcopy(lst_a)
    assert get_every_second_element(lst_a_copy) == [0, 2, 4]
    assert_not_changed_inputs(lst_a_copy, lst_a)


def test_get_every_second_element_empty_input() -> None:
    lst_a: list[int] = []
    lst_a_copy = copy.deepcopy(lst_a)
    assert get_every_second_element(lst_a_copy) == []
    assert_not_changed_inputs(lst_a_copy, lst_a)


def test_get_every_second_element_one_element() -> None:
    lst_a = [1]
    lst_a_copy = copy.deepcopy(lst_a)
    assert get_every_second_element(lst_a_copy) == []
    assert_not_changed_inputs(lst_a_copy, lst_a)


def test_get_first_three_index() -> None:
    lst_a = [-2, 0, 5, 2, 3, 4, 3]
    lst_a_copy = copy.deepcopy(lst_a)
    assert get_first_three_index(lst_a_copy) == 4
    assert_not_changed_inputs(lst_a_copy, lst_a)
    assert_exists_doc(get_first_three_index)


def test_get_first_three_index_empty_input() -> None:
    lst_a: list[int] = []
    lst_a_copy = copy.deepcopy(lst_a)
    assert get_first_three_index(lst_a_copy) is None
    assert_not_changed_inputs(lst_a_copy, lst_a)


def test_get_first_three_index_without_three() -> None:
    lst_a = [-2, 0, 5, 2]
    lst_a_copy = copy.deepcopy(lst_a)
    assert get_first_three_index(lst_a_copy) is None
    assert_not_changed_inputs(lst_a_copy, lst_a)


def test_get_last_three_index() -> None:
    lst_a = [-2, 0, 5, 2, 3, 4, 3]
    lst_a_copy = copy.deepcopy(lst_a)
    assert get_last_three_index(lst_a_copy) == 6
    assert_not_changed_inputs(lst_a_copy, lst_a)


def test_get_last_three_index_empty_input() -> None:
    lst_a: list[int] = []
    lst_a_copy = copy.deepcopy(lst_a)
    assert get_last_three_index(lst_a_copy) is None
    assert_not_changed_inputs(lst_a_copy, lst_a)


def test_get_last_three_index_without_three() -> None:
    lst_a = [-2, 0, 5, 2]
    lst_a_copy = copy.deepcopy(lst_a)
    assert get_last_three_index(lst_a_copy) is None
    assert_not_changed_inputs(lst_a_copy, lst_a)


def test_get_last_three_index_on_first_position() -> None:
    lst_a = [3, 0, 5, 2, 1, 4, 6]
    lst_a_copy = copy.deepcopy(lst_a)
    assert get_last_three_index(lst_a_copy) == 0
    assert_not_changed_inputs(lst_a_copy, lst_a)


def test_get_sum() -> None:
    lst_a = [3, 0, 5, 2, 1, 4, 6]
    lst_a_copy = copy.deepcopy(lst_a)
    assert get_sum(lst_a_copy) == 21
    assert_use(get_sum, "argval", "sum")
    assert_not_changed_inputs(lst_a_copy, lst_a)


def test_get_sum_with_empty_input() -> None:
    lst_a: list[int] = []
    lst_a_copy = copy.deepcopy(lst_a)
    assert get_sum(lst_a_copy) == 0
    assert_use(get_sum, "argval", "sum")
    assert_not_changed_inputs(lst_a_copy, lst_a)


def test_get_min_max() -> None:
    lst_a = [3, 0, 5, 2, 1, 4, 6]
    lst_a_copy = copy.deepcopy(lst_a)
    assert get_min_max(lst_a_copy, 0) == (0, 6)
    assert_use(get_min_max, "argval", "min")
    assert_use(get_min_max, "argval", "max")
    assert_not_changed_inputs(lst_a_copy, lst_a)


def test_get_min_max_with_empty_input_and_zero_default() -> None:
    lst_a: list[int] = []
    lst_a_copy = copy.deepcopy(lst_a)
    assert get_min_max(lst_a_copy, 0) == (0, 0)
    assert_use(get_min_max, "argval", "min")
    assert_use(get_min_max, "argval", "max")
    assert_not_changed_inputs(lst_a_copy, lst_a)


def test_get_min_max_with_empty_input_and_None_default() -> None:
    lst_a: list[int] = []
    lst_a_copy = copy.deepcopy(lst_a)
    assert get_min_max(lst_a_copy, None) == (None, None)
    assert_use(get_min_max, "argval", "min")
    assert_use(get_min_max, "argval", "max")
    assert_not_changed_inputs(lst_a_copy, lst_a)


def test_get_by_index() -> None:
    lst_a = [3, 0, 5, 2, 1, 4, 6]
    lst_a_copy = copy.deepcopy(lst_a)
    assert get_by_index(lst_a_copy, 5, 3) == 4
    assert_use_regexp(get_by_index, ":=")


def test_get_by_index_returns_None() -> None:
    lst_a = [3, 0, 5, 2, 1, 4, 6]
    lst_a_copy = copy.deepcopy(lst_a)
    assert get_by_index(lst_a_copy, 5, 4) is None
    assert_use_regexp(get_by_index, ":=")


def test_doc() -> None:
    assert_exists_doc(get_by_index)
    assert_exists_doc(get_min_max)
    assert_exists_doc(get_sum)
    assert_exists_doc(get_last_three_index)
    assert_exists_doc(get_first_three_index)
    assert_exists_doc(get_every_second_element)
    assert_exists_doc(get_max_element_index)
    assert_exists_doc(get_squares)
    assert_exists_doc(get_indices_from_one)
