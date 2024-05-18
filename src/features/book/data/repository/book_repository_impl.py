from src.features.book.domain.models.book_model import UpdateBookSchema
from src.features.book.domain.models.book_model import Book, CreateBookSchema
from src.features.book.domain.repositories.book_repository import AbstractBookRepository
from dataclasses import dataclass
from src.features.book.data.sources.book_source import AbstractBookSource


@dataclass
class BookRepositoryImpl(AbstractBookRepository):
    source: AbstractBookSource

    def book_get_all(self) -> list[Book]:
        db_books = self.source.getAll()

        return [
            Book(
                id=db_book[0],
                title=db_book[1],
                author=db_book[3],
                publisher=db_book[2],
            )
            for db_book in db_books
        ]

    def book_create(self, new_book: CreateBookSchema) -> str | None:
        return self.source.create(new_book)

    def book_get(self, id: str) -> Book | None:
        db_book = self.source.get(id)

        return (
            Book(
                id=db_book[0],
                title=db_book[1],
                author=db_book[3],
                publisher=db_book[2],
                student_id=db_book[4],
            )
            if db_book != None
            else None
        )

    def book_delete(self, id: str) -> str | None:
        return self.source.delete(id)

    def book_update(self, updated_book: UpdateBookSchema) -> str | None:
        return self.source.update(updated_book)

    def update_record(self, book_id: str, student_id: str | None):
        self.source.update_record(book_id, student_id)
