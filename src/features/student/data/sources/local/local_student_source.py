from dataclasses import dataclass
from src.features.student.data.sources.student_source import AbstractStudentDataSource
from src.shared.database_service import DatabaseService
from src.features.student.domain.models.student_model import CreateStudentSchema

from src.features.student.domain.models.student_model import UpdateStudentSchema
from typing import Optional


@dataclass
class LocalStudentDataSource(AbstractStudentDataSource):
    db: DatabaseService

    def create(self, data: CreateStudentSchema):
        self.db.mutation(
            "INSERT INTO STUDENT(name,phone_no) VALUES(?,?)", (data.name, data.phone_no)
        )

    def get(self, id: str):
        res = self.db.query("SELECT * FROM STUDENT WHERE id = ?", (id,))
        return res.fetchone()

    def getAll(self):
        res = self.db.query("SELECT * FROM STUDENT;")
        return res.fetchall()

    def update(self, id: str, updated_student: UpdateStudentSchema):
        db_student = self.get(id)

        if db_student == None:
            return

        self.db.mutation(
            "UPDATE STUDENT SET name = ?, phone_no = ? WHERE id = ?",
            (
                db_student[1] if updated_student.name == None else updated_student.name,
                (
                    db_student[2]
                    if updated_student.phone_no == None
                    else updated_student.phone_no
                ),
                id,
            ),
        )

    def update_record(self, id: str, book_id: Optional[str]):
        self.db.mutation(
            "UPDATE STUDENT SET book_id = ? WHERE id = ?",
            (book_id, id),
        )

    def delete(self, id: str):
        self.db.mutation("DELETE FROM STUDENT WHERE id = ?", (id,))
