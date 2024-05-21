from dataclasses import dataclass

import textwrap


def wrap(string: str):
    return "\n".join(textwrap.wrap(string))


@dataclass
class Book:
    id: str
    title: str
    author: str
    publisher: str
    student_id: str | None = None

    def status(self) -> str:
        return "Available" if self.student_id == None else "Borrowed"

    def to_tuple(self):
        return (self.id, wrap(self.title), self.author, self.publisher)


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
