import sys
from dataclasses import dataclass
from src.features.admin.domain.models.admin_model import Admin

from src.features.book.presentation.book_view import BookView
from src.features.student.presentation.student_view import StudentView
from src.features.record.presentation.record_view import RecordView
from src.utils.clear_screen import clear_screen


@dataclass
class AdminView:

    book_view: BookView
    student_view: StudentView
    record_view: RecordView

    def run(self):
        name = input("Enter your name: ")
        password = input("Enter your password: ")

        # db_admin = self.search_admin_usecase(name)
        db_admin = ("admin", "admin")

        if name != db_admin[0]:
            print(f"No Admin found with name: {name}")
            sys.exit(0)

        admin = Admin(db_admin[0], db_admin[1])

        if not admin.verify_password(password):
            print(f"Wrong Password!")
            sys.exit(0)

        while True:
            self.display_menu()

    def display_menu(self):
        options = [
            ["Book Management", self.manage_books],
            ["Student Management", self.manage_students],
            ["Issue or Return Book", self.issue_or_return_book],
            ["Logout", self.exit],
        ]

        clear_screen()

        for index, option in enumerate(options):
            print(f"\t {index+1}. {option[0]}")

        user_choice = int(input(f"Enter your choice [1..{len(options)}]: "))

        options[user_choice - 1][1]()

    def manage_books(self):
        self.book_view.run()

    def manage_students(self):
        self.student_view.run()

    def issue_or_return_book(self):
        self.record_view.run()

    def exit(self):
        clear_screen()
        print("Thank you for using LibMan!!!")
        sys.exit(0)
