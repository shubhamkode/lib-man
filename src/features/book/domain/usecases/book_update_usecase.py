from src.features.book.domain.models.book_model import UpdateBookSchema
from src.features.book.domain.repositories.book_repository import AbstractBookRepository
from dataclasses import dataclass
from src.utils.usecase import UseCase


@dataclass
class BookUpdateUseCase(UseCase[UpdateBookSchema, str | None]):
    repo: AbstractBookRepository

    def __call__(self, args: UpdateBookSchema) -> str | None:
        return self.repo.book_update(args)
