import tkinter as _tk
import tkinter.ttk as _ttk


from src.features.student.domain.usecases import StudentGetAllUseCase


class StudentTableFrame(_ttk.Frame):
    def __init__(self, master, student_get_all_usecase: StudentGetAllUseCase):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.student_get_all_usecase = student_get_all_usecase

        self.students_table = _ttk.Treeview(
            self,
            style="StudentTable.Treeview",
            height=1,
            columns=("id", "name", "phone_no"),
            show="headings",
        )

        self.students_table.grid(column=0, row=0, sticky=_tk.NSEW)

        self.students_table.heading("id", text="Id")
        self.students_table.column(
            "id",
            stretch=False,
            width=50,
            anchor=_tk.CENTER,
        )

        self.students_table.heading("name", text="Name")
        self.students_table.column(
            "name",
        )

        self.students_table.heading("phone_no", text="Contact")
        self.students_table.column(
            "phone_no",
            stretch=False,
            width=200,
            anchor=_tk.CENTER,
        )

        self.students = self.student_get_all_usecase()

        for student in self.students:
            self.students_table.insert("", _tk.END, values=student.to_tuple())

        scrollbar = _ttk.Scrollbar(
            self,
            orient=_tk.VERTICAL,
            command=self.students_table.yview,
        )

        self.students_table.configure(yscrollcommand=scrollbar.set)

        scrollbar.grid(
            column=1,
            row=0,
            sticky=_tk.NS,
        )

        _ttk.Style(self).configure(
            "StudentTable.Treeview",
            rowheight=25,
        )

    def refresh_table(self):
        for item in self.students_table.get_children():
            self.students_table.delete(item)

        for student in self.student_get_all_usecase():
            self.students_table.insert(
                "",
                _tk.END,
                values=student.to_tuple(),
            )
