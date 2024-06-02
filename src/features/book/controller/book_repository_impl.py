from dataclasses import dataclass

from .book_repository import (
    CreateArgs,
    FindManyWhereArgs,
    UpdateDataArgs,
    WhereArgs,
    BookRepository,
)

from src.shared import DatabaseService


@dataclass
class BookRepoImpl(BookRepository):
    db: DatabaseService

    def create(self, data: CreateArgs):
        self.db.mutation(
            "INSERT INTO BOOK(title,author,publisher) VALUES (?,?,?)",
            (
                data["title"],
                data["author"],
                data["publisher"],
            ),
        )

    def findUnique(self, where: WhereArgs):
        res = self.db.query("SELECT * FROM BOOK WHERE id = ?", (where["id"],))
        return res.fetchone()

    def findMany(self, where: FindManyWhereArgs | None = None):
        res = self.db.query(
            """SELECT B.id, B.title, B.author, B.Publisher,R.student_id FROM BOOK AS B LEFT JOIN RECORD AS R ON R.book_id = B.id ORDER BY B.title ASC""",
        )
        return res.fetchall()

    def update(self, where: WhereArgs, data: UpdateDataArgs):
        db_book = self.findUnique(where=where)

        if db_book == None:
            return

        self.db.mutation(
            "UPDATE BOOK SET title = ?, publisher = ?, author = ? WHERE id = ?",
            (
                db_book[1] if data["title"] == None else data["title"],
                db_book[2] if data["publisher"] == None else data["publisher"],
                db_book[3] if data["author"] == None else data["author"],
                where["id"],
            ),
        )

    def delete(self, where: WhereArgs):
        self.db.mutation(
            "DELETE FROM BOOK WHERE id = ?",
            (where["id"],),
        )
