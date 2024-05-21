from src.features.book.domain.repositories.book_repository import AbstractBookRepository
from dataclasses import dataclass

from src.utils.usecase import UseCase


@dataclass
class BookDeleteUseCase(UseCase[str, str | None]):
    repo: AbstractBookRepository

    def __call__(self, args: str) -> str | None:
        return self.repo.book_delete(args)
