import tkinter as _tk
import tkinter.ttk as _ttk
from datetime import date
import time


from src.shared.screens.home.components.info_card import InfoCard

from src.features.book.presentation.book_screen import BookWrapper
from src.features.student.presentation.student_screen import (
    StudentWrapper,
)


class LibMan(_tk.Tk):
    def __init__(
        self,
        wrappers: tuple[BookWrapper, StudentWrapper],
    ):
        super().__init__()

        self.geometry("1400x800+100+100")
        self.resizable(False, False)
        self.config(
            background="white",
            padx=15,
            pady=15,
        )
        self.wrappers = wrappers

        books = wrappers[0].book_get_all_usecase()
        students = wrappers[1].student_get_all_usecase()

        self.students_len_info = _tk.IntVar(self, len(students))

        self.books_len_info = _tk.IntVar(self, len(books))
        self.borrowed_len_info = _tk.IntVar(
            self,
            len(list(filter(lambda book: book.student_id != None, books))),
        )

        self.data = {
            "students": self.students_len_info,
            "books": self.books_len_info,
            "borrowed": self.borrowed_len_info,
        }

        self.screens = (
            wrappers[0].run(self, self.reset_info),
            wrappers[1].run(self),
            # wrappers[1].run(self, self.reset_info),
        )  # type ignore

        self.add_widgets()

        _ttk.Style(self).configure(  # type: ignore
            ".",
            font=("Arial", 11),
            background="white",
        )

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=25)

        self.columnconfigure(0, weight=1)

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

    def reset_info(self):
        books = self.wrappers[0].book_get_all_usecase()
        students = self.wrappers[1].student_get_all_usecase()

        self.students_len_info.set(len(students))
        self.books_len_info.set(len(books))
        self.borrowed_len_info.set(
           len(list(filter(lambda book: book.student_id != None, books)))
        )
