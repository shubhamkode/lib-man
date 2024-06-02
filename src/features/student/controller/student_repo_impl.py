from dataclasses import dataclass

from src.features.student.controller.student_repo import (
    CreateArgs,
    FindManyWhereArgs,
    StudentRepository,
    UpdateDataArgs,
    WhereArgs,
)
from src.shared import DatabaseService


@dataclass
class StudentRepoImpl(StudentRepository):
    db: DatabaseService

    def create(self, data: CreateArgs):
        self.db.mutation(
            "INSERT INTO STUDENT(name,contact,roll_no) VALUES (?,?,?)",
            (
                data["name"],
                data["contact"],
                data["roll_no"],
            ),
        )

    def findUnique(self, where: WhereArgs):
        if where["id"] != None and where["roll_no"] != None:
            return

        if where["id"] == None and where["roll_no"] != None:
            res = self.db.query(
                "SELECT S.id,S.name,S.contact,S.roll_no,R.book_id FROM STUDENT AS S LEFT JOIN RECORD AS R ON R.student_id = S.id WHERE roll_no = ? ",
                (where["roll_no"],),
            )
            return res.fetchone()

        elif where["roll_no"] == None and where["id"] != None:
            res = self.db.query(
                "SELECT S.id,S.name,S.contact,S.roll_no,R.book_id FROM STUDENT AS S LEFT JOIN RECORD AS R ON R.student_id = S.id WHERE id = ? ",
                (where["id"],),
            )
            return res.fetchone()

    def findMany(self, where: FindManyWhereArgs | None = None) -> list[tuple[str, ...]]:
        res = self.db.query(
            """
                SELECT S.id,S.name,S.contact,S.roll_no,R.book_id FROM STUDENT AS S LEFT JOIN RECORD AS R ON R.student_id = S.id ORDER BY S.name ASC
            """
        )
        return res.fetchall()

    def update(self, where: WhereArgs, data: UpdateDataArgs):
        db_student = self.findUnique(where)

        if db_student == None:
            return

        self.db.mutation(
            "UPDATE STUDENT SET name = ?, contact = ?, roll_no = ? WHERE id = ?",
            (
                db_student[1] if data["name"] == None else data["name"],
                db_student[2] if data["contact"] == None else data["contact"],
                db_student[3] if data["roll_no"] == None else data["roll_no"],
                where["id"],
            ),
        )

    def delete(self, where: WhereArgs):
        self.db.mutation("DELETE FROM STUDENT WHERE id = ?", (where["id"],))
