from dataclasses import dataclass

from src.features.book.domain.models.book_model import Book
from src.features.book.domain.repositories.book_repository import AbstractBookRepository


from src.utils.usecase import UseCase


@dataclass
class BookGetAllUseCase(UseCase[None, list[Book]]):
    repo: AbstractBookRepository

    def __call__(self, args: None = None) -> list[Book]:
        return self.repo.book_get_all()
