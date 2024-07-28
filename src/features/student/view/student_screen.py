import tkinter as _tk
import tkinter.ttk as _ttk
import tkinter.messagebox as _msg

from dataclasses import dataclass

from .frames import StudentMenuFrame, StudentOperationsFrame, StudentTableFrame


from src.features.student.model.student_model import (
    Student,
    CreateStudentSchema,
    UpdateStudentSchema,
)

from src.features.student.controller.student_repo import StudentRepository
from src.features.record.controller.record_repository import RecordRepository

import src.core.widgets.LibFrame as _lib


@dataclass
class StudentWrapper:

    student_repo: StudentRepository
    record_repo: RecordRepository

    def run(self, master):  # type: ignore
        return StudentScreen(
            master,
            self.record_repo,
            self.student_repo,
        )  # type: ignore


class StudentScreen(_lib.StyledLibFrame):
    def __init__(
        self,
        master,
        record_repo: RecordRepository,
        student_repo: StudentRepository,
    ):  # type: ignore
        super().__init__(master)

        self.student_repo = student_repo
        self.record_repo = record_repo

        self.columnconfigure(0, weight=7)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=5)
        self.rowconfigure(1, weight=1)

        self.add_widgets()

        self.selected_students: list[Student] = []

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

        self.student_table_frame = StudentTableFrame(
            self,
            students=[
                Student.fromTuple(student) for student in self.student_repo.findMany()
            ],
        )

        self.student_table_frame.students_table.bind(
            "<<TreeviewSelect>>",
            self.select_student,
        )

        return self.student_table_frame

    def add_menu(self) -> _tk.Widget:

        self.student_menu_frame = StudentMenuFrame(
            master=self,
            on_student_add=self.on_student_add_click,
            on_student_delete=self.on_student_delete_click,
            on_student_update=self.on_student_update_click,
            on_return=self.on_return_click,
        )

        return self.student_menu_frame

    def add_operations(self, student: Student | None = None) -> _tk.Widget:

        self.student_operations_frame = StudentOperationsFrame(
            self,
            on_cancel=self.on_operations_cancel,
            on_submit=self.on_operations_submit,
            student=student,
        )
        self.student_operations_frame.student = student
        self.student_operations_frame.update_student()

        return self.student_operations_frame

    def on_return_click(self):
        if self.selected_students[0].book_id == None:
            return

        self.record_repo.delete(where={"student_id": int(self.selected_students[0].id)})

        self.event_generate("<<ResetInfo>>")
        self.reset_state()
        self.event_generate("<<RefreshTable>>")

        _msg.showinfo("Success", "Book returned successfully.")

    def on_student_add_click(self):
        self.disable_buttons(
            [self.student_menu_frame.add_btn, self.student_menu_frame.update_btn]
        )
        self.add_operations().grid(
            column=0,
            row=1,
            sticky=_tk.NSEW,
        )

    def on_student_update_click(self):
        self.add_operations(self.selected_students[0]).grid(
            column=0, row=1, sticky=_tk.NSEW
        )

    def on_student_delete_click(self):
        if not (
            _msg.askyesno(
                "Are you sure?",
                "Selected students will be deleted. This action cannot be undone",
            )
        ):
            return
        for student in self.selected_students:
            print(student)
            if student.book_id == "None":
                self.student_repo.delete(where={"id": student.id, "roll_no": None})
            else:
                _msg.showerror(
                    "Error", f"Unable to delete Student with Roll no: {student.roll_no}"
                )

        self.selected_students = []

        self.reset_state()
        self.refresh_students_table()
        self.event_generate("<<ResetInfo>>")

        _msg.showinfo("Delete success", "students deleted successfully")

    def on_operations_submit(self, student: CreateStudentSchema | UpdateStudentSchema):
        self.student_operations_frame.grid_remove()

        if type(student) == CreateStudentSchema:
            self.student_repo.create(
                data={
                    "name": student.name,
                    "contact": student.contact,
                    "roll_no": student.roll_no,
                }
            )
            _msg.showinfo("Create Success", "Student Created Successfully")
        elif type(student) == UpdateStudentSchema:
            self.student_repo.update(
                where={
                    "id": student.id,
                    "roll_no": None,
                },
                data={
                    "name": student.name,
                    "contact": student.contact,
                    "roll_no": student.roll_no,
                },
            )
            _msg.showinfo("Update Success", "Student Updated Successfully")

        self.event_generate("<<ResetInfo>>")
        self.refresh_students_table()
        self.reset_state()

    def on_operations_cancel(self):
        self.student_operations_frame.grid_forget()
        self.reset_state()

    def select_student(self, event):
        self.selected_students = []
        for item in self.student_table_frame.students_table.selection():
            student = self.student_table_frame.students_table.item(item)
            record = student["values"]
            self.selected_students.append(Student.fromTuple(tuple(record)))

        self.reset_state()

        return "break"

    def refresh_students_table(self):
        self.student_table_frame.students = [
            Student.fromTuple(student) for student in self.student_repo.findMany()
        ]
        self.student_table_frame.refresh_table()

    def reset_state(self):

        self.enable_buttons([self.student_menu_frame.add_btn])

        if len(self.selected_students) == 1:
            self.enable_buttons([self.student_menu_frame.update_btn])
            if self.selected_students[0].book_id != "None":
                self.enable_buttons([self.student_menu_frame.return_btn])
            else:
                self.disable_buttons([self.student_menu_frame.return_btn])
        else:
            self.disable_buttons(
                [self.student_menu_frame.update_btn, self.student_menu_frame.return_btn]
            )

        if len(self.selected_students) == 0:
            self.disable_buttons([self.student_menu_frame.delete_btn])
        else:
            self.enable_buttons([self.student_menu_frame.delete_btn])

    def disable_buttons(self, buttons: list[_tk.Button | _ttk.Button]):
        for button in buttons:
            button["state"] = _tk.DISABLED

    def enable_buttons(self, buttons: list[_tk.Button | _ttk.Button]):
        for button in buttons:
            button["state"] = _tk.NORMAL
