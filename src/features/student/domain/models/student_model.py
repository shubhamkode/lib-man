from dataclasses import dataclass
from typing import Optional


@dataclass
class Student:
    id: int
    name: str
    phone_no: str
    book_id: Optional[int]


@dataclass
class CreateStudentSchema:
    name: str
    phone_no: str


@dataclass
class UpdateStudentSchema:
    name: Optional[str] = None
    phone_no: Optional[str] = None
