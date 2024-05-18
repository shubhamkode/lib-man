from abc import ABC, abstractmethod
from src.features.student.domain.models.student_model import (
    Student,
    CreateStudentSchema,
    UpdateStudentSchema,
)


class AbstractStudentRepository(ABC):

    @abstractmethod
    def create(self, new_student: CreateStudentSchema) -> str | None:
        pass

    @abstractmethod
    def get_all(self) -> list[Student]:
        pass

    @abstractmethod
    def get(self, id: str) -> Student | None:
        pass

    @abstractmethod
    def update(self, updated_student: UpdateStudentSchema) -> str | None:
        pass

    @abstractmethod
    def delete(self, id: str) -> str | None:
        pass

    @abstractmethod
    def update_record(self, student_id: str, book_id: str | None):
        pass
