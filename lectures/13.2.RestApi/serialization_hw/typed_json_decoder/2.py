import json
import typing as tp
from decimal import Decimal


def typed(dct: tp.Mapping[str, tp.Any]) -> tp.Mapping[tp.Any, tp.Any]:
    if '__custom_key_type__' in dct:
        u = dct['__custom_key_type__']
        if u == 'decimal':
            c = Decimal
        else:
            c = eval(dct['__custom_key_type__'])
        return {c(key): value for key, value in dct.items() if key != '__custom_key_type__'}
    return dct


def decode_typed_json(json_value: str) -> tp.Any:
    """
    Returns deserialized object from json string.
    Checks __custom_key_type__ in object's keys to choose appropriate type.

    :param json_value: serialized object in json format
    :return: deserialized object
    """
    return json.loads(json_value, object_hook=typed)
