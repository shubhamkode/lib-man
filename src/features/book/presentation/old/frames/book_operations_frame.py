import tkinter.ttk as _ttk
import tkinter as _tk
import tkinter.messagebox as _msg
from typing import Callable
from src.features.book.domain.models.book_model import (
    Book,
    CreateBookSchema,
    UpdateBookSchema,
)

from dataclasses import dataclass


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
        self.columnconfigure(1, weight=4)
        self.rowconfigure(0, weight=1)
        # self.columnconfigure(2, weight=2)

        self.config(padding=(10, 10))

        _ttk.Label(
            self,
            text=f"""{"Add" if self.book == None else "Update"} Book:- """,
            font=("Arial", 14, "bold"),
        ).grid(
            column=0,
            row=0,
            sticky=_tk.NE,
        )

        input_frame = _ttk.Frame(
            self,
        )
        input_frame.grid(
            column=1,
            row=0,
            sticky=_tk.NSEW,
        )

        input_frame.columnconfigure(0, weight=2)
        input_frame.columnconfigure(1, weight=3)

        # Title
        _ttk.Label(input_frame, text="Enter Title: ").grid(
            column=0,
            row=0,
            pady=5,
            sticky=_tk.E,
        )

        _ttk.Entry(
            input_frame,
            textvariable=self.title_var,
            width=30,
        ).grid(
            column=1,
            row=0,
            columnspan=2,
            sticky=_tk.EW,
        )

        _ttk.Label(input_frame, text="Enter Author: ").grid(
            column=0,
            row=1,
            sticky=_tk.E,
        )
        _ttk.Entry(
            input_frame,
            textvariable=self.author_var,
        ).grid(
            column=1,
            columnspan=2,
            row=1,
            sticky=_tk.EW,
        )
        _ttk.Label(input_frame, text="Enter Publisher: ").grid(
            column=0,
            row=2,
            sticky=_tk.E,
        )
        _ttk.Entry(input_frame, textvariable=self.publisher_var).grid(
            column=1,
            columnspan=2,
            row=2,
            sticky=_tk.EW,
        )

        _ttk.Button(
            input_frame,
            text="Cancel",
            command=lambda: self.on_cancel() if self.on_cancel != None else None,
            width=20,
        ).grid(
            column=1,
            row=3,
            sticky=_tk.E,
        )
        _ttk.Button(
            input_frame,
            text="Submit",
            width=20,
            command=self.handle_submit,
        ).grid(
            column=2,
            row=3,
            sticky=_tk.W,
        )

        for widget in self.winfo_children():
            widget.grid(
                padx=5,
                pady=5,
            )
        for widget in input_frame.winfo_children():
            widget.grid(
                padx=20,
                pady=10,
            )

    def validate_book(self) -> bool:
        title = self.title_var.get()
        author = self.author_var.get()
        publisher = self.publisher_var.get()

        try:
            if title == "":
                raise BookException("Title cannot be empty")

            if any(ch.isdigit() for ch in author):
                raise BookException("Author name cannot have a number")

            if any(ch.isdigit() for ch in publisher):
                raise BookException("Publisher name cannot have a number")

        except BookException as err:
            _msg.showerror("Error", err.message)
            return False
        else:
            return True

    def handle_submit(self):

        if self.on_submit == None:
            return

        if not self.validate_book():
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

    def add_book(
        self,
    ):
        if self.book == None:
            return
        self.title_var.set(self.book.title)
        self.author_var.set(self.book.author)
        self.publisher_var.set(self.book.publisher)


@dataclass
class BookException(Exception):
    message: str
