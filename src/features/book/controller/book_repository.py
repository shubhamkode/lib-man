from abc import ABC, abstractmethod

from typing import TypedDict


class CreateArgs(TypedDict):
    title: str
    publisher: str | None
    author: str | None


class WhereArgs(TypedDict):
    id: str


class UpdateDataArgs(TypedDict):
    title: str | None
    publisher: str | None
    author: str | None


class FindManyWhereArgs(TypedDict):
    title: str | None
    publisher: str | None
    author: str | None


class BookRepository(ABC):
    @abstractmethod
    def create(self, data: CreateArgs):
        pass

    @abstractmethod
    def findUnique(self, where: WhereArgs):
        pass

    @abstractmethod
    def findMany(self, where: FindManyWhereArgs | None = None) -> list[tuple[str, ...]]:
        pass

    @abstractmethod
    def update(self, where: WhereArgs, data: UpdateDataArgs):
        pass

    @abstractmethod
    def delete(self, where: WhereArgs):
        pass
