import dataclasses
import dis
import io
from typing import Any, Callable
import sys

import pytest

from . import byteme


@dataclasses.dataclass
class Case:
    func: Callable[..., Any]
    expected_dis_out: str

    def __str__(self) -> str:
        return self.func.__name__


TEST_CASES = [
    Case(
        func=byteme.f0,
        expected_dis_out='''\
   0 LOAD_CONST               0 (None)
   2 RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f1,
        expected_dis_out='''\
   0 LOAD_CONST               1 (0)
   2 STORE_FAST               0 (a)
   4 LOAD_FAST                0 (a)
   6 RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f2,
        expected_dis_out='''\
   0 LOAD_CONST               1 (0)
   2 STORE_FAST               0 (a)
   4 LOAD_GLOBAL              0 (print)
   6 LOAD_FAST                0 (a)
   8 CALL_FUNCTION            1
  10 POP_TOP
  12 LOAD_CONST               0 (None)
  14 RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f3,
        expected_dis_out='''\
   0 LOAD_CONST               1 (0)
   2 STORE_FAST               0 (a)
   4 LOAD_FAST                0 (a)
   6 LOAD_CONST               2 (1)
   8 INPLACE_ADD
  10 STORE_FAST               0 (a)
  12 LOAD_GLOBAL              0 (print)
  14 LOAD_FAST                0 (a)
  16 CALL_FUNCTION            1
  18 POP_TOP
  20 LOAD_CONST               0 (None)
  22 RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f4,
        expected_dis_out='''\
   0 LOAD_GLOBAL              0 (range)
   2 LOAD_CONST               1 (10)
   4 CALL_FUNCTION            1
   6 RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f5,
        expected_dis_out='''\
   0 LOAD_GLOBAL              0 (range)
   2 LOAD_CONST               1 (10)
   4 CALL_FUNCTION            1
   6 GET_ITER
   8 FOR_ITER                12 (to 22)
  10 STORE_FAST               0 (i)
  12 LOAD_GLOBAL              1 (print)
  14 LOAD_FAST                0 (i)
  16 CALL_FUNCTION            1
  18 POP_TOP
  20 JUMP_ABSOLUTE            8
  22 LOAD_CONST               0 (None)
  24 RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f6,
        expected_dis_out='''\
   0 LOAD_CONST               1 (0)
   2 STORE_FAST               0 (a)
   4 LOAD_GLOBAL              0 (range)
   6 LOAD_CONST               2 (10)
   8 CALL_FUNCTION            1
  10 GET_ITER
  12 FOR_ITER                12 (to 26)
  14 STORE_FAST               1 (i)
  16 LOAD_FAST                0 (a)
  18 LOAD_CONST               3 (1)
  20 INPLACE_ADD
  22 STORE_FAST               0 (a)
  24 JUMP_ABSOLUTE           12
  26 LOAD_GLOBAL              1 (print)
  28 LOAD_FAST                0 (a)
  30 CALL_FUNCTION            1
  32 POP_TOP
  34 LOAD_CONST               0 (None)
  36 RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f8,
        expected_dis_out='''\
   0 LOAD_CONST               1 ((1, 2))
   2 UNPACK_SEQUENCE          2
   4 STORE_FAST               0 (x)
   6 STORE_FAST               1 (y)
   8 LOAD_CONST               0 (None)
  10 RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f9,
        expected_dis_out='''\
   0 LOAD_CONST               1 (1)
   2 LOAD_CONST               1 (1)
   4 COMPARE_OP               2 (==)
   6 POP_JUMP_IF_FALSE       12
   8 LOAD_CONST               1 (1)
  10 RETURN_VALUE
  12 LOAD_CONST               2 (2)
  14 RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f10,
        expected_dis_out='''\
   0 LOAD_GLOBAL              0 (range)
   2 LOAD_CONST               1 (10)
   4 CALL_FUNCTION            1
   6 GET_ITER
   8 FOR_ITER                16 (to 26)
  10 STORE_FAST               0 (i)
  12 LOAD_FAST                0 (i)
  14 LOAD_CONST               2 (3)
  16 COMPARE_OP               2 (==)
  18 POP_JUMP_IF_FALSE        8
  20 POP_TOP
  22 JUMP_ABSOLUTE           26
  24 JUMP_ABSOLUTE            8
  26 LOAD_CONST               0 (None)
  28 RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f11,
        expected_dis_out='''\
   0 BUILD_LIST               0
   2 LOAD_CONST               1 ((1, 2, 3))
   4 LIST_EXTEND              1
   6 STORE_FAST               0 (list_)
   8 LOAD_CONST               2 (1)
  10 LOAD_CONST               3 (2)
  12 LOAD_CONST               4 (('a', 'b'))
  14 BUILD_CONST_KEY_MAP      2
  16 STORE_FAST               1 (dict_)
  18 LOAD_FAST                0 (list_)
  20 LOAD_FAST                1 (dict_)
  22 BUILD_TUPLE              2
  24 RETURN_VALUE
'''
    ),
    Case(
        func=byteme.f12,
        expected_dis_out='''\
   0 LOAD_CONST               1 (1)
   2 STORE_FAST               0 (a)
   4 LOAD_CONST               2 (2)
   6 STORE_FAST               1 (b)
   8 LOAD_CONST               3 (3)
  10 STORE_FAST               2 (c)
  12 LOAD_CONST               4 (4)
  14 STORE_FAST               3 (d)
  16 LOAD_CONST               5 (5)
  18 STORE_FAST               4 (e)
  20 LOAD_FAST                0 (a)
  22 LOAD_FAST                1 (b)
  24 LOAD_FAST                2 (c)
  26 BINARY_MULTIPLY
  28 LOAD_FAST                3 (d)
  30 LOAD_FAST                4 (e)
  32 BINARY_POWER
  34 BINARY_TRUE_DIVIDE
  36 BINARY_ADD
  38 RETURN_VALUE
'''
    ),
]


def test_version() -> None:
    """
    To do this task you need python=3.9.7
    """
    assert '3.9.7' == sys.version.split(' ', maxsplit=1)[0]


def strip_dis_out(dis_out: str) -> str:
    """Strip first 11 chars from dis_out and remove empty lines"""
    return '\n'.join(line[11:] for line in dis_out.split('\n') if line) + '\n'


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_byteme(t: Case) -> None:
    out = io.StringIO()
    dis.dis(t.func, file=out)
    actual_dis_out = out.getvalue()
    print(actual_dis_out)
    assert strip_dis_out(actual_dis_out) == t.expected_dis_out
