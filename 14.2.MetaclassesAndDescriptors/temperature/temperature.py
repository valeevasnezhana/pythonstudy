import typing as tp


class Temperature:
    def __init__(self, name: str):
        self._name = name

    def __delete__(self, obj: tp.Any):
        raise ValueError("Value can't be deleted")


class Kelvin(Temperature):
    def __init__(self, name: str):
        super().__init__(name)

    def __get__(self, obj: tp.Optional[tp.Any], obj_type: type) -> tp.Any:
        if obj is None:
            return self
        return getattr(obj, self._name)

    def __set__(self, obj: tp.Optional[tp.Any], value: int):
        if obj:
            try:
                getattr(obj, self._name)
            except AttributeError as e:
                raise e
            if value > 0:
                setattr(obj, self._name, value)
            else:
                raise ValueError("Kelvin Temperature must be positive")


class Celsius(Temperature):
    def __init__(self, name: str):
        super().__init__(name)

    def __get__(self, obj: tp.Optional[tp.Any], obj_type: type) -> tp.Any:
        if obj is None:
            return self
        absolute_temperature = type(obj).__dict__[self._name]
        if not isinstance(absolute_temperature, Kelvin):
            raise AttributeError(
                f"""Celsius based on Kelvin descriptors, got {absolute_temperature}
                 with type {type(absolute_temperature)}""")
        return absolute_temperature.__get__(obj, type(obj)) - 273

    def __set__(self, *args):
        raise AttributeError("Celsius value can't be changed, use Kelvin to set this attribute")