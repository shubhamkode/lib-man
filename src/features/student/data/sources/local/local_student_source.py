from dataclasses import dataclass
from src.features.student.data.sources.student_source import AbstractStudentSource
from src.shared.database_service import DatabaseService
from src.features.student.domain.models.student_model import (
    CreateStudentSchema,
    UpdateStudentSchema,
)


@dataclass
class LocalStudentDataSource(AbstractStudentSource):
    db: DatabaseService

    def create(self, student: CreateStudentSchema) -> str | None:
        return self.db.mutation(
            "INSERT INTO STUDENT(name,phone_no) VALUES(?,?)",
            (student.name, student.phone_no),
        )

    def get(self, id: str) -> tuple[str, ...] | None:
        res = self.db.query("SELECT * FROM STUDENT WHERE id = ?", (id,))
        return res.fetchone()

    def getAll(self) -> list[tuple[str, ...]]:
        res = self.db.query("SELECT * FROM STUDENT")
        return res.fetchall()

    def update(self, updated_student: UpdateStudentSchema) -> str | None:
        db_student = self.get(updated_student.id)

        if db_student == None:
            return

        return self.db.mutation(
            "UPDATE STUDENT SET name = ?, phone_no = ? WHERE id = ?",
            (
                db_student[1] if updated_student.name == None else updated_student.name,
                (
                    db_student[2]
                    if updated_student.phone_no == None
                    else updated_student.phone_no
                ),
                updated_student.id,
            ),
        )

    def delete(self, id: str) -> str | None:
        return self.db.mutation("DELETE FROM STUDENT WHERE id = ?", (id,))

    def student_update_record(self, student_id: str, book_id: str | None):
        self.db.mutation(
            "UPDATE STUDENT SET book_id = ? WHERE id = ?",
            (book_id, student_id),
        )
