from typing import List, Optional
from abc import ABC, abstractmethod
from src.features.student.domain.models.student_model import Student


class AbstractStudentRepository(ABC):
    @abstractmethod
    def get_all_students(self) -> List[Student]:
        pass

    @abstractmethod
    def create_new_student(self) -> None:
        pass

    @abstractmethod
    def get_student_by_id(self) -> Optional[Student]:
        pass

    @abstractmethod
    def delete_student_by_id(self) -> None:
        pass

    @abstractmethod
    def update_student_by_id(self) -> None:
        pass

    @abstractmethod
    def update_record(self) -> None:
        pass
