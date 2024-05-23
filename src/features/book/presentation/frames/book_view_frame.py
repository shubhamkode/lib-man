import tkinter as _tk
import tkinter.ttk as _ttk

from src.features.book.domain.usecases import BookGetAllUseCase


class BookViewFrame(_ttk.Frame):
    def __init__(
        self,
        master,
        book_get_all_usecase: BookGetAllUseCase,
    ):
        super().__init__(master)

        self.book_get_all_usecase = book_get_all_usecase

        self.books_table = _ttk.Treeview(
            self,
            columns=(
                "id",
                "title",
                "author",
                "publisher",
                "status",
            ),
            show="headings",
        )

        self.books_table.grid(
            column=0,
            row=0,
            sticky=_tk.NSEW,
        )

        self.books_table.heading("id", text="Id")
        self.books_table.column(
            "id",
            width=50,
            anchor=_tk.CENTER,
        )
        self.books_table.heading("title", text="Title")
        self.books_table.column(
            "title",
            width=350,
            stretch=True,
        )
        self.books_table.heading("author", text="Author")
        self.books_table.column(
            "author",
            width=150,
            anchor=_tk.CENTER,
        )
        self.books_table.heading("publisher", text="Publisher")
        self.books_table.column(
            "publisher",
            width=150,
            anchor=_tk.CENTER,
        )
        self.books_table.heading("status", text="Status")
        self.books_table.column(
            "status",
            width=100,
            anchor=_tk.CENTER,
        )

        self.books = self.book_get_all_usecase()

        for book in filter(lambda book: book.student_id == None, self.books):
            self.books_table.insert(
                "",
                _tk.END,
                values=book.to_tuple(),
            )

        scrollbar = _ttk.Scrollbar(
            self,
            orient=_tk.VERTICAL,
            command=self.books_table.yview,  # type: ignore
        )

        self.books_table.configure(  # type: ignore
            yscroll=scrollbar.set,
        )
        scrollbar.grid(
            column=1,
            row=0,
            sticky=_tk.NS,
        )

        for widget in self.winfo_children():
            widget.grid(padx=5, pady=10)

    def refresh_table(self):
        for item in self.books_table.get_children():
            self.books_table.delete(item)

        for book in self.book_get_all_usecase():
            self.books_table.insert(
                "",
                _tk.END,
                values=book.to_tuple(),
            )
