import dataclasses
from pickletools import genops


@dataclasses.dataclass
class PickleVersion:
    is_new_format: bool
    version: int


def get_pickle_version(data: bytes) -> PickleVersion:
    """
    Returns used protocol version for serialization.

    :param data: serialized object in pickle format.
    :return: protocol version.
    """
    opcode, arg, _ = next(genops(data))
    if opcode.name != 'PROTO':
        return PickleVersion(False, -1)
    if not isinstance(arg, int):
        raise RuntimeError()
    return PickleVersion(True, arg)