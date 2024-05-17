from typing import Optional
from src.features.student.domain.models.student_model import Student
from src.features.student.domain.repository.student_repo import (
    AbstractStudentRepository,
)
from dataclasses import dataclass


@dataclass
class GetStudentByIdUseCase:
    student_repo: AbstractStudentRepository

    def run(self, student_id: str) -> Optional[Student]:
        return self.student_repo.get_student_by_id(student_id)
