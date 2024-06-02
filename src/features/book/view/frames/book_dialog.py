import tkinter as _tk
import tkinter.ttk as _ttk
import tkinter.messagebox as _msg
from dataclasses import dataclass


# from src.features.book.controller.book_repository import BookRepository

from src.features.student.controller.student_repo import StudentRepository
from src.features.record.controller.record_repository import RecordRepository
from src.features.student.model.student_model import Student


@dataclass
class BookIssueDialogWrapper:
    # student_get_usecase: StudentGetUseCase
    # student_update_record_usecase: UpdateStudentRecordUseCase
    student_repo: StudentRepository
    record_repo: RecordRepository
    # book_repo: BookRepository

    def run(self, master, book_id: str):
        BookIssueDialog(
            master,
            # self.student_get_usecase,
            # self.student_update_record_usecase,
            # self.book_repo,
            self.student_repo,
            self.record_repo,
            book_id,
        )


class BookIssueDialog(_tk.Toplevel):
    def __init__(
        self,
        master,
        # student_get_usecase: StudentGetUseCase,
        # student_update_record_usecase: UpdateStudentRecordUseCase,
        # book_repo: BookRepository,
        student_repo: StudentRepository,
        record_repo: RecordRepository,
        book_id: str,
    ):
        super().__init__(master)
        self.geometry("400x200+200+200")
        self.resizable(False, False)

        self.student_repo = student_repo
        self.record_repo = record_repo

        self.book_id = book_id

        self.result: str | None = None
        self.student: Student | None = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.grab_set()

        self.student_id_var = _tk.StringVar()
        self.student_string = _tk.StringVar()

        self.add_widgets()

        _ttk.Style(self).configure(  # type: ignore
            ".",
            font=("Arial", 11),
            background="white",
        )
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.bind("<Escape>", self.quit)

    def quit(self, event=None):
        self.destroy()

    def add_widgets(self):
        self.base_frame = _ttk.Frame(
            self,
        )
        self.base_frame.grid(
            column=0,
            row=0,
            sticky=_tk.NSEW,
        )
        self.base_frame.columnconfigure(0, weight=1)
        self.base_frame.rowconfigure(0, weight=1)
        self.base_frame.rowconfigure(1, weight=8)

        self._input_menu().grid(
            column=0,
            row=0,
            sticky=_tk.NSEW,
            padx=20,
            pady=(20, 10),
        )

        self._actions_frame().grid(
            column=0, row=1, sticky=_tk.NSEW, padx=20, pady=(0, 20)
        )

    def _actions_frame(self) -> _tk.Widget:
        actions_frame = _ttk.Frame(
            self.base_frame,
        )

        actions_frame.columnconfigure(0, weight=1)
        actions_frame.rowconfigure(0, weight=1)

        _ttk.Label(actions_frame, textvariable=self.student_string, font=("", 14)).grid(
            column=0,
            row=0,
            sticky=_tk.NS,
        )

        self._button_box(actions_frame).grid(
            column=0,
            row=1,
            sticky=_tk.NSEW,
        )

        return actions_frame

    def _input_menu(self) -> _tk.Widget:
        input_frame = _ttk.Frame(self.base_frame)

        input_frame.columnconfigure(0, weight=4)
        input_frame.columnconfigure(1, weight=1)

        input_frame.rowconfigure(0, weight=1)
        input_frame.rowconfigure(1, weight=4)

        _ttk.Label(input_frame, text="Student search", font=("", 12, "bold")).grid(
            column=0,
            row=0,
            sticky=_tk.EW,
            columnspan=2,
        )

        student_id_entry = _ttk.Entry(
            input_frame,
            font=("", 14),
            textvariable=self.student_id_var,
        )
        student_id_entry.grid(
            column=0,
            row=1,
            sticky=_tk.EW,
        )
        student_id_entry.focus_set()

        _ttk.Button(
            input_frame, text="Search", width=10, command=self.search_student
        ).grid(
            column=1,
            row=1,
            sticky=_tk.EW,
        )

        student_id_entry.bind("<Return>", self.search_student)

        for widget in input_frame.winfo_children():
            widget.grid(padx=5, pady=4)

        return input_frame

    def search_student(self, event=None):

        student_id = self.student_id_var.get()

        if not any(ch.isalpha() for ch in student_id):
            res = self.student_repo.findUnique(
                where={"id": self.student_id_var.get(), "roll_no": None}
            )
        else:
            res = self.student_repo.findUnique(
                where={"id": None, "roll_no": self.student_id_var.get()}
            )

        if res == None:
            _msg.showerror(
                "Error",
                f"Student with id: {self.student_id_var.get()} does not exist..",
            )
            return

        self.student = Student.fromTuple(res)

        self.student_string.set(f"Name: {self.student.name}")

        if self.student.book_id == None:
            self.submit_btn["state"] = _tk.NORMAL

        return "break"

    def _button_box(self, master) -> _tk.Widget:
        frame = _ttk.Frame(master)

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        _ttk.Button(
            frame,
            text="Cancel",
            command=self.quit,
            width=20,
        ).grid(
            column=0,
            row=0,
            sticky=_tk.EW,
        )
        self.submit_btn = _ttk.Button(
            frame,
            text="Submit",
            state=_tk.DISABLED,
            width=20,
            command=self.update_result,
        )
        self.submit_btn.grid(
            column=1,
            row=0,
            sticky=_tk.EW,
        )

        for widget in frame.winfo_children():
            widget.grid(padx=5, pady=4)

        return frame

    def update_result(self):
        if self.student == None:
            return

        self.record_repo.create(
            data={
                "student_id": int(self.student.id),
                "book_id": int(self.book_id),
            }
        )
        self.event_generate("<<RefreshTable>>")
        self.event_generate("<<ResetInfo>>")
        self.quit()
