import typing as tp
import json
from decimal import Decimal


def to_int(dct: dict[str, tp.Any]) -> dict[int, tp.Any]:
    res: dict[int, tp.Any] = {}
    for key, val in dct.items():
        if key != "__custom_key_type__":
            res[int(key)] = val
    return res


def to_float(dct: dict[str, tp.Any]) -> dict[float, tp.Any]:
    res: dict[float, tp.Any] = {}
    for key, val in dct.items():
        if key != "__custom_key_type__":
            res[float(key)] = val
    return res


def to_decimal(dct: dict[str, tp.Any]) -> dict[Decimal, tp.Any]:
    res: dict[Decimal, tp.Any] = {}
    for key, val in dct.items():
        if key != "__custom_key_type__":
            res[Decimal(key)] = val
    return res


def custom_key_type(dct: dict[str, tp.Any]) -> dict[tp.Any, tp.Any]:
    custom_type = dct.get("__custom_key_type__")
    res: dict[tp.Any, tp.Any] = {}
    if custom_type == 'decimal':
        res = to_decimal(dct)
    elif custom_type == 'int':
        res = to_int(dct)
    elif custom_type == 'float':
        res = to_float(dct)
    else:
        return dct
    return res


def decode_typed_json(json_value: str) -> tp.Any:
    """
    Returns deserialized object from json string.
    Checks __custom_key_type__ in object's keys to choose appropriate type.

    :param json_value: serialized object in json format
    :return: deserialized object
    """
    return json.loads(json_value, object_hook=custom_key_type)