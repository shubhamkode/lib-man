import tkinter as _tk
from dataclasses import dataclass

from src.shared.screens.home.home_screen import HomeScreenWrapper
from src.features.auth import AuthScreenWrapper


class MainApp(_tk.Tk):
    def __init__(
        self,
        home_screen_wrapper: HomeScreenWrapper,
        auth_screen_wrapper: AuthScreenWrapper,
    ):
        super().__init__()

        self.title("Library Management System")
        self.geometry("1200x600+100+100")
        self.resizable(False, False)

        self.config(background="white", padx=15, pady=15)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.auth_screen = auth_screen_wrapper(self)
        self.auth_screen.grid(
            column=0,
            row=0,
        )

        self.home_screen = home_screen_wrapper.run(self)

        self.bind_all("<<LoginSuccess>>", self.handle_login_success)

    def handle_login_success(self, event=None):
        self.auth_screen.grid_forget()
        self.home_screen.grid(column=0, row=0, sticky=_tk.NSEW)


@dataclass
class MainAppWrapper:
    home_screen_wrapper: HomeScreenWrapper
    auth_screen_wrapper: AuthScreenWrapper

    def run(self) -> MainApp:
        return MainApp(self.home_screen_wrapper, self.auth_screen_wrapper)
