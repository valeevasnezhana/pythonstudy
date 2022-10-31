import typing as tp
from abc import ABC, abstractmethod
from dataclasses import dataclass

from .animals import Cat, Cow, Dog


class Animal(ABC):
    @abstractmethod
    def say(self) -> str:
        pass


@dataclass()
class CatAdapter(Animal):
    _cat: Cat

    def say(self) -> str:
        return self._cat.say()


@dataclass()
class DogAdapter(Animal):
    _dog: Dog

    def say(self) -> str:
        return self._dog.say("woof")


@dataclass()
class CowAdapter(Animal):
    _cow: Cow

    def say(self) -> str:
        return self._cow.talk()


def animals_factory(animal: tp.Any) -> Animal:
    if isinstance(animal, Cow):
        return CowAdapter(animal)
    elif isinstance(animal, Dog):
        return DogAdapter(animal)
    elif isinstance(animal, Cat):
        return CatAdapter(animal)
    else:
        raise TypeError("Unknown animal")
