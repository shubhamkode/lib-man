from dataclasses import dataclass


@dataclass
class AuthException(Exception):
    message: str


@dataclass
class StudentException(Exception):
    message: str


@dataclass
class BookException(Exception):
    message: str
