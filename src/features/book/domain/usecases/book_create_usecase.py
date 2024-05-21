from src.features.book.domain.models.book_model import CreateBookSchema
from src.features.book.domain.repositories.book_repository import AbstractBookRepository
from dataclasses import dataclass

from src.utils.usecase import UseCase


@dataclass
class BookCreateUseCase(UseCase[CreateBookSchema, str | None]):
    repo: AbstractBookRepository

    def __call__(self, args: CreateBookSchema) -> str | None:
        return self.repo.book_create(args)
