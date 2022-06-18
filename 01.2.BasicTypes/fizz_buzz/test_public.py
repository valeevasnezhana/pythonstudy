import dataclasses
import dis
import inspect
import types
import typing as tp

import pytest

from .fizz_buzz import get_fizz_buzz


@dataclasses.dataclass
class Case:
    name: str
    n: int
    expected: tp.Mapping[int, tp.Union[int, str]]

    def __str__(self) -> str:
        return 'test_{}'.format(self.name)


TEST_CASES = [
    Case(name="test_zero_element", n=1, expected={0: 1}),
    Case(name="test_first_three_elements", n=3, expected={0: 1, 1: 2, 2: "Fizz"}),
    Case(name="check_fizz", n=100, expected={i - 1: "Fizz" for i in range(3, 101, 3) if i % 15 != 0}),
    Case(name="test_first_two_elements", n=2, expected={0: 1, 1: 2}),
    Case(name="check_buzz", n=100, expected={i - 1: "Buzz" for i in range(5, 101, 5) if i % 15 != 0}),
    Case(name="check_fizz_buzz", n=100, expected={i - 1: "FizzBuzz" for i in range(15, 101, 15)}),
    Case(name="check_digits", n=100, expected={i - 1: i for i in range(101) if i % 3 != 0 and i % 5 != 0})
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

@pytest.mark.parametrize("test_case", TEST_CASES, ids=str)
def test_get_fizz_buzz(test_case: Case) -> None:
    fizz_buzz_list = get_fizz_buzz(test_case.n)
    assert len(fizz_buzz_list) == test_case.n
    for key, value in test_case.expected.items():
        assert fizz_buzz_list[key] == value


def test_doc() -> None:
    assert_exists_doc(get_fizz_buzz)
