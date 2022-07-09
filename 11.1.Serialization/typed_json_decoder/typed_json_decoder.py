import typing as tp
import json

from decimal import Decimal


STR_TO_PYTHONIC_TYPE = {'int': int, 'float': float, 'decimal': Decimal}
MAGIC_KEY = "__custom_key_type__"


def decode_typed_json(json_value: str) -> tp.Any:
    """
    Returns deserialized object from json string.
    Checks __custom_key_type__ in object's keys to choose appropriate type.

    :param json_value: serialized object in json format
    :return: deserialized object
    """
    def object_hook(dct: tp.Dict[str, tp.Any]) -> tp.Dict[tp.Any, tp.Any]:
        type_string = dct.pop(MAGIC_KEY, None)
        if type_string is not None:
            pythonic_type = STR_TO_PYTHONIC_TYPE[type_string]
            return {pythonic_type(key): value for key, value in dct.items()}
        return dct
    return json.loads(json_value, object_hook=object_hook)