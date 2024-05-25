import tkinter as _tk
import tkinter.ttk as _ttk

class InfoCard(_ttk.Frame):
    def __init__(
        self,
        master,  # type: ignore
        value: _tk.IntVar,
        tag: str,
    ):
        super().__init__(master)

        self.value = value
        self.tag = tag
        # self.config(highlightbackground="blue",highlightthickness=4,)

        self.columnconfigure(0, weight=1)

        _ttk.Label(
            self,
            textvariable=self.value,
            anchor="center",
            padding=5,
            font=("Helvetica", 25, "bold"),
        ).grid(
            column=0,
            row=0,
            sticky=_tk.NSEW,
        )
        _ttk.Label(
            self,
            text=self.tag.capitalize(),
            anchor="center",
            font=("Helvetica", 14),
        ).grid(
            column=0,
            row=1,
            sticky=_tk.EW,
        )
