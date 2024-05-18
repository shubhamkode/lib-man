from src.features.book.domain.models.book_model import Book
from src.features.book.domain.repositories.book_repository import AbstractBookRepository
from dataclasses import dataclass

from src.utils.usecase import UseCase


@dataclass
class BookGetUseCase(UseCase[str, Book | None]):
    repo: AbstractBookRepository

    def run(self, args: str) -> Book | None:
        return self.repo.book_get(args)
