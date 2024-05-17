from typing import List
from src.features.book.domain.models.book_model import Book
from src.features.book.domain.repositories.book_repository import AbstractBookRepository
from dataclasses import dataclass


@dataclass
class GetAllBooksUseCase:
    book_repo: AbstractBookRepository

    def run(self) -> List[Book]:
        return self.book_repo.getAllBooks()
