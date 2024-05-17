from src.features.book.domain.models.book_model import UpdateBookSchema
from src.features.book.domain.repositories.book_repository import AbstractBookRepository
from dataclasses import dataclass


@dataclass
class UpdateBookByIdUseCase:
    book_repo: AbstractBookRepository

    def run(self, book_id: str, updated_book: UpdateBookSchema):
        self.book_repo.update_book(book_id, updated_book)
