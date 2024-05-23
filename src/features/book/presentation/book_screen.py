import tkinter as _tk
import tkinter.ttk as _ttk

from src.features.book.presentation.frames import (
    BookViewFrame,
    BookOperationsFrame,
    MenuFrame,
)

from src.features.book.presentation.frames.student.student_operations_frame import (
    StudentOperationsFrame,
)


from src.features.book.domain.usecases import (
    BookGetAllUseCase,
    BookDeleteUseCase,
    BookCreateUseCase,
    BookUpdateUseCase,
)
from src.features.book.domain.models.book_model import (
    Book,
    CreateBookSchema,
    UpdateBookSchema,
)

from src.features.student.domain.models.student_model import (
    CreateStudentSchema,
    UpdateStudentSchema,
)


from src.features.book.presentation.frames.student.student_view_frame import (
    StudentViewFrame,
)

from src.features.student.domain.usecases import (
    StudentGetAllUseCase,
    StudentCreateUseCase,
    StudentUpdateUseCase,
)


class BookScreen(_tk.Tk):
    def __init__(
        self,
        book_get_all_usecase: BookGetAllUseCase,
        book_delete_usecase: BookDeleteUseCase,
        book_create_usecase: BookCreateUseCase,
        book_update_usecase: BookUpdateUseCase,
        student_get_all_usecase: StudentGetAllUseCase,
        student_create_usecase: StudentCreateUseCase,
        student_update_usecase: StudentUpdateUseCase,
    ):

        super().__init__()

        self.book_create_usecase = book_create_usecase
        self.book_get_all_usecase = book_get_all_usecase
        self.book_update_usecase = book_update_usecase
        self.book_delete_usecase = book_delete_usecase

        self.student_create_usecase = student_create_usecase
        self.student_get_all_usecase = student_get_all_usecase
        self.student_update_usecase = student_update_usecase

        self.title("LibMan - Dashboard")
        # self.geometry("900x600+100+100") widthxheight
        self.geometry("1100x600+100+100")
        self.resizable(False, False)
        self.configure(background="white")

        self.selected_books: list[Book] = []

        self.create_widgets()

        _ttk.Style(self).configure(
            ".",
            font=("Helvetica", 11),
            background="white",
        )

    def create_widgets(self):

        paddings = {"padx": 5, "pady": 2}

        self.frame = _ttk.Frame(
            self,
        )

        self.frame.grid(
            column=0,
            row=0,
            sticky=_tk.NSEW,
            pady=20,
            padx=20,
        )

        self.frame.columnconfigure(0, weight=4)
        self.frame.columnconfigure(1, weight=1)

        _ttk.Label(
            self.frame,
            text="Welcome admin! ",
            font=(("Helvetica", 15, "bold")),
        ).grid(column=0, row=0, sticky=_tk.W, pady=(10, 20))
        # Student View Frame
        self.student_view_frame = StudentViewFrame(
            self.frame,
            student_get_all_usecase=self.student_get_all_usecase,
        )

        self.student_view_frame.grid(
            column=0, row=1, columnspan=4, sticky=_tk.NSEW, **paddings
        )

        self.student_view_frame.grid_remove()

        # Adding Book View Frame
        self.book_view_frame = BookViewFrame(
            self.frame,
            book_get_all_usecase=self.book_get_all_usecase,
        )

        self.book_view_frame.books_table.bind(
            "<<TreeviewSelect>>",
            self.select_book,  # type: ignore
        )

        self.book_view_frame.grid(
            column=0,
            row=1,
            columnspan=4,
            sticky=_tk.NSEW,
            **paddings,
            # padx=20,
            # pady=20,
        )

        self.menu_frame = MenuFrame(
            self.frame,
            on_toggle=self.toggle_table,
            on_book_add=self.show_add_book_dialog,
            on_book_update=self.update_book,
            on_book_delete=self.delete_books,
            on_issue=self.issue_book,
            on_student_add=self.on_student_add,
        )
        self.menu_frame.grid(
            column=4,
            row=1,
            rowspan=2,
            **paddings,
            sticky=_tk.NS,
        )

    def on_student_add(self):

        self.menu_frame.student_add_btn["state"] = _tk.DISABLED

        self.student_operations_frame = StudentOperationsFrame(
            self.frame,
            on_submit=self.handle_student_operations_submit,
            on_cancel=self.destroy_student_operations,
        )

        self.student_operations_frame.grid(
            column=0,
            row=2,
            stick=_tk.NSEW,
            padx=20,
            pady=10,
        )

    def destroy_student_operations(self):

        self.student_operations_frame.destroy()
        self.menu_frame.student_add_btn["state"] = _tk.NORMAL
        self.menu_frame.student_update_btn["state"] = _tk.DISABLED

    def handle_student_operations_submit(
        self,
        student: CreateStudentSchema | UpdateStudentSchema,
    ):
        if type(student) == CreateStudentSchema:
            self.student_create_usecase(student)
        elif type(student) == UpdateStudentSchema:
            self.student_update_usecase(student)


        self.destroy_student_operations()
        self.student_view_frame.refresh_table()

    def toggle_table(self):
        self.selected_books = []

        if self.book_view_frame.winfo_viewable():
            self.book_view_frame.grid_remove()
            self.student_view_frame.grid()

        if self.student_view_frame.winfo_viewable():
            self.student_view_frame.grid_remove()
            self.book_view_frame.grid()

    def select_book(self, event):
        self.selected_books = []
        for item in self.book_view_frame.books_table.selection():
            book = self.book_view_frame.books_table.item(item)
            record = book["values"]
            self.selected_books.append(
                Book(
                    id=record[0],
                    title=record[1],
                    author=record[2],
                    publisher=record[3],
                )
            )
        self.menu_frame.delete_book_btn["state"] = (
            _tk.NORMAL if len(self.selected_books) >= 1 else _tk.DISABLED
        )

        if len(self.selected_books) == 1:
            self.menu_frame.issue_btn["state"] = _tk.NORMAL
            self.menu_frame.update_btn["state"] = _tk.NORMAL
        else:
            self.menu_frame.issue_btn["state"] = _tk.DISABLED
            self.menu_frame.update_btn["state"] = _tk.DISABLED

    def delete_books(self):
        for book in self.selected_books:
            self.book_delete_usecase(book.id)

        self.book_view_frame.refresh_table()

    def show_add_book_dialog(self):

        self.menu_frame.add_book_btn["state"] = _tk.DISABLED

        self.book_operations_frame = BookOperationsFrame(
            self.frame,
            on_cancel=self.destroy_book_operations_frame,
            on_submit=self.handle_book_operations_submit,
        )

        self.book_operations_frame.grid(
            column=0,
            row=2,
            stick=_tk.NSEW,
            padx=20,
            pady=10,
        )

    def handle_book_operations_submit(
        self,
        book: CreateBookSchema | UpdateBookSchema,
    ):
        if type(book) == CreateBookSchema:
            self.book_create_usecase(book)
        elif type(book) == UpdateBookSchema:
            self.book_update_usecase(book)

        self.destroy_book_operations_frame()
        self.book_view_frame.refresh_table()

    def destroy_book_operations_frame(self):
        self.book_operations_frame.grid_forget()
        self.menu_frame.add_book_btn["state"] = _tk.NORMAL
        self.menu_frame.update_btn["state"] = _tk.NORMAL

    def update_book(self):
        self.menu_frame.add_book_btn["state"] = _tk.DISABLED
        self.menu_frame.update_btn["state"] = _tk.DISABLED

        self.book_operations_frame = BookOperationsFrame(
            self.frame,
            book=self.selected_books[0],
            on_cancel=self.destroy_book_operations_frame,
            on_submit=self.handle_book_operations_submit,
        )

        self.book_operations_frame.grid(
            column=0,
            row=2,
            stick=_tk.NSEW,
            padx=20,
            pady=10,
        )
