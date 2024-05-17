from typing import List, Optional
from src.features.book.domain.models.book_model import UpdateBookSchema
from src.features.book.domain.models.book_model import Book, CreateBookSchema
from src.features.book.domain.repositories.book_repository import AbstractBookRepository
from dataclasses import dataclass
from src.features.book.data.sources.book_source import AbstractBookSource


@dataclass
class BookRepositoryImpl(AbstractBookRepository):
    source: AbstractBookSource

    def getAllBooks(self) -> List[Book]:

        books = self.source.getAll()

        return [Book(book[0], book[1], book[3], book[2], book[4]) for book in books]

    def createNewBook(self, book: CreateBookSchema) -> None:
        self.source.create(book)

    def get_book_by_id(self, bookId: str) -> Optional[Book]:

        db_book = self.source.get(bookId)

        if not db_book:
            return None

        return Book(db_book[0], db_book[1], db_book[3], db_book[2], db_book[4])

    def delete_book_by_id(self, book_id: str) -> None:
        self.source.delete(book_id)

    def update_book(self, book_id: str, updated_book: UpdateBookSchema) -> None:
        self.source.update(book_id, updated_book)

    def update_book_record(self, book_id: str, student_id: Optional[str]) -> None:
        self.source.update_book_record(book_id, student_id)
