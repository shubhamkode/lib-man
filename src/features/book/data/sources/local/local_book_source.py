from dataclasses import dataclass
from src.features.book.data.sources.book_source import AbstractBookSource
from src.shared.database_service import DatabaseService
from src.features.book.domain.models.book_model import (
    UpdateBookSchema,
    CreateBookSchema,
)


@dataclass
class LocalBookSource(AbstractBookSource):
    db: DatabaseService

    def create(self, book: CreateBookSchema) -> str | None:
        return self.db.mutation(
            "INSERT INTO BOOK(title,author,publisher) VALUES (?,?,?)",
            (book.title, book.author, book.publisher),
        )

    def get(self, id: str) -> tuple[str, ...] | None:
        res = self.db.query("SELECT * FROM BOOK WHERE id = ?", (id,))
        return res.fetchone()

    def getAll(self) -> list[tuple[str, ...]]:
        res = self.db.query("SELECT * FROM BOOK")
        return res.fetchall()

    def update(self, updated_book: UpdateBookSchema) -> str | None:
        db_book = self.get(updated_book.id)

        if db_book == None:
            return

        return self.db.mutation(
            "UPDATE BOOK SET title = ?, author = ?, publisher = ? WHERE id = ? ",
            (
                db_book[1] if updated_book.title == None else updated_book.title,
                db_book[3] if updated_book.author == None else updated_book.author,
                (
                    db_book[2]
                    if updated_book.publisher == None
                    else updated_book.publisher
                ),
                updated_book.id,
            ),
        )

    def delete(self, id: str) -> str | None:
        return self.db.mutation("DELETE FROM BOOK WHERE id = ?", (id,))

    def update_record(self, book_id: str, student_id: str | None):
        self.db.mutation(
            "UPDATE BOOK SET student_id = ? WHERE id = ?", (student_id, book_id)
        )
