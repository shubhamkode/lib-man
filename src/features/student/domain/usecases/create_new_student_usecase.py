from src.features.student.domain.models.student_model import CreateStudentSchema
from src.features.student.domain.repository.student_repo import (
    AbstractStudentRepository,
)
from dataclasses import dataclass


@dataclass
class CreateNewStudentUseCase:
    student_repo: AbstractStudentRepository

    def run(self, student: CreateStudentSchema):
        self.student_repo.create_new_student(student)
