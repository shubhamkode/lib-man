import tkinter as _tk
import tkinter.ttk as _ttk
import tkinter.messagebox as _msg
import tkinter.commondialog as _commondialog


from src.features.book.domain.usecases import (
    BookGetAllUseCase,
    BookDeleteUseCase,
    BookCreateUseCase,
)
from src.features.book.domain.models.book_model import Book, CreateBookSchema


class BookScreen(_tk.Tk):
    def __init__(
        self,
        book_get_all_usecase: BookGetAllUseCase,
        book_delete_usecase: BookDeleteUseCase,
        book_create_usecase: BookCreateUseCase,
    ):

        super().__init__()

        self.book_get_all_usecase = book_get_all_usecase
        self.book_delete_usecase = book_delete_usecase
        self.book_create_usecase = book_create_usecase

        self.title("Book Management Screen")
        # self.geometry("900x600+100+100") widthxheight
        self.geometry("1100x600+100+100")
        self.resizable(False, False)
        self.configure(background="white")

        self.selected_books: list[Book] = []
        self.add_book

        # self.columnconfigure(0, weight=1)
        # self.rowconfigure(0, weight=1)

        self.create_widgets()

        _ttk.Style(self).configure(
            ".",
            font=("Helvetica", 11),
            background="white",
        )

    def create_widgets(self):

        frame = _ttk.Frame(self)

        frame.grid(
            column=0,
            row=0,
            sticky=_tk.NSEW,
            pady=30,
            padx=20,
        )

        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=4)

        _ttk.Label(
            frame,
            text="Welcome, Admin",
            font=(("Helvetica", 15, "bold")),
        ).grid(
            row=0,
            column=0,
            sticky=_tk.W,
        )

        self.book_table = _ttk.Treeview(
            frame,
            columns=(
                "id",
                "title",
                "author",
                "publisher",
            ),
            show="headings",
        )

        self.book_table.heading("id", text="Id")
        self.book_table.heading("title", text="Title")
        self.book_table.heading("author", text="Author")
        self.book_table.heading("publisher", text="Publisher")

        for book in self.book_get_all_usecase():
            self.book_table.insert("", _tk.END, values=book.to_tuple())

        # book_table scrollbar
        scrollbar = _ttk.Scrollbar(
            frame,
            orient=_tk.VERTICAL,
            command=self.book_table.yview,
        )

        self.book_table.configure(
            yscroll=scrollbar.set,
        )
        scrollbar.grid(
            column=1,
            row=1,
            sticky=_tk.NS,
        )

        self.book_table.bind(
            "<<TreeviewSelect>>",
            self.select_book,
        )
        self.book_table.grid(
            column=0,
            row=1,
            sticky=_tk.EW,
            padx=20,
            pady=20,
        )

        self.add_book_frame = _ttk.Frame(frame)

        # Buttons
        frame2 = _ttk.Frame(
            self,
        )
        frame2.grid(
            column=1,
            row=0,
            pady=20,
        )

        self.add_book_button = _ttk.Button(
            frame2,
            text="Add book",
            width=20,
            command=self.show_add_book_dialog,
        )

        self.add_book_button.grid(
            row=0,
            column=0,
        )

        self.delete_button = _ttk.Button(
            frame2,
            text="Delete Book",
            width=20,
            state=_tk.DISABLED,
            command=self.delete_books,
        )
        self.delete_button.grid(
            row=1,
            column=0,
        )

        for widget in frame.winfo_children():
            widget.grid(padx=5, pady=10)

        for widget in frame2.winfo_children():
            widget.grid(padx=5, pady=3)

    def select_book(self, event):
        self.selected_books = []
        for item in self.book_table.selection():
            book = self.book_table.item(item)
            record = book["values"]
            self.selected_books.append(
                Book(
                    id=record[0],
                    title=record[1],
                    author=record[2],
                    publisher=record[3],
                )
            )
            self.delete_button["state"] = _tk.NORMAL

    def delete_books(self):
        for book in self.selected_books:
            self.book_delete_usecase(book.id)

        self.delete_button["state"] = _tk.DISABLED

        self.refresh_table()

    def show_add_book_dialog(self):

        self.add_book_button["state"] = _tk.DISABLED

        title = _tk.StringVar()
        author = _tk.StringVar()
        publisher = _tk.StringVar()

        self.add_book_frame.columnconfigure(0, weight=1)
        self.add_book_frame.columnconfigure(1, weight=1)
        self.add_book_frame.columnconfigure(2, weight=4)

        _ttk.Label(self.add_book_frame, text="Add Book:- ").grid(
            column=0,
            row=0,
        )

        _ttk.Label(self.add_book_frame, text="Enter Book Title: ").grid(
            column=1,
            row=1,
            pady=5,
            sticky=_tk.W,
        )
        _ttk.Entry(self.add_book_frame, textvariable=title).grid(
            column=2, row=1, sticky=_tk.EW
        )

        _ttk.Label(self.add_book_frame, text="Enter Book Author").grid(
            column=1,
            row=2,
            sticky=_tk.W,
        )
        _ttk.Entry(self.add_book_frame, textvariable=author).grid(
            column=2, row=2, sticky=_tk.EW
        )
        _ttk.Label(self.add_book_frame, text="Enter Book Publisher").grid(
            column=1,
            row=3,
            sticky=_tk.W,
        )
        _ttk.Entry(self.add_book_frame, textvariable=publisher).grid(
            column=2,
            row=3,
            sticky=_tk.EW,
        )

        _ttk.Button(
            self.add_book_frame,
            text="Cancel",
            command=self.destroy_add_book_frame,
        ).grid(
            column=3,
            row=4,
            sticky=_tk.EW,
        )

        _ttk.Button(
            self.add_book_frame,
            text="Submit",
            command=lambda: self.add_book(
                new_book=CreateBookSchema(
                    title=title.get(),
                    author=author.get(),
                    publisher=publisher.get(),
                )
            ),
        ).grid(
            column=4,
            row=4,
            sticky=_tk.EW,
        )

        self.add_book_frame.grid(
            column=0,
            row=2,
            sticky=_tk.EW,
        )

        for widget in self.add_book_frame.winfo_children():
            widget.grid(
                padx=5,
                pady=10,
            )

    def add_book(self, new_book: CreateBookSchema):
        if new_book.title == "" or new_book.author == "" or new_book.publisher == "":
            _msg.showerror(
                "Input Error",
                "All Fields are Required",
            )
            return
        self.book_create_usecase(new_book)
        self.refresh_table()

        self.destroy_add_book_frame()

    def refresh_table(self):
        for item in self.book_table.get_children():
            self.book_table.delete(item)

        for book in self.book_get_all_usecase():
            self.book_table.insert("", _tk.END, values=book.to_tuple())

    def destroy_add_book_frame(self):
        self.add_book_frame.grid_forget()
        self.add_book_button["state"] = _tk.NORMAL
