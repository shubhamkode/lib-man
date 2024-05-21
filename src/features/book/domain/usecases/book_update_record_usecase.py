from dataclasses import dataclass
from src.features.book.domain.repositories.book_repository import AbstractBookRepository

from src.utils.usecase import UseCase


@dataclass
class BookUpdateRecordUseCase(UseCase[tuple[str, str | None], None]):
    repo: AbstractBookRepository

    # 0 - bookId
    # 1 - student-Id
    def __call__(self, args: tuple[str, str | None]) -> None:
        return self.repo.update_record(args[0], args[1])
