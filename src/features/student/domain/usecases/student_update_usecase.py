from src.features.student.domain.models.student_model import UpdateStudentSchema
from src.features.student.domain.repository.student_repo import (
    AbstractStudentRepository,
)
from dataclasses import dataclass
from src.utils.usecase import UseCase


@dataclass
class StudentUpdateUseCase(UseCase[UpdateStudentSchema, str | None]):
    repo: AbstractStudentRepository

    def __call__(self, args: UpdateStudentSchema) -> str | None:
        return self.repo.update(args)
