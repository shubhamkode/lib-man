import tkinter as _tk
import tkinter.ttk as _ttk
import tkinter.messagebox as _msg
import re

from dataclasses import dataclass

from src.utils.exceptions import AuthException


class AuthScreenWrapper:
    def __call__(self, master):
        return AuthScreen(master)


class AuthScreen(_ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)

        self.message = "Login Success."

        self.email_var = _tk.StringVar()
        self.password_var = _tk.StringVar()

        _ttk.Label(self, text="Email").grid(
            column=0,
            row=0,
            sticky=_tk.W,
        )
        _ttk.Entry(
            self,
            font=("", 14),
            textvariable=self.email_var,
        ).grid(column=0, row=1, pady=(2, 10))
        _ttk.Label(self, text="Password").grid(
            column=0,
            row=2,
            sticky=_tk.W,
        )
        _ttk.Entry(
            self,
            font=("", 14),
            textvariable=self.password_var,
        ).grid(
            column=0,
            row=4,
            pady=(2, 10),
        )

        login_button = _ttk.Button(
            self,
            text="Submit",
            command=self.handle_submit,
        )
        login_button.grid(column=0, row=5, ipady=4, pady=(10, 0), sticky=_tk.EW)

        login_button.bind(
            "<Return>",
            self.handle_submit,
        )

    # def validate_

    def handle_submit(self, event=None):

        email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

        try:
            if not re.fullmatch(email_regex, self.email_var.get()):
                raise AuthException("Email Address not valid...")

            if (
                self.email_var.get() == ""
                or not self.email_var.get() == "admin@admin.com"
            ):
                raise AuthException("email address not linked with any admin...")

            if self.password_var.get() == "":
                raise AuthException("Password Required")

            if not self.password_var.get() == "admin":
                raise AuthException("Invalid Password")

        except AuthException as err:
            _msg.showerror("Error", err.message)

        else:
            self.event_generate("<<LoginSuccess>>")

        return "break"
