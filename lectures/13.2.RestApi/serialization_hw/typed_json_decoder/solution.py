import typing as tp
import json

from decimal import Decimal


TYPE_STR_TO_TYPE_OBJ = {
    'int': int,
    'float': float,
    'decimal': Decimal,
}


def decode_typed_json(json_value: str) -> tp.Any:
    """
    Returns deserialized object from json string.
    Checks __custom_key_type__ in object's keys to choose appropriate type.

    :param json_value: serialized object in json format
    :return: deserialized object
    """
    def object_hook(dct: tp.Dict[str, tp.Any]) -> tp.Dict[tp.Any, tp.Any]:
        custom_key_type = dct.pop('__custom_key_type__', None)
        if custom_key_type is not None:
            type_obj = TYPE_STR_TO_TYPE_OBJ[custom_key_type]
            return {type_obj(key): value for key, value in dct.items()}
        return dct

    return json.loads(json_value, object_hook=object_hook)
