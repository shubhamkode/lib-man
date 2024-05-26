from dataclasses import dataclass


@dataclass
class Book:
    id: str
    title: str
    author: str
    publisher: str
    student_id: str | None = None

    @property
    def status(self) -> str:
        return "AVAILABLE" if self.student_id == None else "BORROWED"

    def to_tuple(self):
        return (
            self.id,
            self.title,
            self.author,
            self.publisher,
            self.status,
        )


@dataclass
class CreateBookSchema:
    title: str
    author: str
    publisher: str


@dataclass
class UpdateBookSchema:
    id: str
    title: str | None = None
    author: str | None = None
    publisher: str | None = None
