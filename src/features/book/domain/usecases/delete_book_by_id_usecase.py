from src.features.book.domain.repositories.book_repository import AbstractBookRepository
from dataclasses import dataclass


@dataclass
class DeleteBookByIdUseCase:
    book_repo: AbstractBookRepository

    def run(self, bookId: str) -> None:
        return self.book_repo.delete_book_by_id(bookId)
