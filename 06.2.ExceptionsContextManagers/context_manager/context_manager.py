import traceback
from contextlib import contextmanager
from typing import Iterator, Optional, TextIO, Type
import sys


@contextmanager
def supresser(*types_: Type[BaseException]) -> Iterator[None]:
    try:
        yield
    except types_:
        pass


@contextmanager
def retyper(type_from: Type[BaseException], type_to: Type[BaseException]) -> Iterator[None]:
    try:
        yield
    except type_from:
        exception_type, value, traceback_ = sys.exc_info()
        if isinstance(value, type_from):
            raise type_to(*value.args).with_traceback(traceback_)
        raise


@contextmanager
def dumper(stream: Optional[TextIO] = None) -> Iterator[None]:
    if stream is None:
        stream = sys.stderr
    try:
        yield
    except Exception:
        exception_type, value, traceback_ = sys.exc_info()
        message = str(traceback.format_exception_only(exception_type, value))
        stream.write(message)
        raise

