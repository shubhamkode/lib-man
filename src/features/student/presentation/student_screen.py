import tkinter as _tk
import tkinter.ttk as _ttk

from dataclasses import dataclass

from src.features.student.domain.usecases import StudentGetAllUseCase


@dataclass
class StudentWrapper:
    student_get_all_usecase: StudentGetAllUseCase

    def run(self, master):  # type: ignore
        return StudentScreen(master)  # type: ignore


class StudentScreen(_tk.Frame):
    def __init__(
        self,
        master,  # type: ignore
    ):
        super().__init__(master)

        self.configure(highlightcolor="blue", highlightthickness=4)

        _ttk.Label(self, text="Student Screen").grid(column=0, row=0)
