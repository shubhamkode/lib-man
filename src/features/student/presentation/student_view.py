from dataclasses import dataclass
from typing import List, Optional

from src.features.student.domain.usecases import (
    CreateNewStudentUseCase,
    GetAllStudentsUseCase,
    GetStudentByIdUseCase,
    UpdateStudentByIdUseCase,
    DeleteStudentByIdUseCase,
)

from src.features.book.domain.usecases import GetBookByIdUseCase

from src.features.student.domain.models.student_model import (
    Student,
    CreateStudentSchema,
    UpdateStudentSchema,
)

from src.features.book.domain.models.book_model import Book

from src.utils.clear_screen import clear_screen


@dataclass
class StudentView:
    create_new_student_usecase: CreateNewStudentUseCase
    get_all_students_usecase: GetAllStudentsUseCase
    get_student_by_id_usecase: GetStudentByIdUseCase
    update_student_by_id_usecase: UpdateStudentByIdUseCase
    delete_student_by_id_usecase: DeleteStudentByIdUseCase

    get_book_by_id_usecase: GetBookByIdUseCase

    def run(self):
        options = [
            ["Add Student", self.add_student],
            ["Display All Students", self.display_all_students],
            ["Search Student", self.search_student],
            ["Update Student", self.update_student],
            ["Delete Student", self.delete_student],
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

    def add_student(self):
        while True:
            clear_screen()
            name = input("Enter Student Name: ")
            phone_no = input("Enter Student Phone No: ")

            self.create_new_student_usecase.run(CreateStudentSchema(name, phone_no))

            print("Student Added Successfully....")

            choice = input("Do you want to continue adding more students? [Yes/No]: ")
            if choice in ["No", "no", "n", "NO"]:
                break
            elif choice in ["YES", "Yes", "yes", "y"]:
                continue
            else:
                print("Invalid Choice..")
                break

        return

    def display_all_students(self):
        clear_screen()
        print_students(self.get_all_students_usecase.run())

    def search_student(self):
        book = None
        student_id = input("Enter student Id: ")

        student = self.get_student_by_id_usecase.run(student_id)

        if student == None:
            print(f"No Student found with Id: {student_id}")
            return

        if student.book_id != None:
            book = self.get_book_by_id_usecase.run(student.book_id)

        clear_screen()
        print_student(student, book)

    def update_student(self):

        clear_screen()
        student_id = input("Enter Student Id: ")

        name = input("Enter Updated Name: ")
        phone_no = input("Enter Updated Phone No: ")

        self.update_student_by_id_usecase.run(
            student_id,
            UpdateStudentSchema(
                name if (len(name)) != 0 else None,
                phone_no if len(phone_no) != 0 else None,
            ),
        )

        print(f"Student with id: {student_id} updated successfully.")

    def delete_student(self):

        clear_screen()
        student_id = input("Enter Student Id: ")
        self.delete_student_by_id_usecase.run(student_id)
        print(f"Student with id: {student_id} deleted successfully..")


def print_students(students: List[Student]) -> None:
    for student in students:
        print(
            f"""
            ****************
                id: {student.id}
                Name: {student.name}
                Phone No: {student.phone_no}
            ****************"""
        )


def print_student(student: Student, book: Optional[Book]):
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

    # {"" if student == None else f" Borrowed by: {student.id}.- {student.name} "}
