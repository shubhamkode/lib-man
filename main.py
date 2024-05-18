from src.shared.database_service import SQLiteDatabaseService
from src.utils.helpers import get_database_queries

# views
from src.features.admin.presentation.admin_view import AdminView


from inject import inject
from src.utils.clear_screen import clear_screen


DATABASE_NAME = "libman.sqlite"
DATABASE_SQL_FILE = "./db.sql"


def runApp():

    # setup
    dbClient = SQLiteDatabaseService(DATABASE_NAME)
    dbClient.setup(get_database_queries(DATABASE_SQL_FILE))

    (book_view, student_view, record_view) = inject(dbClient)

    clear_screen()

    print("\tWelcome to LibMan!!!")

    AdminView(
        book_view=book_view,
        student_view=student_view,
        record_view=record_view,
    ).run()


if __name__ == "__main__":
    runApp()
