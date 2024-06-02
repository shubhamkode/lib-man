from abc import ABC, abstractmethod

from typing import TypedDict


class CreateArgs(TypedDict):
    name: str
    contact: str
    roll_no: str


class WhereArgs(TypedDict):
    id: str | None
    roll_no: str | None


class FindManyWhereArgs(TypedDict):
    name: str | None
    contact: str | None


class UpdateDataArgs(TypedDict):
    name: str | None
    contact: str | None
    roll_no: str | None


class StudentRepository(ABC):
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
