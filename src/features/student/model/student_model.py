from dataclasses import dataclass


@dataclass
class Student:
    id: str
    name: str
    contact: str
    roll_no: str
    book_id: str | None = None

    @classmethod
    def fromTuple(cls, tup: tuple[str, ...]):
        return cls(
            id=tup[0],
            name=tup[1],
            contact=tup[2],
            roll_no=tup[3],
            book_id=tup[4],
        )


@dataclass
class CreateStudentSchema:
    name: str
    contact: str
    roll_no: str


@dataclass
class UpdateStudentSchema:
    id: str
    name: str | None = None
    contact: str | None = None
    roll_no: str | None = None
