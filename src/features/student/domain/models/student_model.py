from dataclasses import dataclass


@dataclass
class Student:
    id: str
    name: str
    phone_no: str
    book_id: str | None = None


@dataclass
class CreateStudentSchema:
    name: str
    phone_no: str


@dataclass
class UpdateStudentSchema:
    id: str
    name: str | None = None
    phone_no: str | None = None
