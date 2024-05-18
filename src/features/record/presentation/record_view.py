from dataclasses import dataclass
from src.utils.clear_screen import clear_screen

from src.features.book.domain.usecases import (
    BookUpdateUseCase,
    BookUpdateRecordUseCase,
    BookGetUseCase,
)

from src.features.student.domain.usecases import (
    UpdateStudentRecordUseCase,
    StudentGetUseCase,
)
from typing import Callable


@dataclass
class RecordView:

    book_get_usecase: BookGetUseCase
    book_update_usecase: BookUpdateUseCase

    student_get_usecase: StudentGetUseCase

    update_student_record_usecase: UpdateStudentRecordUseCase
    book_update_record_usecase: BookUpdateRecordUseCase

    def run(self):
        options: dict[str, Callable[[], None]] = {
            "Issue Book": self.issue_book,
            "Return Book": self.return_book,
        }

        while True:
            clear_screen()
            for index, key in enumerate(options):
                print(f"\t {index+1}. {key}")
            print(f"\t {len(options)+1}. Return to Main Menu")

            user_choice = int(input(f"Enter your choice [1..{len(options)+1}]: "))

            if user_choice == len(options) + 1:
                return
            else:
                options[list(options.keys())[user_choice - 1]]()

                input("\nPress Enter to Continue...\n")

    def issue_book(self):
        clear_screen()
        # check if the book exists in the database and is available
        book_id = input("Enter book Id: ")
        db_book = self.book_get_usecase.run(book_id)

        if not db_book or db_book.student_id != None:
            print(f"Book with id: {book_id} cannot be issued...")
            return

        # check if the student in question has no book issued
        student_id = input("Enter Student Id: ")

        db_student = self.student_get_usecase.run(student_id)

        if db_student == None:
            return

        if db_student.book_id != None:
            print(f"Student with studentId: {student_id} already has a book issued...")
            return

        # issue the book to the student
        ## update book available status to false
        ## create new record of the book with student_id and book_id

        self.book_update_record_usecase.run((book_id, student_id))

        self.update_student_record_usecase.run(student_id, book_id)

        print(
            f"Book with bookId: {book_id} successfully issued to Student with studentId: {student_id}"
        )

    def return_book(self):
        # update student's book_id to null
        # update book_status to available
        clear_screen()
        student_id = input("Enter Student Id: ")

        db_student = self.student_get_usecase.run(student_id)

        if db_student == None or db_student.book_id == None:
            print(f"No Student Exists with id: {student_id} or no book borrowed.")
            return

        self.book_update_record_usecase.run((db_student.book_id, None))

        self.update_student_record_usecase.run(student_id, None)

        print(
            f"Book with bookId: {db_student.book_id} successfully returned by student with studentId: {student_id}"
        )
