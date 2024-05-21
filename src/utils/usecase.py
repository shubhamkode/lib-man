from abc import ABC, abstractmethod
from typing import TypeVar, Generic

K = TypeVar("K")
V = TypeVar("V")


class UseCase(Generic[K, V], ABC):
    @abstractmethod
    def __call__(self, args: K) -> V:
        pass
