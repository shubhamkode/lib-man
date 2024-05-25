import tkinter as _tk
import tkinter.ttk as _ttk
import tkinter.messagebox as _msg
import tkinter.simpledialog as _dialog

from src.features.book.domain.usecases import (
    BookGetAllUseCase,
    BookCreateUseCase,
    BookUpdateUseCase,
    BookDeleteUseCase,
)
from typing import Callable

from src.features.book.domain.models.book_model import (
    Book,
    CreateBookSchema,
    UpdateBookSchema,
)

from src.features.book.presentation.old.frames.book_view_frame import BookViewFrame

from src.features.book.presentation.old.frames.menu_frame import MenuFrame

from src.features.book.presentation.old.frames.book_operations_frame import (
    BookOperationsFrame,
)

from dataclasses import dataclass


@dataclass
class BookWrapper:

    book_create_usecase: BookCreateUseCase
    book_get_all_usecase: BookGetAllUseCase
    book_update_usecase: BookUpdateUseCase
    book_delete_usecase: BookDeleteUseCase

    def run(self, master, reset_info: Callable[[], None]):  # type: ignore
        return BookScreen(
            master,
            self.book_create_usecase,
            self.book_get_all_usecase,
            self.book_update_usecase,
            self.book_delete_usecase,
            reset_info,
        )  # type: ignore


class BookScreen(_ttk.Frame):
    def __init__(
        self,
        master,
        book_create_usecase: BookCreateUseCase,
        book_get_all_usecase: BookGetAllUseCase,
        book_update_usecase: BookUpdateUseCase,
        book_delete_usecase: BookDeleteUseCase,
        reset_info: Callable[[], None],
    ):  # type: ignore
        super().__init__(master)

        self.book_create_usecase = book_create_usecase
        self.book_get_all_usecase = book_get_all_usecase
        self.book_update_usecase = book_update_usecase
        self.book_delete_usecase = book_delete_usecase

        self.reset_info = reset_info

        self.columnconfigure(0, weight=7)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=5)
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
        self.add_operations().grid(
            column=0,
            row=1,
            sticky=_tk.NSEW,
        )

    def add_table(self) -> _tk.Widget:

        self.book_view_frame = BookViewFrame(
            self,
            self.book_get_all_usecase,
        )

        self.book_view_frame.books_table.bind(
            "<<TreeviewSelect>>",
            self.select_book,
        )

        return self.book_view_frame

    def add_menu(self) -> _tk.Widget:

        menu_frame = _ttk.Frame(self)

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

    def add_operations(self) -> _tk.Widget:
        operations_frame = _ttk.Frame(
            self,
            height=260,
        )

        operations_frame.columnconfigure(0, weight=1)
        operations_frame.rowconfigure(0, weight=1)

        self.book_operations_frame = BookOperationsFrame(
            operations_frame,
            on_cancel=self.on_cancel,
            on_submit=self.on_submit,
        )

        return operations_frame

    def on_add_book_click(self):

        self.disable_buttons(
            [self.menu_frame.add_book_btn, self.menu_frame.update_book_btn]
        )

        self.book_operations_frame.grid(
            column=0,
            row=0,
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
                )
            )

        if len(self.selected_books) >= 1:
            self.enable_buttons([self.menu_frame.delete_book_btn])

        if len(self.selected_books) == 1:
            self.enable_buttons(
                [self.menu_frame.issue_btn, self.menu_frame.update_book_btn]
            )
        else:
            self.disable_buttons(
                [self.menu_frame.issue_btn, self.menu_frame.update_book_btn]
            )

    def on_book_delete(self):
        if _msg.askyesno(
            "Are you sure?",
            "Selected books will be deleted. This action cannot be undone.",
        ):
            for book in self.selected_books:
                self.book_delete_usecase(book.id)

        self.book_view_frame.refresh_table()

        self.selected_books = []

        self.reset_state()

        _msg.showinfo("Delete success", "Books deleted successfully")

    def reset_state(self):
        self.reset_info()
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
            self.book_create_usecase(book)
            _msg.showinfo("Create success", "Book created successfully")
        elif type(book) == UpdateBookSchema:
            self.book_update_usecase(book)
            _msg.showinfo("Update success", "Book updated successfully")

        self.book_view_frame.refresh_table()
        self.reset_state()

    def on_book_update(self):
        self.book_operations_frame.book = self.selected_books[0]
        self.book_operations_frame.add_book()
        self.book_operations_frame.grid(
            column=0,
            row=0,
            sticky=_tk.NSEW,
        )

    def on_book_issue(self):
        # print(_("Student Details", "Enter Student Id: "))
        print(CustomDialog().result)
        # print(_dialog.askinteger("Enter StudentId: ", "StudentId "))


class CustomDialog(_tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.geometry("500x300+200+200")
        self.resizable(False, False)

        self.result = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.add_widgets()

        _ttk.Style(self).configure(".", background="white")

    def add_widgets(self):
        self.base_frame = _tk.Frame(
            self,
            highlightbackground="blue",
            highlightthickness=4,
        ).grid(
            column=0,
            row=0,
            sticky=_tk.NSEW,
        )

        self._button_box().grid(column=0, row=0, sticky=_tk.EW)

    def _button_box(self) -> _tk.Widget:
        frame = _tk.Frame(
            self.base_frame,
            highlightbackground="blue",
            highlightthickness=4,
        )

        return frame
