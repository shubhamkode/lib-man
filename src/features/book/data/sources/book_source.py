from abc import ABC, abstractmethod
from typing import Optional


class AbstractBookSource(ABC):
    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def getAll(self):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def search(self):
        pass

    @abstractmethod
    def update_book_record(self, book_id: str, student_id: Optional[str]):
        pass
