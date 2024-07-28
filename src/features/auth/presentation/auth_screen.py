import tkinter as _tk
import tkinter.messagebox as _msg
import re


from src.utils import AuthException

import src.core.widgets.LibFrame as _lib


class AuthScreenWrapper:
    def __call__(self, master):
        return AuthScreen(master)


class AuthScreen(_lib.StyledLibFrame):
    def __init__(self, master):
        super().__init__(
            master,
        )

        # Remove

        self.columnconfigure(0, weight=1)

        self.message = "Login Success."

        self.email_var = _tk.StringVar()
        self.password_var = _tk.StringVar()

        _lib.StyledLibLabel(
            self,
            text="Welcome Back!",
            font=("", 16, "bold"),
        ).grid(
            column=0,
            row=0,
            pady=(0, 16),
            sticky=_tk.W,
        )

        _lib.StyledLibLabel(self, text="Email").grid(
            column=0,
            row=1,
            sticky=_tk.W,
        )
        _lib.StyledLibEntry(
            self,
            font=("", 12),
            width=30,
            textvariable=self.email_var,
        ).grid(
            column=0,
            row=2,
            pady=(4, 12),
            sticky=_tk.EW,
        )
        _lib.StyledLibLabel(
            self,
            text="Password",
        ).grid(
            column=0,
            row=3,
            sticky=_tk.W,
        )
        _lib.StyledLibEntry(
            self,
            font=("", 12),
            textvariable=self.password_var,
        ).grid(
            column=0,
            row=4,
            pady=(4, 12),
            sticky=_tk.EW,
        )

        login_button = _lib.StyledLibButton(
            self,
            text="Submit",
            command=self.handle_submit,
        )
        login_button.grid(
            column=0,
            row=5,
            ipady=4,
            pady=(4, 0),
            sticky=_tk.EW,
        )

        login_button.bind(
            "<Return>",
            self.handle_submit,
        )

        # _ttk.Style(self).configure("Auth.TEntry", padding="6 4 4 4")

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
