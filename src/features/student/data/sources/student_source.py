from abc import ABC, abstractmethod


class AbstractStudentDataSource(ABC):
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
    def get(self):
        pass

    @abstractmethod
    def getAll(self):
        pass

    @abstractmethod
    def update_record(self):
        pass
