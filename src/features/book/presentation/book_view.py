from dataclasses import dataclass
from typing import List, Optional
from src.features.book.domain.usecases import (
    CreateNewBookUseCase,
    CreateBookSchema,
    GetAllBooksUseCase,
    DeleteBookByIdUseCase,
    GetBookByIdUseCase,
    UpdateBookByIdUseCase,
)

from src.features.student.domain.usecases import GetStudentByIdUseCase

from src.features.book.domain.models.book_model import Book, UpdateBookSchema

from src.utils.clear_screen import clear_screen
from src.features.student.domain.models.student_model import Student


@dataclass
class BookView:
    create_new_book_usecase: CreateNewBookUseCase
    get_all_books_usecase: GetAllBooksUseCase
    get_book_by_id_usecase: GetBookByIdUseCase
    update_book_by_id_usecase: UpdateBookByIdUseCase
    delete_book_by_id_usecase: DeleteBookByIdUseCase
    get_student_by_id_usecase: GetStudentByIdUseCase

    def run(self):
        options = [
            ["Add Book", self.add_book],
            ["Display All Books", self.display_all_books],
            # ["Display available Books", self.display_available_books],
            ["Search Book", self.search_book],
            ["Update Book", self.update_book],
            ["Delete Book", self.delete_book],
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

    def display_all_books(self):
        clear_screen()
        books = self.get_all_books_usecase.run()
        print_books(books)

    def add_book(self):
        while True:
            clear_screen()
            title = input("Enter Book Title: ")
            author = input("Enter Author: ")
            publisher = input("Enter Publisher: ")

            self.create_new_book_usecase.run(
                CreateBookSchema(title=title, author=author, publisher=publisher)
            )

            print("Book Added Successfully....")

            choice = input("Do you want to continue adding more books? [Yes/No]: ")
            if choice in ["No", "no", "n", "NO"]:
                break
            elif choice in ["YES", "Yes", "yes", "y"]:
                continue
            else:
                print("Invalid Choice..")
                break

        return

    def delete_book(self):
        clear_screen()
        book_id = input("Enter Book Id: ")
        self.delete_book_by_id_usecase.run(book_id)
        print(f"Book with id: {book_id} deleted successfully.")

    def search_book(self):
        clear_screen()
        book_id = input("Enter BookId to be searched: ")

        book = self.get_book_by_id_usecase.run(book_id)

        if book == None:
            print(f"No Book Found with Id: {book_id}")
            return

        if book.student_id == None:
            print_book(book, None)
        else:
            student = self.get_student_by_id_usecase.run(book.student_id)
            print_book(book, student)

    def update_book(self):
        clear_screen()
        book_id = input("Enter Book Id: ")

        title = input("Enter Updated Title: ")
        author = input("Enter Updated Author: ")
        publisher = input("Enter Updated Publisher: ")

        self.update_book_by_id_usecase.run(
            book_id,
            UpdateBookSchema(
                title if len(title) != 0 else None,
                author if len(author) != 0 else None,
                publisher if len(publisher) != 0 else None,
            ),
        )
        print(f"Book with id: {book_id} updated successfully.")


def print_books(books: List[Book]) -> None:
    for book in books:
        print(
            f"""
            ****************
                id: {book.id}
                Title: {book.title}
                Author: {book.author}
                Publisher: {book.publisher}
                Status: {book.status()}
            ****************"""
        )


def print_book(book: Book, student: Optional[Student]) -> None:
    print(
        f"""
            ****************
                id: {book.id}
                Title: {book.title}
                Author: {book.author}
                Publisher: {book.publisher}
                Status: {book.status()}
                ****
                    {"" if student == None else f" Borrowed by: {student.id}.- {student.name} "}
                ****
            ****************"""
    )
