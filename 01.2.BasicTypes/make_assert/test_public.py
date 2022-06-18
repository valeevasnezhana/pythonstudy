import dis
import inspect
import types
import typing as tp

import pytest

from .make_assert import test_check_ctr, ctr_correct_implementation


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


def test_clicks_equals_shows_not_assert() -> None:
    test_check_ctr(2, 2, 1.0)


def test_zero_shows_not_assert() -> None:
    test_check_ctr(100, 0, 0.0)


def test_zero_clicks_not_assert() -> None:
    test_check_ctr(0, 100, 0.0)


def test_fractional_ctr_assert() -> None:
    with pytest.raises(AssertionError, match="Wrong ctr calculation"):
        test_check_ctr(1, 2, 0.5)


def test_ctr_greater_then_one_assert() -> None:
    with pytest.raises(AssertionError, match="Wrong ctr calculation"):
        test_check_ctr(10, 5, 1.0)


def test_ctr2_clicks_equals_shows() -> None:
    result = ctr_correct_implementation(2, 2)
    assert type(result) == float
    assert result == 1.0


def test_ctr2_zero_shows() -> None:
    result = ctr_correct_implementation(0, 0)
    assert type(result) == float
    assert result == 0.0


def test_ctr2_fractional() -> None:
    result = ctr_correct_implementation(1, 2)
    assert type(result) == float
    assert result == 0.5


def test_ctr2_clicks_greater_than_shows() -> None:
    with pytest.raises(AssertionError, match="Clicks greater than shows"):
        ctr_correct_implementation(2, 1)


def test_doc() -> None:
    assert_exists_doc(test_check_ctr)
    assert_exists_doc(ctr_correct_implementation)
