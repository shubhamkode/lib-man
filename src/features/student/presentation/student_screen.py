import tkinter as _tk
import tkinter.ttk as _ttk
import tkinter.messagebox as _msg
import tkinter.simpledialog as _dialog

from dataclasses import dataclass

from .frames import StudentMenuFrame, StudentOperationsFrame, StudentTableFrame

from src.features.student.domain.usecases import (
    StudentGetAllUseCase,
    StudentCreateUseCase,
    StudentUpdateUseCase,
    StudentDeleteUseCase,
    UpdateStudentRecordUseCase,
)

from src.features.book.domain.usecases import BookUpdateRecordUseCase

from typing import Callable
from src.features.student.domain.models.student_model import (
    Student,
    CreateStudentSchema,
    UpdateStudentSchema,
)


@dataclass
class StudentWrapper:

    student_create_usecase: StudentCreateUseCase
    student_get_all_usecase: StudentGetAllUseCase
    student_update_usecase: StudentUpdateUseCase
    student_delete_usecase: StudentDeleteUseCase

    student_update_record_usecase: UpdateStudentRecordUseCase
    book_update_record_usecase: BookUpdateRecordUseCase

    def run(self, master):  # type: ignore
        return StudentScreen(
            master,
            self,
            self.student_create_usecase,
            self.student_get_all_usecase,
            self.student_update_usecase,
            self.student_delete_usecase,
        )  # type: ignore


class StudentScreen(_ttk.Frame):
    def __init__(
        self,
        master,
        wrapper: StudentWrapper,
        student_create_usecase: StudentCreateUseCase,
        student_get_all_usecase: StudentGetAllUseCase,
        student_update_usecase: StudentUpdateUseCase,
        student_delete_usecase: StudentDeleteUseCase,
    ):  # type: ignore
        super().__init__(master)

        self.wrapper = wrapper

        self.student_create_usecase = student_create_usecase
        self.student_get_all_usecase = student_get_all_usecase
        self.student_update_usecase = student_update_usecase
        self.student_delete_usecase = student_delete_usecase

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
        self.add_operations().grid(
            column=0,
            row=1,
            sticky=_tk.NSEW,
        )

    def add_table(self) -> _tk.Widget:

        self.student_table_frame = StudentTableFrame(
            self,
            self.student_get_all_usecase,
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

    def add_operations(self) -> _tk.Widget:
        operations_frame = _ttk.Frame(
            self,
            height=260,
        )

        operations_frame.columnconfigure(0, weight=1)
        operations_frame.rowconfigure(0, weight=1)

        self.student_operations_frame = StudentOperationsFrame(
            operations_frame,
            on_cancel=self.on_operations_cancel,
            on_submit=self.on_operations_submit,
        )

        return operations_frame

    def on_return_click(self):
        if self.selected_students[0].book_id == None:
            return

        self.wrapper.book_update_record_usecase(
            (self.selected_students[0].book_id, None)
        )

        self.wrapper.student_update_record_usecase(
            self.selected_students[0].id,
            None,
        )

        self.event_generate("<<ResetInfo>>")
        self.reset_state()
        self.event_generate("<<RefreshTable>>")

        _msg.showinfo("Success", "Book returned successfully.")

    def on_student_add_click(self):
        self.disable_buttons(
            [self.student_menu_frame.add_btn, self.student_menu_frame.update_btn]
        )
        self.student_operations_frame.grid(column=0, row=0, sticky=_tk.NSEW)

    def on_student_update_click(self):
        self.student_operations_frame.student = self.selected_students[0]
        self.student_operations_frame.update_student()
        self.student_operations_frame.grid(
            column=0,
            row=0,
            sticky=_tk.NSEW,
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
            self.student_delete_usecase(student.id)

        self.selected_students = []

        self.reset_state()
        self.student_table_frame.refresh_table()
        self.event_generate("<<ResetInfo>>")

        _msg.showinfo("Delete success", "students deleted successfully")

    def on_operations_submit(self, student: CreateStudentSchema | UpdateStudentSchema):
        self.student_operations_frame.grid_remove()

        if type(student) == CreateStudentSchema:
            self.student_create_usecase(student)
            _msg.showinfo("Create Success", "Student Created Successfully")
        elif type(student) == UpdateStudentSchema:
            self.student_update_usecase(student)
            _msg.showinfo("Update Success", "Student Updated Successfully")

        self.event_generate("<<ResetInfo>>")
        self.student_table_frame.refresh_table()
        self.reset_state()

    def on_operations_cancel(self):
        self.student_operations_frame.grid_forget()
        self.reset_state()

    def select_student(self, event):
        self.selected_students = []
        for item in self.student_table_frame.students_table.selection():
            student = self.student_table_frame.students_table.item(item)
            record = student["values"]
            self.selected_students.append(
                Student(
                    id=record[0], name=record[1], phone_no=record[2], book_id=record[3]
                )
            )

        self.reset_state()

        return "break"

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
