from src.features.student.domain.models.student_model import UpdateStudentSchema
from src.features.student.domain.repository.student_repo import (
    AbstractStudentRepository,
)
from dataclasses import dataclass


@dataclass
class UpdateStudentByIdUseCase:
    student_repo: AbstractStudentRepository

    def run(self, student_id, updated_student: UpdateStudentSchema):
        self.student_repo.update_student_by_id(student_id, updated_student)
