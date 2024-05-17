from typing import List, Optional
from dataclasses import dataclass
from src.features.student.domain.models.student_model import (
    Student,
    CreateStudentSchema,
    UpdateStudentSchema,
)
from src.features.student.domain.repository.student_repo import (
    AbstractStudentRepository,
)
from src.features.student.data.sources.student_source import AbstractStudentDataSource


@dataclass
class StudentRepositoryImpl(AbstractStudentRepository):
    source: AbstractStudentDataSource

    def get_all_students(self) -> List[Student]:

        students = self.source.getAll()

        return [
            Student(student[0], student[1], student[2], student[3])
            for student in students
        ]

    def create_new_student(self, data: CreateStudentSchema) -> None:
        self.source.create(data)

    def get_student_by_id(self, studentId: str) -> Optional[Student]:
        db_student = self.source.get(studentId)

        if not db_student:
            return None

        return Student(db_student[0], db_student[1], db_student[2], db_student[3])

    def delete_student_by_id(self, student_id: str) -> None:
        self.source.delete(student_id)

    def update_student_by_id(
        self, student_id: str, updated_student: UpdateStudentSchema
    ) -> None:
        self.source.update(student_id, updated_student)

    def update_record(self, id: str, book_id: Optional[str]) -> None:
        self.source.update_record(id, book_id)
