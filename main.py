from src.shared.database_service import SQLiteDatabaseService
from src.utils.helpers import get_database_queries


from inject import inject

# from src.utils.clear_screen import clear_screen

DATABASE_NAME = "libman.sqlite"
DATABASE_SQL_FILE = "./db.sql"


def runApp():

    # setup
    dbClient = SQLiteDatabaseService(DATABASE_NAME)
    dbClient.setup(get_database_queries(DATABASE_SQL_FILE))

    (book_screen) = inject(dbClient)

    book_screen.mainloop()


if __name__ == "__main__":
    runApp()
