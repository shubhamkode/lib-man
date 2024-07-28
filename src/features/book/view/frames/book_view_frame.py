import tkinter as _tk
import tkinter.ttk as _ttk

import src.core.widgets.LibFrame as _lib

from src.features.book.model.book_model import Book


class BookViewFrame(_lib.StyledLibFrame):
    def __init__(self, master, books: list[Book] = []):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.books: list[Book] = books

        self.books_table = _ttk.Treeview(
            self,
            style="BookTable.Treeview",
            height=1,
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
        self.books_table.heading("status", text="Status")
        self.books_table.column(
            "status",
            width=150,
            stretch=False,
            anchor=_tk.CENTER,
        )

        for book in self.books:
            self.books_table.insert(
                "",
                _tk.END,
                values=(
                    book.id,
                    book.title,
                    book.author,
                    book.publisher,
                    "AVAILABLE" if book.student_id == None else "BORROWED",
                    book.student_id,
                ),
            )

        scrollbar = _ttk.Scrollbar(
            self,
            orient=_tk.VERTICAL,
            command=self.books_table.yview,  # type: ignore
        )

        self.books_table.configure(  # type: ignore
            yscrollcommand=scrollbar.set,
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

        for book in self.books:
            self.books_table.insert(
                "",
                _tk.END,
                values=(
                    book.id,
                    book.title,
                    book.author,
                    book.publisher,
                    "AVAILABLE" if book.student_id == None else "BORROWED",
                    book.student_id,
                ),
            )
