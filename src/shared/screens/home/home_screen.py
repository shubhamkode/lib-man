import tkinter as _tk
import tkinter.ttk as _ttk
from datetime import date
import time


from src.shared.screens.home.components.info_card import InfoCard

from src.features.book.presentation.book_screen import BookWrapper
from src.features.student.presentation.student_screen import (
    StudentWrapper,
)


from dataclasses import dataclass


@dataclass
class HomeScreenWrapper:
    wrappers: tuple[BookWrapper, StudentWrapper]

    def run(self, master):
        return HomeScreen(master, self)


class HomeScreen(_tk.Frame):
    def __init__(
        self,
        master,
        wrapper: HomeScreenWrapper,
        # wrappers: tuple[BookWrapper, StudentWrapper],
    ):
        super().__init__(master)

        self.config(
            background="white",
            padx=15,
            pady=15,
        )
        self.wrappers = wrapper.wrappers

        books = self.wrappers[0].book_get_all_usecase()
        students = self.wrappers[1].student_get_all_usecase()

        self.students_len_info = _tk.IntVar(self, len(students))

        self.books_len_info = _tk.IntVar(self, len(books))
        self.borrowed_len_info = _tk.IntVar(
            self,
            len(
                list(
                    filter(
                        lambda book: book.student_id != None,
                        books,
                    ),
                )
            ),
        )

        self.data = {
            "students": self.students_len_info,
            "books": self.books_len_info,
            "borrowed": self.borrowed_len_info,
        }

        self.screens = (
            self.wrappers[0].run(self),
            self.wrappers[1].run(self),
            # wrappers[1].run(self, self.reset_info),
        )  # type ignore

        self.bind_all(
            "<<RefreshTable>>",
            self.refresh_table,
        )
        self.bind_all(
            "<<ResetInfo>>",
            self.reset_info,
        )

        self.add_widgets()

        _ttk.Style(self).configure(  # type: ignore
            ".",
            font=("Arial", 11),
            background="white",
        )

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=25)

        self.columnconfigure(0, weight=1)

    def refresh_table(self, event=None):
        self.screens[0].book_view_frame.refresh_table()
        self.screens[1].student_table_frame.refresh_table()

        return "break"

    def add_widgets(self):

        self.time_var = _tk.StringVar(
            self,
            f"""{date.today().strftime("%B %d, %Y")}: {time.strftime("%H:%M", time.localtime())}""",
        )

        main_menu_frame = _ttk.Frame(
            self,
        )
        main_menu_frame.grid(
            column=0,
            row=0,
            sticky=_tk.EW,
        )

        main_menu_frame.columnconfigure(0, weight=1)
        main_menu_frame.columnconfigure(1, weight=1)

        main_menu_frame.rowconfigure(0, weight=1)

        intro_frame = _ttk.Frame(
            main_menu_frame,
        )
        intro_frame.grid(
            column=0,
            row=0,
            sticky=_tk.NSEW,
        )

        _ttk.Label(
            intro_frame,
            text="Hello, Admin!",
            font=("Arial", 20),
        ).grid(
            column=0,
            row=0,
            sticky=_tk.W,
        )
        _ttk.Label(
            intro_frame,
            textvariable=self.time_var,
            font=("Arial", 13),
        ).grid(
            column=0,
            row=1,
            padx=5,
            sticky=_tk.W,
        )

        _ttk.Button(
            main_menu_frame,
            text="Toggle Book/Student",
            command=self.toggle_view,
            width=20,
        ).grid(
            column=1,
            row=0,
            ipady=5,
            sticky=_tk.NE,
        )

        # info-metrics
        info_frame = _tk.Frame(
            main_menu_frame,
            # highlightbackground="blue",
            # highlightthickness=4,
        )

        info_frame.grid(
            column=1,
            row=1,
            pady=5,
            sticky=_tk.EW,
        )

        info_frame.columnconfigure(0, weight=1)
        info_frame.columnconfigure(1, weight=1)
        info_frame.columnconfigure(2, weight=1)
        info_frame.rowconfigure(0, weight=1)

        for index, key in enumerate(self.data.keys()):
            InfoCard(
                info_frame,
                self.data[key],
                key,
            ).grid(
                column=index,
                row=0,
                sticky=_tk.NSEW,
            )

        # operations Frame
        self.screens[0].grid(
            column=0,
            row=1,
            sticky=_tk.NSEW,
        )

        self.after(
            1000 * 60,
            self.update_time,
        )

    def update_time(self):
        self.time_var.set(
            f"""{date.today().strftime("%B %d, %Y")}: {time.strftime("%H:%M", time.localtime())}""",
        )
        self.after(
            1000 * 60,
            self.update_time,
        )

    def toggle_view(self):

        if self.screens[0].winfo_viewable():
            self.screens[0].grid_forget()
            self.screens[1].grid(
                column=0,
                row=1,
                sticky=_tk.NSEW,
            )

        if self.screens[1].winfo_viewable():
            self.screens[1].grid_forget()
            self.screens[0].grid(
                column=0,
                row=1,
                sticky=_tk.NSEW,
            )

    def reset_info(self, event=None):
        books = self.wrappers[0].book_get_all_usecase()
        students = self.wrappers[1].student_get_all_usecase()

        self.students_len_info.set(len(students))
        self.books_len_info.set(len(books))
        self.borrowed_len_info.set(
            len(list(filter(lambda book: book.student_id != None, books)))
        )

        return "break"
