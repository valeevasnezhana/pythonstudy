import dataclasses
import io


@dataclasses.dataclass
class PickleVersion:
    is_new_format: bool
    version: int


NEW_FORMAT_PREFIX = b'\x80'


def get_pickle_version(data: bytes) -> PickleVersion:
    """
    Returns used protocol version for serialization.

    :param data: serialized object in pickle format.
    :return: protocol version.
    """
    with io.BytesIO(data) as stream:
        first_byte = stream.read(1)
        if first_byte == NEW_FORMAT_PREFIX:
            pickle_version = stream.read(1)[0]
            return PickleVersion(True, pickle_version)
        return PickleVersion(False, -1)
