from src.features.student.domain.models.student_model import Student
from src.features.student.domain.repository.student_repo import (
    AbstractStudentRepository,
)
from dataclasses import dataclass

from src.utils.usecase import UseCase


@dataclass
class StudentGetUseCase(UseCase[str, Student | None]):
    repo: AbstractStudentRepository

    def __call__(self, args: str) -> Student | None:
        return self.repo.get(args)
