from src.shared.database_service import SQLiteDatabaseService
from src.utils.helpers import get_database_queries

# views
from src.features.admin.presentation.admin_view import AdminView

import tkinter as tk
from tkinter import TclError, ttk


from inject import inject

# from src.utils.clear_screen import clear_screen
from src.features.book.presentation.book_screen import BookScreen


DATABASE_NAME = "libman.sqlite"
DATABASE_SQL_FILE = "./db.sql"



def runApp():

    # setup
    dbClient = SQLiteDatabaseService(DATABASE_NAME)
    dbClient.setup(get_database_queries(DATABASE_SQL_FILE))

    (book_screen, student_view, record_view) = inject(dbClient)

    # AdminView(
    #     book_view=book_view,
    #     student_view=student_view,
    #     record_view=record_view,
    # ).run()

    # create_main_window()

    book_screen.mainloop()



if __name__ == "__main__":
    runApp()
