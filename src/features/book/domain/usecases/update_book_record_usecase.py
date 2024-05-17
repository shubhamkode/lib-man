from dataclasses import dataclass
from typing import Optional
from src.features.book.domain.repositories.book_repository import AbstractBookRepository


@dataclass
class UpdateBookRecordUseCase:
    book_repo: AbstractBookRepository

    def run(self, book_id: str, student_id: Optional[str]):
        return self.book_repo.update_book_record(book_id, student_id)
