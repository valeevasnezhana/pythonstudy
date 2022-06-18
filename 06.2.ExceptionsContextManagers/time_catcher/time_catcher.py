import time
import typing as tp
from contextlib import AbstractContextManager


class TimeoutException(TimeoutError):
    pass


class SoftTimeoutException(TimeoutException):
    pass


class HardTimeoutException(TimeoutException):
    pass


class TimeCatcher(AbstractContextManager):
    def __init__(self, soft_timeout: tp.Optional[float] = None, hard_timeout: tp.Optional[float] = None):
        if soft_timeout is not None:
            assert soft_timeout > 0
        if hard_timeout is not None:
            assert hard_timeout > 0
        if (soft_timeout is not None) and (hard_timeout is not None):
            assert soft_timeout <= hard_timeout
        self.soft_timeout = soft_timeout
        self.hard_timeout = hard_timeout

    def __enter__(self):
        self.start_time = time.monotonic()
        self.ended = False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.monotonic()
        self.ended = True
        code_time = float(self.end_time - self.start_time)

        if self.hard_timeout and code_time > self.hard_timeout:
            raise HardTimeoutException()

        if self.soft_timeout and code_time > self.soft_timeout:
            raise SoftTimeoutException()

    def __float__(self):
        if self.ended:
            return float(self.end_time - self.start_time)
        else:
            return float(time.monotonic() - self.start_time)

    def __str__(self):
        return f"Time consumed: {float(self):.4f}"
