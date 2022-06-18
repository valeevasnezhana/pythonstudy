import dataclasses
import pickle


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
    version = int(data[1])
    if 0 <= version <= pickle.HIGHEST_PROTOCOL:
        return PickleVersion(version > 1, version)

    return PickleVersion(False, -1)
