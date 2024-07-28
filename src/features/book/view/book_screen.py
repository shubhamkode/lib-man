import tkinter as _tk
import tkinter.ttk as _ttk
import tkinter.messagebox as _msg


from src.features.book.model.book_model import (
    Book,
    CreateBookSchema,
    UpdateBookSchema,
)


from .frames import (
    BookViewFrame,
    MenuFrame,
    BookOperationsFrame,
    BookIssueDialogWrapper,
)


from src.features.book.controller.book_repository import BookRepository

from dataclasses import dataclass
import src.core.widgets.LibFrame as _lib


@dataclass
class BookWrapper:

    book_repo: BookRepository
    book_issue_dialog_wrapper: BookIssueDialogWrapper

    def run(self, master):  # type: ignore
        return BookScreen(
            master,
            self.book_repo,
            self.book_issue_dialog_wrapper,
        )  # type: ignore


class BookScreen(_lib.StyledLibFrame):
    def __init__(
        self,
        master,
        book_repo: BookRepository,
        book_issue_dialog_wrapper: BookIssueDialogWrapper,
    ):  # type: ignore
        super().__init__(master)

        self.book_repo = book_repo

        self.book_issue_dialog_wrapper = book_issue_dialog_wrapper

        self.columnconfigure(0, weight=7)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=10)
        self.rowconfigure(1, weight=1)

        self.add_widgets()

        self.selected_books: list[Book] = []

        for widget in self.winfo_children():
            widget.grid(padx=5, pady=5)

    def add_widgets(self):
        self.add_table().grid(
            column=0,
            row=0,
            sticky=_tk.NSEW,
        )
        self.add_menu().grid(
            column=1,
            row=0,
            rowspan=2,
            sticky=_tk.NS,
        )

    def add_table(self) -> _tk.Widget:

        self.book_view_frame = BookViewFrame(
            self,
            books=[Book.fromTuple(book) for book in self.book_repo.findMany()],
        )

        self.book_view_frame.books_table.bind(
            "<<TreeviewSelect>>",
            self.select_book,
        )

        return self.book_view_frame

    def add_menu(self) -> _tk.Widget:

        menu_frame = _lib.StyledLibFrame(self)

        menu_frame.rowconfigure(0, weight=1)
        menu_frame.columnconfigure(0, weight=1)

        self.menu_frame = MenuFrame(
            menu_frame,
            on_book_add=self.on_add_book_click,
            on_book_delete=self.on_book_delete,
            on_book_update=self.on_book_update,
            on_issue=self.on_book_issue,
        )
        self.menu_frame.grid(
            column=0,
            row=0,
            sticky=_tk.NS,
            rowspan=4,
        )

        return menu_frame

    def add_operations(self, book: Book | None = None) -> _tk.Widget:

        self.book_operations_frame = BookOperationsFrame(
            self,
            book=book,
            on_cancel=self.on_cancel,
            on_submit=self.on_submit,
        )
        return self.book_operations_frame

    def on_add_book_click(self):

        self.disable_buttons(
            [self.menu_frame.add_book_btn, self.menu_frame.update_book_btn]
        )

        self.add_operations().grid(
            column=0,
            row=1,
            sticky=_tk.NSEW,
        )

    def on_cancel(self):

        self.book_operations_frame.grid_forget()

        self.enable_buttons(buttons=[self.menu_frame.add_book_btn])

        if len(self.selected_books) == 1:
            self.enable_buttons([self.menu_frame.update_book_btn])

    def disable_buttons(self, buttons: list[_tk.Button | _ttk.Button]):
        for button in buttons:
            button["state"] = _tk.DISABLED

    def enable_buttons(self, buttons: list[_tk.Button | _ttk.Button]):
        for button in buttons:
            button["state"] = _tk.NORMAL

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
                    student_id=record[5],
                )
            )

        if len(self.selected_books) >= 1:
            self.enable_buttons([self.menu_frame.delete_book_btn])

        if len(self.selected_books) == 1:
            self.enable_buttons([self.menu_frame.update_book_btn])
            if self.selected_books[0].student_id == "None":
                self.enable_buttons([self.menu_frame.issue_btn])
            else:
                self.disable_buttons([self.menu_frame.issue_btn])
        else:
            self.disable_buttons(
                [self.menu_frame.issue_btn, self.menu_frame.update_book_btn]
            )

        return "break"

    def on_book_delete(self):
        if _msg.askyesno(
            "Are you sure?",
            "Selected books will be deleted. This action cannot be undone.",
        ):
            for book in self.selected_books:
                if book.student_id == "None":
                    self.book_repo.delete(where={"id": book.id})
                else:
                    _msg.showerror(
                        "Error", f"Unable to delete book with book_id: {book.id}"
                    )

        self.refresh_book_table()

        self.selected_books = []

        self.reset_state()

        _msg.showinfo("Delete success", "Books deleted successfully")

    def reset_state(self):
        self.event_generate("<<ResetInfo>>")
        self.enable_buttons(
            [
                self.menu_frame.add_book_btn,
            ]
        )

        if len(self.selected_books) == 1:
            self.enable_buttons(
                [
                    self.menu_frame.update_book_btn,
                    self.menu_frame.issue_btn,
                ]
            )

        else:
            self.disable_buttons(
                [
                    self.menu_frame.update_book_btn,
                    self.menu_frame.issue_btn,
                ]
            )

        if len(self.selected_books) >= 1:
            self.enable_buttons([self.menu_frame.delete_book_btn])
        else:
            self.disable_buttons([self.menu_frame.delete_book_btn])

    def on_submit(self, book: CreateBookSchema | UpdateBookSchema):
        self.book_operations_frame.grid_remove()

        if type(book) == CreateBookSchema:
            self.book_repo.create(
                data={
                    "title": book.title,
                    "author": book.author,
                    "publisher": book.publisher,
                }
            )
            _msg.showinfo("Create success", "Book created successfully")
        elif type(book) == UpdateBookSchema:
            self.book_repo.update(
                where={"id": book.id},
                data={
                    "title": book.title,
                    "author": book.author,
                    "publisher": book.publisher,
                },
            )
            _msg.showinfo("Update success", "Book updated successfully")

        self.refresh_book_table()
        self.reset_state()

    def on_book_update(self):
        self.add_operations(book=self.selected_books[0]).grid(
            column=0,
            row=1,
            sticky=_tk.NSEW,
        )
        self.disable_buttons(
            [self.menu_frame.add_book_btn, self.menu_frame.update_book_btn]
        )

    def on_book_issue(self):
        self.book_issue_dialog_wrapper.run(
            self,
            self.selected_books[0].id,
        )

    def refresh_book_table(self):
        self.book_view_frame.books = [
            Book.fromTuple(book) for book in self.book_repo.findMany()
        ]
        self.book_view_frame.refresh_table()
