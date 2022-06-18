from dataclasses import dataclass, field, InitVar
from abc import ABC, abstractmethod
from typing import Union

DISCOUNT_PERCENTS = 15


@dataclass(order=True, frozen=True)
class Item:
    # note: mind the order of fields (!)
    item_id: int = field(compare=False)
    title: str
    cost: int

    def __post_init__(self) -> None:
        assert self.title
        assert self.cost > 0


# Do not remove `# type: ignore`
# It is [a really old issue](https://github.com/python/mypy/issues/5374)
@dataclass  # type: ignore
class Position(ABC):
    item: Item

    @property
    @abstractmethod
    def cost(self) -> Union[int, float]:
        pass


@dataclass()
class CountedPosition(Position):
    count: int = 1

    @property
    def cost(self) -> Union[int, float]:
        return self.count * self.item.cost


@dataclass()
class WeightedPosition(Position):
    weight: float = 1.0

    @property
    def cost(self) -> Union[int, float]:
        return self.weight * self.item.cost


@dataclass()
class Order:
    order_id: int
    positions: list[Position] = field(default_factory=list)
    cost: int = field(init=False)
    have_promo: InitVar[bool] = False

    def __post_init__(self, have_promo: bool) -> None:
        cost = sum(position.cost for position in self.positions)
        if have_promo:
            cost *= (100 - DISCOUNT_PERCENTS) / 100
        self.cost = int(cost)

