from typing import List, Optional
from abc import ABC, abstractmethod
from src.features.book.domain.models.book_model import Book


class AbstractBookRepository(ABC):
    @abstractmethod
    def getAllBooks(self) -> List[Book]:
        pass

    @abstractmethod
    def createNewBook(self) -> None:
        pass

    @abstractmethod
    def get_book_by_id(self) -> Book:
        pass

    @abstractmethod
    def delete_book_by_id(self) -> None:
        pass

    @abstractmethod
    def update_book(self) -> None:
        pass

    @abstractmethod
    def update_book_record(self, book_id: str, student_id: Optional[str]):
        pass
