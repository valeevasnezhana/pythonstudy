import typing as tp
import numbers
import abc

import typing as tp


T_co = tp.TypeVar('T_co', covariant=True)


class Gettable(tp.Protocol[T_co]):
    def __getitem__(self, item: int) -> T_co:
        pass

    def __len__(self) -> int:
        pass


def get(container: Gettable[T_co], index: int) -> tp.Optional[T_co]:
    if container:
        return container[index]

    return None

def case3() -> None:
    class A:
        def __getitem__(self, item: int) -> bool:
            return True

        def __len__(self) -> int:
            return 0

    get(A(), 4)

