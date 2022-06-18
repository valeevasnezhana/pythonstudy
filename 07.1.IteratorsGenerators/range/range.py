from typing import Iterable, Sized, Iterator, Any


class RangeIterator(Iterator[int]):
    def __init__(self, range_: 'Range') -> None:
        self.range_ = range_
        self.position = range_.start

    def __next__(self) -> int:
        value = self.position
        self.position += self.range_.step
        if value < self.range_.stop and self.range_.step > 0:
            return value
        elif value > self.range_.stop and self.range_.step < 0:
            return value
        else:
            raise StopIteration


class Range(Sized, Iterable[int]):
    """The range-like type, which represents an immutable sequence of numbers"""

    def __init__(self, *args: int) -> None:
        """
        : param args: either it's a single `stop` argument
            or sequence of `start, stop[, step]` arguments.
        If the `step` argument is omitted, it defaults to 1.
        If the `start` argument is omitted, it defaults to 0.
        If `step` is zero, ValueError is raised.
        """
        if len(args) not in range(1, 4):
            raise ValueError(f'Number of arguments must be from 1 to 3, got{len(args)}')
        elif len(args) == 1:
            self.start, self.stop, self.step = 0, args[0], 1
        elif len(args) == 2:
            self.start, self.stop, self.step = args[0], args[1], 1
        elif len(args) == 3:
            self.start, self.stop, self.step = args[0], args[1], args[2]
        if self.step == 0:
            raise ValueError('Range() arg 3 (step) must not be zero')

    def __iter__(self) -> RangeIterator:
        return RangeIterator(self)

    def __repr__(self) -> str:
        if self.step != 1:
            return f'range({self.start}, {self.stop}, {self.step})'
        return f'range({self.start}, {self.stop})'

    def __str__(self) -> str:
        if self.step != 1:
            return f'range({self.start}, {self.stop}, {self.step})'
        return f'range({self.start}, {self.stop})'

    def __getitem__(self, key: int) -> int:
        pos = self.start + key * self.step
        if self.step > 0 and pos < self.stop:
            return pos
        elif self.step < 0 and pos > self.stop:
            return pos
        else:
            raise IndexError('Out of bounds')

    def __len__(self) -> int:
        if self.step < 0:
            start, stop, step = self.stop, self.start, -self.step
        else:
            start, stop, step = self.start, self.stop, self.step

        if stop < start:
            return 0

        return (stop - start - 1) // step + 1

    def __contains__(self, key: int) -> bool:
        if (key - self.start) % self.step == 0:
            if self.step > 0 and self.start <= key < self.stop:
                return True
            elif self.step < 0 and self.start >= key > self.stop:
                return True
        return False
