from abc import ABC, abstractmethod
from src.features.book.domain.models.book_model import (
    Book,
    CreateBookSchema,
    UpdateBookSchema,
)


class AbstractBookRepository(ABC):
    @abstractmethod
    def book_create(self, new_book: CreateBookSchema) -> str | None:
        pass

    @abstractmethod
    def book_get_all(self) -> list[Book]:
        pass

    @abstractmethod
    def book_get(self, id: str) -> Book | None:
        pass

    @abstractmethod
    def book_delete(self, id: str) -> str | None:
        pass

    @abstractmethod
    def book_update(self, updated_book: UpdateBookSchema) -> str | None:
        pass

    @abstractmethod
    def update_record(self, book_id: str, student_id: str | None):
        pass
