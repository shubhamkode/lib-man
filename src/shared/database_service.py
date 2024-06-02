from abc import ABC, abstractmethod
import sqlite3


class DatabaseService(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def query(self, query: str, parameters: tuple[str, ...] = ()) -> sqlite3.Cursor:
        pass

    @abstractmethod
    def mutation(
        self, query: str, parameters: tuple[str | int | None, ...] = ()
    ) -> str | None:
        pass

    @abstractmethod
    def setup(self, setup_str: str):
        pass


class SQLiteDatabaseService(DatabaseService):
    def __init__(self, dbName: str):
        self.conn = sqlite3.connect(f"{dbName}", check_same_thread=True)
        self.cursor = self.conn.cursor()

    def query(self, query: str, parameters: tuple[str, ...] = ()) -> sqlite3.Cursor:
        res = self.cursor.execute(query, parameters)
        return res

    def mutation(
        self, query: str, parameters: tuple[str | int | None, ...] = ()
    ) -> str | None:
        self.cursor.execute(query, parameters)
        self.conn.commit()

    def setup(self, setup_str: str):
        self.cursor.executescript(setup_str)

    def __del__(self):
        self.cursor.close()
        self.conn.close()
