from dataclasses import dataclass
from src.features.student.domain.repository.student_repo import (
    AbstractStudentRepository,
)


@dataclass
class DeleteStudentByIdUseCase:
    student_repo: AbstractStudentRepository

    def run(self, studentId: str) -> None:
        self.student_repo.delete_student_by_id(studentId)
