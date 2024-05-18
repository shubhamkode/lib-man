from dataclasses import dataclass

from src.features.student.domain.repository.student_repo import (
    AbstractStudentRepository,
)


@dataclass
class UpdateStudentRecordUseCase:
    student_repo: AbstractStudentRepository

    def run(self, student_id: str, book_id: str | None):
        self.student_repo.update_record(student_id, book_id)
