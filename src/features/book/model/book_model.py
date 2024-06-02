from dataclasses import dataclass


@dataclass
class Book:
    id: str
    title: str
    author: str
    publisher: str
    student_id: str | None = None

    @classmethod
    def fromTuple(cls, tup: tuple[str, ...]):
        return cls(
            id=tup[0],
            title=tup[1],
            author=tup[2],
            publisher=tup[3],
            student_id=tup[4],
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
