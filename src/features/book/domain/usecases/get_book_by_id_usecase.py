from typing import List, Optional
from src.features.book.domain.models.book_model import Book
from src.features.book.domain.repositories.book_repository import AbstractBookRepository
from dataclasses import dataclass


@dataclass
class GetBookByIdUseCase:
    book_repo: AbstractBookRepository

    def run(self, bookId: str) -> Optional[Book]:
        return self.book_repo.get_book_by_id(bookId)
