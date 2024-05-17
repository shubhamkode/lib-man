from dataclasses import dataclass
from src.utils.clear_screen import clear_screen

from src.features.book.domain.models.book_model import UpdateBookSchema

from src.features.book.domain.usecases import (
    GetBookByIdUseCase,
    UpdateBookByIdUseCase,
    UpdateBookRecordUseCase,
)

from src.features.student.domain.usecases import (
    GetStudentByIdUseCase,
    UpdateStudentRecordUseCase,
)


@dataclass
class RecordView:

    get_book_by_id_usecase: GetBookByIdUseCase
    update_book_by_id_usecase: UpdateBookByIdUseCase
    get_student_by_id_usecase: GetStudentByIdUseCase
    update_student_record_usecase: UpdateStudentRecordUseCase

    update_book_record_usecase: UpdateBookRecordUseCase

    def run(self):
        options = [
            ["Issue a Book", self.issue_book],
            ["Return a Book", self.return_book],
        ]

        while True:
            clear_screen()
            for index, option in enumerate(options):
                print(f"\t {index+1}. {option[0]}")
            print(f"\t {len(options)+1}. Return to Main Menu")

            user_choice = int(input(f"Enter your choice [1..{len(options)+1}]: "))

            if user_choice == len(options) + 1:
                return
            else:
                options[user_choice - 1][1]()

                input("\nPress Enter to Continue...\n")

    def issue_book(self):
        clear_screen()
        # check if the book exists in the database and is available
        book_id = int(input("Enter book Id: "))
        db_book = self.get_book_by_id_usecase.run(book_id)

        if not db_book or db_book.student_id != None:
            print(f"Book with id: {book_id} cannot be issued...")
            return

        # check if the student in question has no book issued
        student_id = int(input("Enter Student Id: "))

        db_student = self.get_student_by_id_usecase.run(student_id)

        if not db_student.book_id == None:
            print(f"Student with studentId: {student_id} already has a book issued...")
            return

        # issue the book to the student
        ## update book available status to false
        ## create new record of the book with student_id and book_id

        self.update_book_record_usecase.run(book_id, student_id)

        self.update_student_record_usecase.run(student_id, book_id)

        print(
            f"Book with bookId: {book_id} successfully issued to Student with studentId: {student_id}"
        )

    def return_book(self):
        # update student's book_id to null
        # update book_status to available
        clear_screen()
        student_id = int(input("Enter Student Id: "))

        db_student = self.get_student_by_id_usecase.run(student_id)

        if db_student == None or db_student.book_id == None:
            print(f"No Student Exists with id: {student_id} or no book borrowed.")
            return

        self.update_book_record_usecase.run(db_student.book_id, None)

        self.update_student_record_usecase.run(student_id, None)

        print(
            f"Book with bookId: {db_student.book_id} successfully returned by student with studentId: {student_id}"
        )
