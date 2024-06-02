import tkinter as _tk
import tkinter.ttk as _ttk
import tkinter.messagebox as _msg

from typing import Callable
from dataclasses import dataclass

from src.features.student.model.student_model import (
    Student,
    CreateStudentSchema,
    UpdateStudentSchema,
)


class StudentOperationsFrame(_ttk.Frame):
    def __init__(
        self,
        master,
        on_cancel: Callable[[], None] | None,
        on_submit: Callable[[CreateStudentSchema | UpdateStudentSchema], None] | None,
        student: Student | None = None,
    ):
        super().__init__(master)
        self.student: Student | None = student
        self.on_submit = on_submit
        self.on_cancel = on_cancel

        self.name_var = _tk.StringVar(
            self,
            student.name if student != None else "",
        )
        self.contact_var = _tk.StringVar(
            self,
            student.contact if student != None else "",
        )
        self.roll_no_var = _tk.StringVar(
            self,
            student.roll_no if student != None else "",
        )

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        self.rowconfigure(0, weight=1)

        self.config(padding=(10, 40))

        self.add_widgets()

    def add_widgets(self):
        _ttk.Label(
            self,
            text=f"""{"Add" if self.student == None else "Update"} Student:- """,
            font=("Arial", 14, "bold"),
        ).grid(column=0, row=0, sticky=_tk.NE)

        input_frame = _ttk.Frame(self)

        input_frame.grid(column=1, row=0, sticky=_tk.NSEW)

        input_frame.columnconfigure(0, weight=2)
        input_frame.columnconfigure(1, weight=3)

        _ttk.Label(input_frame, text="Enter Name: ").grid(
            column=0,
            row=0,
            pady=5,
            sticky=_tk.E,
        )
        name_entry = _ttk.Entry(
            input_frame,
            textvariable=self.name_var,
            style="StudentOperations.TEntry",
        )
        name_entry.grid(
            column=1,
            row=0,
            columnspan=2,
            sticky=_tk.EW,
        )

        name_entry.focus()

        _ttk.Label(input_frame, text="Enter Contact: ").grid(
            column=0,
            row=1,
            sticky=_tk.E,
        )
        _ttk.Entry(
            input_frame, textvariable=self.contact_var, style="StudentOperations.TEntry"
        ).grid(
            column=1,
            columnspan=2,
            row=1,
            sticky=_tk.EW,
        )

        _ttk.Label(
            input_frame,
            text="Enter Roll No: ",
        ).grid(
            column=0,
            row=2,
            sticky=_tk.E,
        )
        _ttk.Entry(
            input_frame,
            textvariable=self.roll_no_var,
            style="StudentOperations.TEntry",
        ).grid(
            column=1,
            columnspan=2,
            row=2,
            sticky=_tk.EW,
        )

        cancel_btn = _ttk.Button(
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
        submit_btn = _ttk.Button(
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

        _ttk.Style(self).configure("StudentOperations.TEntry", padding="6 4 4 4")

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

    def validate_contact(self) -> bool:
        contact = self.contact_var.get()
        roll_no = self.roll_no_var.get()

        try:
            if self.name_var.get() == "":
                raise StudentException("Name Required")
            if any(ch.isalpha() for ch in contact):
                raise StudentException("Contact must only have numbers")
            if not len(contact) == 10:
                raise StudentException("Contact must be of 10 digits only")
            if not any(ch.isalpha() for ch in roll_no):
                raise StudentException("Roll no must have alphanumeric characters")
        except StudentException as err:
            _msg.showerror("Error", err.message)
            return False
        else:
            return True

    def handle_submit(self):

        if self.on_submit == None:
            return

        if not self.validate_contact():
            return

        if self.student == None:
            self.on_submit(
                CreateStudentSchema(
                    name=self.name_var.get(),
                    contact=self.contact_var.get(),
                    roll_no=self.roll_no_var.get(),
                )
            )

        else:
            self.on_submit(
                UpdateStudentSchema(
                    id=self.student.id,
                    name=self.name_var.get() if self.name_var.get() != "" else None,
                    contact=(
                        self.contact_var.get() if self.contact_var.get() != "" else None
                    ),
                    roll_no=(
                        self.roll_no_var.get() if self.roll_no_var.get() != "" else None
                    ),
                )
            )

    def update_student(self):
        if self.student == None:
            return

        self.name_var.set(self.student.name)
        self.contact_var.set(self.student.contact)
        self.roll_no_var.set(self.student.roll_no)


@dataclass
class StudentException(Exception):
    message: str
