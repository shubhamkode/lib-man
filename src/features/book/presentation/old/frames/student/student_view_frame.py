import tkinter as _tk
import tkinter.ttk as _ttk

from src.features.student.domain.usecases import StudentGetAllUseCase


class StudentViewFrame(_ttk.Frame):
    def __init__(
        self,
        master,
        student_get_all_usecase: StudentGetAllUseCase,
    ):
        super().__init__(master)

        self.student_get_all_usecase = student_get_all_usecase

        self.table = _ttk.Treeview(
            self,
            columns=(
                "id",
                "name",
                "phone_no",
                "book_issued",
            ),
            show="headings",
        )

        self.table.grid(
            column=0,
            row=0,
            sticky=_tk.NSEW,
        )

        self.table.heading("id", text="Id")
        self.table.column(
            "id",
            width=50,
            anchor=_tk.CENTER,
        )
        self.table.heading("name", text="Name")
        self.table.column(
            "name",
            width=400,
        )
        self.table.heading(
            "phone_no",
            text="Contact",
        )
        self.table.column(
            "phone_no",
            width=200,
            anchor=_tk.CENTER,
        )
        self.table.heading("book_issued", text="Book Id")
        self.table.column(
            "book_issued",
            width=150,
            anchor=_tk.CENTER,
        )

        self.students = self.student_get_all_usecase()

        for student in self.students:
            self.table.insert("", _tk.END, values=student.to_tuple())

        scrollbar = _ttk.Scrollbar(
            self,
            orient=_tk.VERTICAL,
            command=self.table.yview,  # type: ignore
        )

        self.table.configure(  # type: ignore
            yscroll=scrollbar.set,
        )
        scrollbar.grid(
            column=1,
            row=0,
            sticky=_tk.NS,
        )

        for widget in self.winfo_children():
            widget.grid(padx=5, pady=10)

    def refresh_table(self):
        for item in self.table.get_children():
            self.table.delete(item)

        for student in self.student_get_all_usecase():
            self.table.insert(
                "",
                _tk.END,
                values=student.to_tuple(),
            )
