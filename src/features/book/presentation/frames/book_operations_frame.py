import tkinter.ttk as _ttk
import tkinter as _tk
from typing import Callable
from src.features.book.domain.models.book_model import (
    Book,
    CreateBookSchema,
    UpdateBookSchema,
)


class BookOperationsFrame(_ttk.Frame):
    def __init__(
        self,
        master,
        book: Book | None = None,
        on_submit: Callable[[CreateBookSchema | UpdateBookSchema], None] | None = None,
        on_cancel: Callable[[], None] | None = None,
    ):
        super().__init__(master)

        self.book = book
        self.on_submit = on_submit
        self.on_cancel = on_cancel

        self.title_var = _tk.StringVar(self, book.title if book != None else "")
        self.author_var = _tk.StringVar(self, book.author if book != None else "")
        self.publisher_var = _tk.StringVar(self, book.publisher if book != None else "")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=2)

        _ttk.Label(self, text="Add Book:- ").grid(
            column=0,
            row=0,
        )

        # Title
        _ttk.Label(self, text="Enter Title: ").grid(
            column=1,
            row=1,
            pady=5,
            sticky=_tk.W,
        )
        _ttk.Entry(self, textvariable=self.title_var).grid(
            column=2,
            row=1,
            columnspan=2,
            sticky=_tk.EW,
        )

        _ttk.Label(self, text="Enter Author: ").grid(
            column=1,
            row=2,
            sticky=_tk.W,
        )
        _ttk.Entry(
            self,
            textvariable=self.author_var,
        ).grid(
            column=2,
            columnspan=2,
            row=2,
            sticky=_tk.EW,
        )
        _ttk.Label(self, text="Enter Publisher: ").grid(
            column=1,
            row=3,
            sticky=_tk.W,
        )
        _ttk.Entry(self, textvariable=self.publisher_var).grid(
            column=2,
            columnspan=2,
            row=3,
            sticky=_tk.EW,
        )

        _ttk.Button(
            self,
            text="Cancel",
            command=lambda: self.on_cancel() if self.on_cancel != None else None,
        ).grid(
            column=3,
            row=4,
            sticky=_tk.EW,
        )

        _ttk.Button(self, text="Submit", command=self.handle_submit).grid(
            column=4,
            row=4,
            sticky=_tk.EW,
        )

        for widget in self.winfo_children():
            widget.grid(
                padx=5,
                pady=10,
            )

    def handle_submit(self):

        if self.on_submit == None:
            return

        if self.book == None:
            self.on_submit(
                CreateBookSchema(
                    title=self.title_var.get(),
                    author=self.author_var.get(),
                    publisher=self.publisher_var.get(),
                )
            )

        else:
            self.on_submit(
                UpdateBookSchema(
                    id=self.book.id,
                    title=self.title_var.get() if self.title_var.get() != "" else None,
                    author=(
                        self.author_var.get() if self.author_var.get() != "" else None
                    ),
                    publisher=(
                        self.publisher_var.get()
                        if self.publisher_var.get() != ""
                        else None
                    ),
                )
            )
