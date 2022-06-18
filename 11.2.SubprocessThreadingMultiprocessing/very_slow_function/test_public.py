import dis
import timeit
import types
import typing as tp

from .very_slow_function import calc_squares_simple
from .very_slow_function import calc_squares_multithreading
from .very_slow_function import calc_squares_multiprocessing


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


def test_used_very_slow_function() -> None:
    assert_use(calc_squares_simple, "argval", "very_slow_function")
    assert_use(calc_squares_multithreading, "argval", "very_slow_function")
    assert_use(calc_squares_multiprocessing, "argval", "very_slow_function")


def test_used_multithreading() -> None:
    assert_use(calc_squares_multithreading, "argval", "Thread")


def test_used_multiprocessing() -> None:
    assert_use(calc_squares_multiprocessing, "argval", "Pool")


def test_correctness() -> None:
    expected_result = [0, 1, 4, 9]
    assert expected_result == calc_squares_simple(4)
    assert expected_result == calc_squares_multithreading(4)
    assert expected_result == calc_squares_multiprocessing(4)


def test_speed() -> None:
    time_simple = timeit.timeit(lambda: calc_squares_simple(50), number=1)
    time_multithreading = timeit.timeit(lambda: calc_squares_multithreading(50), number=1)
    time_multiprocessing = timeit.timeit(lambda: calc_squares_multiprocessing(50), number=1)

    assert time_simple > time_multiprocessing

    print('\nelapsed time for:')
    print(f'\t1. calc_squares_simple: {time_simple:.2f}s')
    print(f'\t2. calc_squares_multithreading: {time_multithreading:.2f}s')
    print(f'\t3. calc_squares_multiprocessing: {time_multiprocessing:.2f}s')
