import tkinter.ttk as _ttk
import tkinter as _tk
from typing import Callable

import src.core.widgets.LibFrame as _lib


class StudentMenuFrame(_lib.StyledLibFrame):
    def __init__(
        self,
        master,
        on_student_add: Callable[[], None] | None = None,
        on_student_update: Callable[[], None] | None = None,
        on_student_delete: Callable[[], None] | None = None,
        on_return: Callable[[], None] | None = None,
    ):
        super().__init__(master)

        paddings = {"padx": 5, "pady": 4}

        self.add_btn = _lib.StyledLibButton(
            self,
            text="Add Student",
            width=20,
            command=lambda: self.handle(on_student_add),
        )
        self.add_btn.grid(column=0, row=2, **paddings)

        self.delete_btn = _lib.StyledLibButton(
            self,
            text="Delete Student",
            width=20,
            state=_tk.DISABLED,
            command=lambda: self.handle(on_student_delete),
        )
        self.delete_btn.grid(column=0, row=4, **paddings)

        self.update_btn = _lib.StyledLibButton(
            self,
            text="Update Student",
            width=20,
            state=_tk.DISABLED,
            command=lambda: self.handle(on_student_update),
        )
        self.update_btn.grid(column=0, row=3, **paddings)

        _ttk.Separator(self, orient=_tk.HORIZONTAL).grid(
            column=0,
            row=6,
            sticky=_tk.EW,
            pady=8,
        )

        self.return_btn = _lib.StyledLibButton(
            self,
            text="Return Book",
            width=20,
            state=_tk.DISABLED,
            command=lambda: self.handle(on_return),
        )
        self.return_btn.grid(column=0, row=11, **paddings)

    def handle(self, fn: Callable[[], None] | None = None):
        if not fn == None:
            fn()
