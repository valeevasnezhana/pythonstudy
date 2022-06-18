import copy
import dis
import dataclasses
import inspect

import types
import typing as tp

import pytest


from .common_type_2 import convert_to_common_type


@dataclasses.dataclass
class Case:
    values: list[tp.Any]
    converted_values: list[tp.Any]
    common_type: type

    def __str__(self) -> str:
        return "convert_{}".format(self.values)


TEST_CASES = [
    Case(
        values=["ozon.ru", ["amazon.com", "vk.com"], ("py.manytask.ru", "yandex.ru"), None, ""],
        converted_values=[["ozon.ru"], ["amazon.com", "vk.com"], ["py.manytask.ru", "yandex.ru"], [], []],
        common_type=list
    ),
    Case(
        values=["ozon.ru", "amazon.com", "py.manytask.ru", None, ""],
        converted_values=["ozon.ru", "amazon.com", "py.manytask.ru", "", ""],
        common_type=str
    ),
    Case(
        values=[122334, [121223, 9389384], (123223, 4384934), None, ""],
        converted_values=[[122334], [121223, 9389384], [123223, 4384934], [], []],
        common_type=list
    ),
    Case(
        values=[122334, (121223, 9389384), (123223, 4384934), None, ""],
        converted_values=[[122334], [121223, 9389384], [123223, 4384934], [], []],
        common_type=list
    ),
    Case(
        values=[True, (True, False), None, ""],
        converted_values=[[True], [True, False], [], []],
        common_type=list
    ),
    Case(
        values=[122334, "", 4384934, None, ""],
        converted_values=[122334, 0, 4384934, 0, 0],
        common_type=int
    ),
    Case(
        values=[15, 10.75, 2, None, ""],
        converted_values=[15.0, 10.75, 2.0, 0.0, 0.0],
        common_type=float
    ),
    Case(
        values=[15, 2, None, ""],
        converted_values=[15, 2, 0, 0],
        common_type=int
    ),
    Case(
        values=[2.0, None, ""],
        converted_values=[2.0, 0.0, 0.0],
        common_type=float
    ),
    Case(
        values=[False, 0, True, "", None],
        converted_values=[False, False, True, False, False],
        common_type=bool
    ),
    Case(
        values=[1, 1, 1, "", True],
        converted_values=[True, True, True, False, True],
        common_type=bool
    ),
    Case(
        values=[None, "", None, None],
        converted_values=["", "", "", ""],
        common_type=str
    ),
    Case(
        values=[None],
        converted_values=[""],
        common_type=str
    ),
    Case(
        values=[None, None, None, None],
        converted_values=["", "", "", ""],
        common_type=str
    ),
    Case(
        values=[False, False, False],
        converted_values=[False, False, False],
        common_type=bool
    ),
    Case(
        values=[0, None, ""],
        converted_values=[0, 0, 0],
        common_type=int
    )
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
def test_convert_to_common_type(t: Case) -> None:
    values_copy = copy.deepcopy(t.values)
    converted_values = convert_to_common_type(values_copy)

    assert t.values == values_copy, "You shouldn't change inputs"
    assert converted_values == t.converted_values
    for value in converted_values:
        assert type(value) == t.common_type
