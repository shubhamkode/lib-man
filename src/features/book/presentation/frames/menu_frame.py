import tkinter.ttk as _ttk
import tkinter as _tk
from typing import Callable


class MenuFrame(_ttk.Frame):
    def __init__(
        self,
        master,
        on_toggle: Callable[[], None] | None = None,
        on_book_add: Callable[[], None] | None = None,
        on_book_update: Callable[[], None] | None = None,
        on_book_delete: Callable[[], None] | None = None,
        on_issue: Callable[[], None] | None = None,
        on_student_add: Callable[[], None] | None = None,
    ):
        super().__init__(master)

        paddings = {"padx": 5, "pady": 4}

        self.toggle_view = _ttk.Button(
            self,
            text="Toggle Student/Book",
            width=20,
            command=lambda: self.handle(on_toggle)
        )
        self.toggle_view.grid(
            column=0,
            row=0,
            **paddings,
        )

        _ttk.Separator(self, orient=_tk.HORIZONTAL).grid(
            column=0,
            row=1,
            sticky=_tk.EW,
            pady=8,
        )

        self.add_book_btn = _ttk.Button(
            self,
            text="Add Book",
            width=20,
            command=lambda: self.handle(on_book_add)
        )
        self.add_book_btn.grid(column=0, row=2, **paddings)
        self.delete_book_btn = _ttk.Button(
            self,
            text="Delete Book",
            width=20,
            state=_tk.DISABLED,
            command=lambda: self.handle(on_book_delete)
        )
        self.delete_book_btn.grid(column=0, row=4, **paddings)

        self.update_btn = _ttk.Button(
            self,
            text="Update Book",
            width=20,
            state=_tk.DISABLED,
            command=lambda: self.handle(on_book_update)
        )
        self.update_btn.grid(column=0, row=3, **paddings)

        _ttk.Separator(self, orient=_tk.HORIZONTAL).grid(
            column=0,
            row=6,
            sticky=_tk.EW,
            pady=8,
        )

        self.student_add_btn = _ttk.Button(
            self,
            text="Add Student",
            width=20,
            command=lambda: self.handle(on_student_add)
        )
        self.student_add_btn.grid(column=0, row=7, **paddings)

        self.student_update_btn = _ttk.Button(
            self,
            text="Update Student",
            state=_tk.DISABLED,
            width=20,
            # command=lambda: on_issue() if on_issue != None else None,
        )
        self.student_update_btn.grid(column=0, row=8, **paddings)

        self.student_delete_btn = _ttk.Button(
            self,
            text="Delete Student",
            state=_tk.DISABLED,
            width=20,
            # command=lambda: on_issue() if on_issue != None else None,
        )
        self.student_delete_btn.grid(column=0, row=9, **paddings)

        _ttk.Separator(self, orient=_tk.HORIZONTAL).grid(
            column=0,
            row=10,
            sticky=_tk.EW,
            pady=8,
        )

        self.issue_btn = _ttk.Button(
            self,
            text="Issue Book",
            width=20,
            state=_tk.DISABLED,
            command=lambda: on_issue() if on_issue != None else None,
        )
        self.issue_btn.grid(column=0, row=11, **paddings)

        self.book_return_btn = _ttk.Button(
            self,
            text="Return Book",
            width=20,
            state=_tk.DISABLED,
            command=lambda: on_issue() if on_issue != None else None,
        )
        self.book_return_btn.grid(column=0, row=12, **paddings)

    def handle(self, fn: Callable[[], None] | None = None):
        if not fn == None:
            fn()
