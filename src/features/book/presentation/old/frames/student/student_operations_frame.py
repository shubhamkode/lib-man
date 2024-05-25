import tkinter.ttk as _ttk
import tkinter as _tk
from typing import Callable

from src.features.student.domain.models.student_model import (
    Student,
    UpdateStudentSchema,
    CreateStudentSchema,
)


class StudentOperationsFrame(_ttk.Frame):
    def __init__(
        self,
        master,
        student: Student | None = None,
        on_submit: (
            Callable[[UpdateStudentSchema | CreateStudentSchema], None] | None
        ) = None,
        on_cancel: Callable[[], None] | None = None,
    ):
        super().__init__(master)

        self.student = student
        self.on_submit = on_submit
        self.on_cancel = on_cancel

        self.name_var = _tk.StringVar(self, student.name if student != None else "")
        self.phone_no_var = _tk.StringVar(
            self, student.phone_no if student != None else ""
        )

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=2)

        _ttk.Label(self, text="Add Student:- ").grid(
            column=0,
            row=0,
        )

        # Title
        _ttk.Label(self, text="Enter Name: ").grid(
            column=1,
            row=1,
            pady=5,
            sticky=_tk.W,
        )
        _ttk.Entry(self, textvariable=self.name_var).grid(
            column=2,
            row=1,
            columnspan=2,
            sticky=_tk.EW,
        )

        _ttk.Label(self, text="Enter Contact: ").grid(
            column=1,
            row=2,
            sticky=_tk.W,
        )
        _ttk.Entry(
            self,
            textvariable=self.phone_no_var,
        ).grid(
            column=2,
            columnspan=2,
            row=2,
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

        # TODO:- Add Input Validation

        if self.student == None:
            self.on_submit(
                CreateStudentSchema(
                    name=self.name_var.get(),
                    phone_no=self.phone_no_var.get(),
                )
            )

        else:
            self.on_submit(
                UpdateStudentSchema(
                    id=self.student.id,
                    name=self.name_var.get() if self.name_var.get() != "" else None,
                    phone_no=(
                        self.phone_no_var.get()
                        if self.phone_no_var.get() != ""
                        else None
                    ),
                )
            )
