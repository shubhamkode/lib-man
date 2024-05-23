from dataclasses import dataclass


@dataclass
class Student:
    id: str
    name: str
    phone_no: str
    book_id: str | None = None

    def to_tuple(self):
        return (self.id, self.name, self.phone_no, self.book_id)


@dataclass
class CreateStudentSchema:
    name: str
    phone_no: str


@dataclass
class UpdateStudentSchema:
    id: str
    name: str | None = None
    phone_no: str | None = None
