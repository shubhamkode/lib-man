import tkinter.ttk as _ttk
import tkinter as _tk
from typing import Callable
import src.core.widgets.LibFrame as _lib


class MenuFrame(_lib.StyledLibFrame):
    def __init__(
        self,
        master,
        on_book_add: Callable[[], None] | None = None,
        on_book_update: Callable[[], None] | None = None,
        on_book_delete: Callable[[], None] | None = None,
        on_issue: Callable[[], None] | None = None,
    ):
        super().__init__(master)

        paddings = {"padx": 5, "pady": 4}

        self.add_book_btn = _lib.StyledLibButton(
            self, text="Add Book", width=20, command=lambda: self.handle(on_book_add)
        )
        self.add_book_btn.grid(column=0, row=2, **paddings)
        self.delete_book_btn = _lib.StyledLibButton(
            self,
            text="Delete Book",
            width=20,
            state=_tk.DISABLED,
            command=lambda: self.handle(on_book_delete),
        )
        self.delete_book_btn.grid(column=0, row=4, **paddings)

        self.update_book_btn = _lib.StyledLibButton(
            self,
            text="Update Book",
            width=20,
            state=_tk.DISABLED,
            command=lambda: self.handle(on_book_update),
        )
        self.update_book_btn.grid(column=0, row=3, **paddings)

        _ttk.Separator(self, orient=_tk.HORIZONTAL).grid(
            column=0,
            row=6,
            sticky=_tk.EW,
            pady=8,
        )

        self.issue_btn = _lib.StyledLibButton(
            self,
            text="Issue Book",
            width=20,
            state=_tk.DISABLED,
            command=lambda: on_issue() if on_issue != None else None,
        )
        self.issue_btn.grid(column=0, row=11, **paddings)

    def handle(self, fn: Callable[[], None] | None = None):
        if not fn == None:
            fn()
