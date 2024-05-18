from src.features.student.domain.models.student_model import Student
from src.features.student.domain.repository.student_repo import (
    AbstractStudentRepository,
)
from dataclasses import dataclass


from src.utils.usecase import UseCase


@dataclass
class StudentGetAllUseCase(UseCase[None, list[Student]]):
    repo: AbstractStudentRepository

    def run(self, args: None = None) -> list[Student]:
        return self.repo.get_all()
