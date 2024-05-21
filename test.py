# def create_button_frame(root: tk.Tk) -> ttk.Frame:
#     frame = ttk.Frame(root)
#     frame.columnconfigure(0, weight=1)

#     ttk.Button(frame, text="Find Next").grid(column=0, row=0)
#     ttk.Button(frame, text="Replace").grid(column=0, row=1)
#     ttk.Button(frame, text="Replace All").grid(column=0, row=2)
#     ttk.Button(frame, text="Cancel").grid(column=0, row=3)

#     for widget in frame.winfo_children():
#         widget.grid(padx=5, pady=5)

#     return frame


# def create_input_frame(root: tk.Tk) -> ttk.Frame:
#     frame = ttk.Frame(root)
#     frame.columnconfigure(0, weight=1)
#     frame.columnconfigure(0, weight=3)

#     ttk.Label(frame, text="Find what: ").grid(
#         column=0,
#         row=0,
#         sticky=tk.W,
#     )

#     keyword = ttk.Entry(frame, width=30)
#     keyword.focus()
#     keyword.grid(column=1, row=0, sticky=tk.W)

#     ttk.Label(frame, text="Replace with: ").grid(
#         column=0,
#         row=2,
#         sticky=tk.W,
#     )

#     replacement = ttk.Entry(frame, width=30)
#     replacement.grid(column=1, row=2, sticky=tk.W)

#     match_case = tk.StringVar()
#     match_case_check = ttk.Checkbutton(
#         frame,
#         text="Match case",
#         variable=match_case,
#         command=lambda: print(match_case.get()),
#     )
#     match_case_check.grid(column=0, row=2, sticky=tk.W)

#     # Wrap Around checkbox
#     wrap_around = tk.StringVar()
#     wrap_around_check = ttk.Checkbutton(
#         frame,
#         variable=wrap_around,
#         text="Wrap around",
#         command=lambda: print(wrap_around.get()),
#     )
#     wrap_around_check.grid(column=0, row=3, sticky=tk.W)

#     for widget in frame.winfo_children():
#         widget.grid(padx=5, pady=5)

#     return frame


# def create_main_window():
#     root = tk.Tk()
#     root.title("Replace")
#     root.resizable(False, False)

#     try:
#         root.attributes("-toolwindow", True)
#     except TclError:
#         print("Not Supported on your platform")

#     root.columnconfigure(0, weight=4)
#     root.columnconfigure(1, weight=1)

#     create_input_frame(root).grid(column=0, row=0)
#     create_button_frame(root).grid(column=1, row=0)

#     root.mainloop()

import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("300x110")
        self.resizable(False, False)
        self.title("Login")

        paddings = {"padx": 5, "pady": 5}
        entry_font = {"font": ("Helvetica", 11)}

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        username = tk.StringVar()
        password = tk.StringVar()

        ttk.Label(self, text="Username: ").grid(
            column=0,
            row=0,
            sticky=tk.W,
            **paddings,
        )

        ttk.Entry(
            self,
            textvariable=username,
            **entry_font,
        ).grid(
            column=1,
            row=0,
            sticky=tk.E,
            **paddings,
        )

        ttk.Label(self, text="Password: ").grid(
            column=0, row=1, sticky=tk.W, **paddings
        )

        ttk.Entry(
            self,
            textvariable=password,
            show="*",
            **entry_font,
        ).grid(
            column=1,
            row=1,
            sticky=tk.E,
            **paddings,
        )

        ttk.Button(self, text="Login",style="Login.TButton").grid(
            column=1,
            row=3,
            sticky=tk.E,
            **paddings,
        )

        self.style = ttk.Style(self)
        self.style.configure("TLabel", font=("Helvetica", 11))
        self.style.configure("TButton", font=("Helvetica", 11))
        self.style.configure("Login.TButton", font=("Helvetica", 24))


if __name__ == "__main__":
    app = App()
    app.mainloop()