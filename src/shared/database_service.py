from abc import ABC, abstractmethod
import _sqlite3


class DatabaseService(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def query(self):
        pass

    def mutation(self):
        pass

    def setup(self):
        pass


class SQLiteDatabaseService(DatabaseService):
    def __init__(self, dbName: str):
        self.conn = _sqlite3.connect(f"{dbName}", check_same_thread=True)
        self.cursor = self.conn.cursor()

    def query(self, queryStr: str, parameters=()):
        return self.cursor.execute(queryStr, parameters)

    def mutation(self, mutationStr: str, parameters=()):
        res = self.cursor.execute(mutationStr, parameters)
        self.conn.commit()
        return res.lastrowid

    def setup(self, setupStr: str):
        self.cursor.executescript(setupStr)

    def __del__(self):
        self.cursor.close()
        self.conn.close()
