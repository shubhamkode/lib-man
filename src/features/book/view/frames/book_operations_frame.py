import tkinter.ttk as _ttk
import tkinter as _tk
import tkinter.messagebox as _msg
from typing import Callable
from src.features.book.model.book_model import (
    Book,
    CreateBookSchema,
    UpdateBookSchema,
)

from dataclasses import dataclass
import src.core.widgets.LibFrame as _lib


class BookOperationsFrame(_lib.StyledLibFrame):
    def __init__(
        self,
        master,
        book: Book | None = None,
        on_submit: Callable[[CreateBookSchema | UpdateBookSchema], None] | None = None,
        on_cancel: Callable[[], str | None] | None = None,
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

        self.config(padding=(10, 10))

        _lib.StyledLibLabel(
            self,
            text=f"""{"Add" if self.book == None else "Update"} Book:- """,
            font=("Arial", 14, "bold"),
        ).grid(
            column=0,
            row=0,
            sticky=_tk.NE,
        )

        input_frame = _lib.StyledLibFrame(
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
        _lib.StyledLibLabel(input_frame, text="Enter Title: ").grid(
            column=0,
            row=0,
            pady=5,
            sticky=_tk.E,
        )

        title_entry = _lib.StyledLibEntry(
            input_frame,
            textvariable=self.title_var,
            width=30,
        )
        title_entry.grid(
            column=1,
            row=0,
            columnspan=2,
            sticky=_tk.EW,
        )

        title_entry.focus()

        _lib.StyledLibLabel(input_frame, text="Enter Author: ").grid(
            column=0,
            row=1,
            sticky=_tk.E,
        )
        _lib.StyledLibEntry(
            input_frame,
            textvariable=self.author_var,
        ).grid(
            column=1,
            columnspan=2,
            row=1,
            sticky=_tk.EW,
        )
        _lib.StyledLibLabel(input_frame, text="Enter Publisher: ").grid(
            column=0,
            row=2,
            sticky=_tk.E,
        )
        _lib.StyledLibEntry(
            input_frame,
            textvariable=self.publisher_var,
        ).grid(
            column=1,
            columnspan=2,
            row=2,
            sticky=_tk.EW,
        )

        cancel_btn = _lib.StyledLibButton(
            input_frame,
            text="Cancel",
            command=lambda: self.on_cancel() if self.on_cancel != None else None,
            width=20,
        )
        cancel_btn.grid(
            column=1,
            row=3,
            sticky=_tk.E,
        )
        submit_btn = _lib.StyledLibButton(
            input_frame,
            text="Submit",
            width=20,
            command=self.handle_submit,
        )
        submit_btn.grid(
            column=2,
            row=3,
            sticky=_tk.W,
        )

        cancel_btn.bind(
            "<Return>",
            lambda event: self.on_cancel() if self.on_cancel != None else None,
        )
        submit_btn.bind(
            "<Return>",
            lambda event: self.handle_submit(),
        )


        for widget in self.winfo_children():
            widget.grid(
                padx=5,
                pady=5,
            )
        for widget in input_frame.winfo_children():
            widget.grid(
                padx=20,
                pady=5,
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


@dataclass
class BookException(Exception):
    message: str
