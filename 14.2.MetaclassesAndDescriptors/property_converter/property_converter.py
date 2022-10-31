from collections import defaultdict
import typing as tp
from dataclasses import dataclass
import inspect


@dataclass()
class OldProperty:
    getter: tp.Optional[tp.Callable] = None
    setter: tp.Optional[tp.Callable] = None


class PropertyConverterMeta(type):
    def __new__(mcs: type, name: str, bases: tp.Tuple[type], dct: tp.Dict[str, tp.Any]) -> 'PropertyConverterMeta':
        properties: tp.DefaultDict[str, OldProperty] = defaultdict(OldProperty)
        for base in bases:
            get_functions = inspect.getmembers(base, inspect.isfunction)
            for name, value in get_functions:
                if name in dct:
                    value = dct[name]
                if name.startswith("get_"):
                    properties[name[4:]].getter = value
                if name.startswith("set_"):
                    properties[name[4:]].setter = value
        for name, prop in properties.items():
            if name in dct:
                continue
            dct[name] = property(prop.getter, prop.setter)
        return tp.cast(PropertyConverterMeta, type.__new__(mcs, name, bases, dct))


class PropertyConverter(metaclass=PropertyConverterMeta):
    pass
