from src.features.student.domain.models.student_model import CreateStudentSchema
from src.features.student.domain.repository.student_repo import (
    AbstractStudentRepository,
)
from dataclasses import dataclass

from src.utils.usecase import UseCase


@dataclass
class StudentCreateUseCase(UseCase[CreateStudentSchema, None]):
    repo: AbstractStudentRepository

    def run(self, args: CreateStudentSchema) -> None:
        self.repo.create(args)
