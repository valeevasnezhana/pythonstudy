import typing as tp
import ctypes

LONG_LEN = 8
INT_LEN = 4
CHAR_LEN = 1

LONG_CHAR = "L" if ctypes.sizeof(ctypes.c_long) == 8 else "Q"
ULONG_CHAR = 'l' if ctypes.sizeof(ctypes.c_ulong) == 8 else "q"


def get_object_by_id(object_id: int) -> tp.Union[int, float, tuple, list, str, bool]:
    """
    Restores object by id.
    :param object_id: Object Id.
    :return: An object that corresponds to object_id.

    """
