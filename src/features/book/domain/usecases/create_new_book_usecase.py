from src.features.book.domain.models.book_model import CreateBookSchema
from src.features.book.domain.repositories.book_repository import AbstractBookRepository
from dataclasses import dataclass


@dataclass
class CreateNewBookUseCase:
    book_repo: AbstractBookRepository

    def run(self, book: CreateBookSchema):
        self.book_repo.createNewBook(book)
