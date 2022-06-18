import copy
import dataclasses
import dis
import inspect
import types
import typing as tp

import pytest

from .reverse_dict import revert


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
    dct: tp.Mapping[str, str]
    result: tp.Mapping[str, list[str]]

    def __str__(self) -> str:
        return 'revert_{}'.format(self.dct)


TEST_CASES = [
    Case(dct={}, result={}),
    Case(dct={"a": "1"}, result={"1": ["a"]}),
    Case(dct={"ab": "12"}, result={"12": ["ab"]}),
    Case(dct={"": "1", "a": ""}, result={"1": [""], "": ["a"]}),
    Case(dct={"a": "1", "b": "2"}, result={"1": ["a"], "2": ["b"]}),
    Case(dct={"a": "1", "b": "2", "c": "1"}, result={"1": ["a", "c"], "2": ["b"]}),
    Case(dct={"a": "1", "b": "2", "c": "1", "d": "1"}, result={"1": ["a", "c", "d"], "2": ["b"]}),
    Case(dct={"a": "1", "b": "2", "c": "1", "d": "1", "e": "2"}, result={"1": ["a", "c", "d"], "2": ["b", "e"]}),
    Case(
        dct={"a": "1", "b": "2", "c": "1", "d": "1", "e": "2", "g": "3"},
        result={"1": ["a", "c", "d"], "2": ["b", "e"], "3": ["g"]}
    ),
]


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_reverse_dict(t: Case) -> None:
    given_dct = copy.deepcopy(t.dct)

    answer = revert(given_dct)

    assert t.dct == given_dct, "You shouldn't change input dict"

    for k, v in answer.items():
        v.sort()

    assert answer == t.result
    assert isinstance(answer, dict)


def test_doc() -> None:
    assert_exists_doc(revert)
