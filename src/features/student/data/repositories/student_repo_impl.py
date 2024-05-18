from dataclasses import dataclass
from src.features.student.domain.models.student_model import (
    Student,
    CreateStudentSchema,
    UpdateStudentSchema,
)
from src.features.student.domain.repository.student_repo import (
    AbstractStudentRepository,
)
from src.features.student.data.sources.student_source import AbstractStudentSource


@dataclass
class StudentRepositoryImpl(AbstractStudentRepository):
    source: AbstractStudentSource

    def create(self, new_student: CreateStudentSchema) -> str | None:
        return self.source.create(new_student)

    def get_all(self) -> list[Student]:
        db_students = self.source.getAll()

        return [
            Student(db_student[0], db_student[1], db_student[2], db_student[3])
            for db_student in db_students
        ]

    def get(self, id: str) -> Student | None:
        db_student = self.source.get(id)

        return (
            Student(
                id=db_student[0],
                name=db_student[1],
                phone_no=db_student[2],
                book_id=db_student[3],
            )
            if db_student != None
            else None
        )

    def update(self, updated_student: UpdateStudentSchema) -> str | None:
        return self.source.update(updated_student)

    def delete(self, id: str) -> str | None:
        return self.source.delete(id)

    def update_record(self, student_id: str, book_id: str | None):
        self.source.student_update_record(student_id, book_id)
