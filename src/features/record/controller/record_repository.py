from typing import TypedDict
from dataclasses import dataclass

from src.shared import DatabaseService


class CreateRecordArgs(TypedDict):
    student_id: int
    book_id: int


class WhereRecordArgs(TypedDict):
    student_id: int | None


@dataclass
class RecordRepository:
    db: DatabaseService

    def create(self, data: CreateRecordArgs):
        self.db.mutation(
            "INSERT INTO RECORD(student_id,book_id) VALUES (?,?)",
            (
                data["student_id"],
                data["book_id"],
            ),
        )

    def delete(
        self,
        where: WhereRecordArgs,
    ):
        self.db.mutation(
            "DELETE FROM RECORD WHERE student_id = ?", (where["student_id"],)
        )
