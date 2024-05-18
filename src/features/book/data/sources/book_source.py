from abc import ABC, abstractmethod

from src.features.book.domain.models.book_model import (
    UpdateBookSchema,
    CreateBookSchema,
)


class AbstractBookSource(ABC):
    @abstractmethod
    def create(self, book: CreateBookSchema) -> str | None:
        pass


    @abstractmethod
    def getAll(self) -> list[tuple[str, ...]]:
        pass

    @abstractmethod
    def get(self, id: str) -> tuple[str, ...] | None:
        pass

    @abstractmethod
    def update(self, updated_book: UpdateBookSchema) -> str | None:
        pass

    @abstractmethod
    def delete(self, id: str) -> str | None:
        pass

    @abstractmethod
    def update_record(self, book_id: str, student_id: str | None):
        pass
