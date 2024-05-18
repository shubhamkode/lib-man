from abc import ABC, abstractmethod
from src.features.student.domain.models.student_model import (
    UpdateStudentSchema,
    CreateStudentSchema,
)


class AbstractStudentSource(ABC):
    @abstractmethod
    def create(self, student: CreateStudentSchema) -> str | None:
        pass

    @abstractmethod
    def getAll(self) -> list[tuple[str, ...]]:
        pass

    @abstractmethod
    def get(self, id: str) -> tuple[str, ...] | None:
        pass

    @abstractmethod
    def update(self, updated_student: UpdateStudentSchema) -> str | None:
        pass

    @abstractmethod
    def delete(self, id: str) -> str | None:
        pass

    @abstractmethod
    def student_update_record(self, student_id: str, book_id: str | None):
        pass
