import tkinter as _tk
import tkinter.ttk as _ttk


from src.features.student.model.student_model import Student

import src.core.widgets.LibFrame as _lib

class StudentTableFrame(_lib.StyledLibFrame):
    def __init__(self, master, students: list[Student]):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.students = students

        self.students_table = _ttk.Treeview(
            self,
            style="StudentTable.Treeview",
            height=1,
            columns=("id", "name", "contact","roll_no"),
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

        self.students_table.heading("contact", text="Contact")
        self.students_table.column(
            "contact",
            stretch=False,
            width=200,
            anchor=_tk.CENTER,
        )

        self.students_table.heading("roll_no", text="Roll No")
        self.students_table.column(
            "roll_no",
            stretch=False,
            width=200,
            anchor=_tk.CENTER,
        )

        for student in self.students:
            self.students_table.insert(
                "",
                _tk.END,
                values=(
                    student.id,
                    student.name,
                    student.contact,
                    student.roll_no,
                    student.book_id,
                ),
            )

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

        for student in self.students:
            self.students_table.insert(
                "",
                _tk.END,
                values=(
                    student.id,
                    student.name,
                    student.contact,
                    student.roll_no,
                    student.book_id,
                ),
            )
