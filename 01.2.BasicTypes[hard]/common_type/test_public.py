import dis
import dataclasses
import inspect

import types
import typing as tp

import pytest

from .common_type import get_common_type


@dataclasses.dataclass
class Case:
    value1: tp.Any
    value2: tp.Any
    common_type: type

    def __str__(self) -> str:
        return 'find_common_type_of_{}_and_{}'.format(type(self.value1), type(self.value2))


TEST_CASES = [
    Case(value1="[1,2,3]", value2=[3, 4, 5], common_type=str),
    Case(value1="(1,2,3)", value2=(3, 4, 5), common_type=str),
    Case(value1="[1,2,3]", value2=range(3), common_type=str),
    Case(value1="range(3)", value2=range(3), common_type=str),
    Case(value1="[1,2,3]", value2=10, common_type=str),
    Case(value1="[1,2,3]", value2=1.3, common_type=str),
    Case(value1="1.3", value2=1.3, common_type=str),
    Case(value1="[1,2,3]", value2=1j, common_type=str),
    Case(value1="Hello", value2=False, common_type=str),
    Case(value1="True", value2=True, common_type=str),
    Case(value1="False", value2=False, common_type=str),

    Case(value1=[1, 2, 3], value2=[3, 4, 5], common_type=list),
    Case(value1=[1, 2, 3], value2=(1, 2, 3), common_type=list),
    Case(value1=[1, 2, 3], value2=range(3), common_type=list),
    Case(value1=[1, 2, 3], value2=2, common_type=str),
    Case(value1=[1, 2, 3], value2=1.5, common_type=str),
    Case(value1=[1, 2, 3], value2=2j, common_type=str),
    Case(value1=[1, 2, 3], value2=True, common_type=str),

    Case(value1=(1, 2, 3), value2=(3, 4, 5), common_type=tuple),
    Case(value1=(1, 2, 3), value2=range(3), common_type=tuple),
    Case(value1=(1, 2, 3), value2=2, common_type=str),
    Case(value1=(1, 2, 3), value2=1.5, common_type=str),
    Case(value1=(1, 2, 3), value2=2j, common_type=str),
    Case(value1=(1, 2, 3), value2=False, common_type=str),

    Case(value1=range(3), value2=range(3), common_type=tuple),
    Case(value1=range(3), value2=1, common_type=str),
    Case(value1=range(3), value2=1.0, common_type=str),
    Case(value1=range(3), value2=1j, common_type=str),
    Case(value1=range(3), value2=False, common_type=str),

    Case(value1=True, value2=False, common_type=bool),
    Case(value1=True, value2=2, common_type=int),
    Case(value1=True, value2=1.5, common_type=float),
    Case(value1=True, value2=2j, common_type=complex),

    Case(value1=1.0, value2=2, common_type=float),
    Case(value1=1.0, value2=1.5, common_type=float),
    Case(value1=1.0, value2=2j, common_type=complex),

    Case(value1=1, value2=2, common_type=int),
    Case(value1=1, value2=2j, common_type=complex),

    Case(value1=1j, value2=2j, common_type=complex),
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
def test_common_convertible_type(t: Case) -> None:

    common_type = get_common_type(type(t.value1), type(t.value2))
    common_type_reverse = get_common_type(type(t.value2), type(t.value1))

    # Check that symmetric
    assert common_type == common_type_reverse

    # Check that doesn't fall
    common_type(t.value1)
    common_type(t.value2)

    # Check that is expected
    assert common_type is t.common_type


def check_doc() -> None:
    assert_exists_doc(get_common_type)
