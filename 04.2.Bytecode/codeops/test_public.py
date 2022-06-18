import dataclasses
import types
from textwrap import dedent

import pytest

from .codeops import count_operations


@dataclasses.dataclass
class Case:
    source_code: str
    op_counts: dict[str, int]

    @property
    def code(self) -> types.CodeType:
        dedent_source_code = dedent(self.source_code)
        return compile(dedent_source_code, '<string>', 'exec')


TEST_CASES = [
    Case(
        source_code="""
            a = 1
            b = 2
            a += b
            print(a)
        """,
        op_counts={
            'CALL_FUNCTION': 1,
            'INPLACE_ADD': 1,
            'LOAD_CONST': 3,
            'LOAD_NAME': 4,
            'POP_TOP': 1,
            'RETURN_VALUE': 1,
            'STORE_NAME': 3,
        }
    ),
    Case(
        source_code="""
            def f():
                a = 1
            f()
        """,
        op_counts={
            'CALL_FUNCTION': 1,
            'LOAD_CONST': 5,
            'LOAD_NAME': 1,
            'MAKE_FUNCTION': 1,
            'POP_TOP': 1,
            'RETURN_VALUE': 2,
            'STORE_FAST': 1,
            'STORE_NAME': 1,
        }
    ),
    Case(
        source_code="""
            def f():
                a = 1
            print(f())
        """,
        op_counts={
            'CALL_FUNCTION': 2,
            'LOAD_CONST': 5,
            'LOAD_NAME': 2,
            'MAKE_FUNCTION': 1,
            'POP_TOP': 1,
            'RETURN_VALUE': 2,
            'STORE_FAST': 1,
            'STORE_NAME': 1,
        }
    ),
    Case(
        source_code="""
            def foo(x):
                return x**2
            def bar(x):
                return x*2
            print(bar(foo(10)))
        """,
        op_counts={
            'BINARY_MULTIPLY': 1,
            'BINARY_POWER': 1,
            'CALL_FUNCTION': 3,
            'LOAD_CONST': 8,
            'LOAD_FAST': 2,
            'LOAD_NAME': 3,
            'MAKE_FUNCTION': 2,
            'POP_TOP': 1,
            'RETURN_VALUE': 3,
            'STORE_NAME': 2,
        }
    ),
    Case(
        source_code="""
            def foo():
                def bar():
                    def baz():
                        return 1
                    return baz
                return bar
        """,
        op_counts={
            'LOAD_CONST': 8,
            'LOAD_FAST': 2,
            'MAKE_FUNCTION': 3,
            'RETURN_VALUE': 4,
            'STORE_FAST': 2,
            'STORE_NAME': 1,
        }
    ),
]


@pytest.mark.parametrize('t', TEST_CASES)
def test_count_operations(t: Case) -> None:
    assert count_operations(t.code) == t.op_counts
