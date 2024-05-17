from typing import List
from src.features.student.domain.models.student_model import Student
from src.features.student.domain.repository.student_repo import AbstractStudentRepository
from dataclasses import dataclass


@dataclass
class GetAllStudentsUseCase:
    student_repo: AbstractStudentRepository

    def run(self) -> List[Student]:
        return self.student_repo.get_all_students()
