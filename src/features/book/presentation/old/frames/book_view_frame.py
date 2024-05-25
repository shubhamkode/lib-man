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

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.book_get_all_usecase = book_get_all_usecase

        self.books_table = _ttk.Treeview(
            self,
            style="BookTable.Treeview",
            height=1,
            columns=(
                "id",
                "title",
                "author",
                "publisher",
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
            stretch=False,
            width=50,
            anchor=_tk.CENTER,
        )
        self.books_table.heading(
            "title",
            text="Title",
            anchor=_tk.CENTER,
        )
        self.books_table.column(
            "title",
            width=350,
        )
        self.books_table.heading("author", text="Author")
        self.books_table.column(
            "author",
            width=150,
            stretch=False,
            anchor=_tk.CENTER,
        )
        self.books_table.heading("publisher", text="Publisher")
        self.books_table.column(
            "publisher",
            width=150,
            stretch=False,
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

        _ttk.Style(self).configure(
            "BookTable.Treeview",
            rowheight=25,
        )

    def refresh_table(self):
        for item in self.books_table.get_children():
            self.books_table.delete(item)

        for book in self.book_get_all_usecase():
            self.books_table.insert(
                "",
                _tk.END,
                values=book.to_tuple(),
            )
