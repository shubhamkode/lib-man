from src.shared import SQLiteDatabaseService
from src.utils import get_database_queries


from inject import inject

DATABASE_NAME = "db.sqlite"
DATABASE_SQL_FILE = "./db.sql"


def runApp():

    # setup
    dbClient = SQLiteDatabaseService(DATABASE_NAME)

    dbClient.setup(get_database_queries(DATABASE_SQL_FILE))

    main_app_wrapper = inject(dbClient)

    main_app_wrapper.run().mainloop()


if __name__ == "__main__":
    runApp()
