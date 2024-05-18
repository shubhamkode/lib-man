from dataclasses import dataclass
from typing import Callable
from src.features.book.domain.usecases import (
    BookCreateUseCase,
    BookGetAllUseCase,
    BookGetUseCase,
    BookUpdateUseCase,
    BookDeleteUseCase,
)


from src.features.student.domain.usecases import StudentGetUseCase

from src.features.book.domain.models.book_model import (
    Book,
    UpdateBookSchema,
    CreateBookSchema,
)

from src.utils.clear_screen import clear_screen
from src.features.student.domain.models.student_model import Student


@dataclass
class BookView:

    book_create_usecase: BookCreateUseCase
    book_get_all_usecase: BookGetAllUseCase
    book_get_usecase: BookGetUseCase
    book_update_usecase: BookUpdateUseCase
    book_delete_usecase: BookDeleteUseCase

    student_get_usecase: StudentGetUseCase

    def run(self):

        options: dict[str, Callable[[], None]] = {
            "Add Book": self.book_create,
            "Display All Books": self.book_get_all,
            "Search Book": self.book_get,
            "Update Book": self.book_update,
            "Delete Book": self.book_delete,
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

    def book_create(self):

        while True:
            clear_screen()
            title = input("Enter Book Title: ")
            author = input("Enter Author: ")
            publisher = input("Enter Publisher: ")

            self.book_create_usecase.run(CreateBookSchema(title, author, publisher))

            print("Book Added Successfully....")

            choice = input("Do you want to continue adding more books? [Yes/No]: ")
            if choice in ["No", "no", "n", "NO"]:
                break
            elif choice in ["YES", "Yes", "yes", "y"]:
                continue
            else:
                print("Invalid Choice..")
                break

    def book_get_all(self):
        clear_screen()
        print_books(self.book_get_all_usecase.run())

    def book_get(self):

        student: Student | None = None

        clear_screen()
        book_id = input("Enter BookId to be searched: ")

        db_book = self.book_get_usecase.run(book_id)

        if db_book == None:
            print(f"No Book Found with Id: {book_id}")
            return

        if db_book.student_id != None:
            student = self.student_get_usecase.run(db_book.student_id)

        print_book(db_book, student)

    def book_update(self):
        clear_screen()
        book_id = input("Enter Book Id: ")

        title = input("Enter Updated Title: ")
        author = input("Enter Updated Author: ")
        publisher = input("Enter Updated Publisher: ")

        self.book_update_usecase.run(
            UpdateBookSchema(
                book_id,
                title if len(title) != 0 else None,
                author if len(author) != 0 else None,
                publisher if len(publisher) != 0 else None,
            )
        )

        print(f"Book with id: {book_id} updated successfully.")

    def book_delete(self):
        clear_screen()
        book_id = input("Enter Book Id: ")
        self.book_delete_usecase.run(book_id)
        print(f"Book with id: {book_id} deleted successfully.")


def print_books(books: list[Book]) -> None:
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


def print_book(book: Book, student: Student | None = None) -> None:
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
