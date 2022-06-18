import typing as tp
import json

from decimal import Decimal


def change_types(data: tp.Any) -> None:
    if isinstance(data, dict) and "__custom_key_type__" in data:
        cast_type = data["__custom_key_type__"]
        data.pop("__custom_key_type__")
        keys = [key for key in data]
        if cast_type == "int":
            for key in keys:
                new_key_int: int = int(key)
                data[new_key_int] = data[key]
                data.pop(key)
        elif cast_type == "float":
            for key in keys:
                new_key_float: float = float(key)
                data[new_key_float] = data[key]
                data.pop(key)
        else:
            for key in keys:
                new_key_decimal: Decimal = Decimal(key)
                data[new_key_decimal] = data[key]
                data.pop(key)


def change_dict(data: tp.Any) -> None:
    if isinstance(data, dict):
        change_types(data)
        for key, value in data.items():
            change_dict(value)
    elif isinstance(data, list):
        change_types(data)
        for elem in data:
            change_dict(elem)


def decode_typed_json(json_value: str) -> tp.Any:
    """
    Returns deserialized object from json string.
    Checks __custom_key_type__ in object's keys to choose appropriate type.

    :param json_value: serialized object in json format
    :return: deserialized object
    """
    data = json.loads(json_value)
    change_dict(data)
    return data
