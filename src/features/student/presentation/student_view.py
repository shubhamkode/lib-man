from dataclasses import dataclass
from typing import Callable

from src.features.student.domain.usecases import (
    StudentCreateUseCase,
    StudentGetAllUseCase,
    StudentGetUseCase,
    StudentUpdateUseCase,
    StudentDeleteUseCase,
)

from src.features.book.domain.usecases import BookGetUseCase

from src.features.student.domain.models.student_model import (
    Student,
    CreateStudentSchema,
    UpdateStudentSchema,
)

from src.features.book.domain.models.book_model import Book

from src.utils.clear_screen import clear_screen


@dataclass
class StudentView:

    student_create_usecase: StudentCreateUseCase
    student_get_all_usecase: StudentGetAllUseCase
    student_get_usecase: StudentGetUseCase
    student_update_usecase: StudentUpdateUseCase
    student_delete_usecase: StudentDeleteUseCase

    book_get_usecase: BookGetUseCase

    def run(self):
        options: dict[str, Callable[[], None]] = {
            "Add Student": self.student_create,
            "Display All Student": self.student_get_all,
            "Search Student": self.student_get,
            "Update Student": self.student_update,
            "Delete Student": self.student_delete,
        }

        while True:
            clear_screen()
            for index, key in enumerate(options.keys()):
                print(f"\t {index+1}. {key}")
            print(f"\t {len(options)+1}. Return to Main Menu")

            user_choice = int(input(f"Enter your choice [1..{len(options)+1}]: "))

            if user_choice == len(options) + 1:
                return
            else:
                options[list(options.keys())[user_choice - 1]]()

                input("\nPress Enter to Continue...\n")

    def student_create(self):
        phone_no: str

        while True:

            clear_screen()
            name = input("Enter Student Name: ")

            while True:
                phone_no = input("Enter Student Phone No: ")
                if len(phone_no) == 10:
                    break
                else:
                    print("Invalid Phone No.")

            self.student_create_usecase.run(CreateStudentSchema(name, phone_no))

            print("Student Added Successfully....")

            choice = input("Do you want to continue adding more students? [Yes/No]: ")
            if choice in ["No", "no", "n", "NO"]:
                break
            elif choice in ["YES", "Yes", "yes", "y"]:
                continue
            else:
                print("Invalid Choice..")
                break

    def student_get_all(self):
        clear_screen()
        print_students(self.student_get_all_usecase.run())

    def student_get(self):

        book: Book | None = None

        clear_screen()
        student_id = input("Enter student Id: ")

        db_student = self.student_get_usecase.run(student_id)

        if db_student == None:
            print(f"No Student found with Id: {student_id}")
            return

        if db_student.book_id != None:
            book = self.book_get_usecase.run(db_student.book_id)

        print_student(db_student, book)

    def student_update(self):
        phone_no: str

        clear_screen()

        student_id = input("Enter Student Id: ")

        name = input("Enter Updated Name: ")

        while True:
            phone_no = input("Enter Updated Phone No: ")
            if len(phone_no) == 10:
                break
            else:
                print("Invalid Phone No.")

        self.student_update_usecase.run(
            UpdateStudentSchema(
                student_id,
                name if len(name) != 0 else None,
                phone_no if len(phone_no) != 0 else None,
            )
        )

        print(f"Student with id: {student_id} updated successfully.")

    def student_delete(self):
        clear_screen()

        student_id = input("Enter Student Id: ")
        self.student_delete_usecase.run(student_id)
        print(f"Student with id: {student_id} deleted successfully..")


def print_students(students: list[Student]) -> None:
    for student in students:
        print(
            f"""
            ****************
                id: {student.id}
                Name: {student.name}
                Phone No: {student.phone_no}
            ****************"""
        )


def print_student(student: Student, book: Book | None = None):
    print(
        f"""
            ****************
                id: {student.id}
                Name: {student.name}
                Phone No: {student.phone_no}

                ****
                {"" if book == None else f" Borrowed:- {book.id}.- {book.title}"}
                ****
            ****************"""
    )
