from dataclasses import dataclass
from src.features.student.domain.repository.student_repo import (
    AbstractStudentRepository,
)

from src.utils.usecase import UseCase


@dataclass
class StudentDeleteUseCase(UseCase[str, str | None]):
    repo: AbstractStudentRepository

    def run(self, args: str) -> str | None:
        return self.repo.delete(args)
