from dataclasses import dataclass
from typing import Optional


@dataclass
class Book:
    id: int
    title: str
    author: str
    publisher: str
    student_id: Optional[int]

    def status(self) -> str:
        return "Available" if self.student_id == None else "Borrowed"


@dataclass
class CreateBookSchema:
    title: str
    author: str
    publisher: str


@dataclass
class UpdateBookSchema:
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
