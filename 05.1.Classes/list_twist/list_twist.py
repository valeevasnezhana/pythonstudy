from collections import UserList
import typing as tp


# https://github.com/python/mypy/issues/5264#issuecomment-399407428
if tp.TYPE_CHECKING:
    BaseList = UserList[tp.Optional[tp.Any]]
else:
    BaseList = UserList


class ListTwist(BaseList):
    """
    List-like class with additional attributes:
        * reversed, R - return reversed list
        * first, F - insert or retrieve first element;
                     Undefined for empty list
        * last, L -  insert or retrieve last element;
                     Undefined for empty list
        * size, S -  set or retrieve size of list;
                     If size less than list length - truncate to size;
                     If size greater than list length - pad with Nones
    """
    REVERSED = ['reversed', 'R']
    FIRST = ['first', 'F']
    LAST = ['last', 'L']
    SIZE = ['size', 'S']

    def __getattr__(self, name: str) -> tp.Any:
        if name in self.REVERSED:
            return list(reversed(self.data))
        elif name in self.FIRST:
            return self.data[0]
        elif name in self.LAST:
            return self.data[-1]
        elif name in self.SIZE:
            return len(self)
        else:
            return super().__getattribute__(name)

    def __setattr__(self, name: str, value: tp.Any) -> None:
        if name in self.FIRST:
            self.data[0] = value
        elif name in self.LAST:
            self.data[-1] = value
        elif name in self.SIZE:
            if value < len(self):
                del self.data[value:]
            elif value > len(self):
                self.data += [None] * (value - len(self))
        else:
            return super().__setattr__(name, value)
