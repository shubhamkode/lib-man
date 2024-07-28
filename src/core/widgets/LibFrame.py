import tkinter.ttk as _ttk

from typing import TypedDict, Literal

from ..colors import APP_THEME


class LibFrame(_ttk.Frame):
    def __init__(self, master, bg: str | None, **kwargs):
        super().__init__(master, style="LibFrame.TFrame", **kwargs)
        _ttk.Style().configure(
            style="LibFrame.TFrame",
            background=bg,
        )


class LibLabel(_ttk.Label):
    def __init__(self, master, bg: str | None, color: str | None, **kwargs):
        super().__init__(master, style="Label.TLabel", **kwargs)
        _ttk.Style().configure(
            style="Label.TLabel",
            background=bg,
            foreground=color,
        )


class LibEntryStyle(TypedDict):
    bg: str | None
    color: str | None
    p: str | None


class LibEntry(_ttk.Entry):
    def __init__(self, master, tw_style: LibEntryStyle, **kwargs):
        super().__init__(master, style="Entry.TEntry", **kwargs)
        _ttk.Style().configure(
            style="Entry.TEntry",
            fieldbackground=tw_style.get("bg"),
            foreground=tw_style.get("color"),
            padding=tw_style.get("p"),
        )


class LibButtonStyle(TypedDict):
    bg: str | None = None
    color: str | None = None




class LibButton(_ttk.Button):
    def __init__(self, master, tw_style: LibButtonStyle, **kwargs):
        super().__init__(master, style="Button.TButton", **kwargs)
        _ttk.Style().configure(
            style="Button.TButton",
            background=tw_style.get("bg"),
            foreground=tw_style.get("color"),
        )


class StyledLibFrame(LibFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=APP_THEME["surface"], **kwargs)


class StyledLibEntry(LibEntry):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            tw_style={
                "p": "6 4 4 4",
                "bg": APP_THEME["surfaceVariant"],
                "color": APP_THEME["onSurfaceVariant"],
            },
            **kwargs,
        )


class StyledLibLabel(LibLabel):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            bg=APP_THEME["surface"],
            color=APP_THEME["onSurface"],
            **kwargs,
        )



class StyledLibButton(LibButton):
    def __init__(
        self,
        master,
        **kwargs
    ):
        super().__init__(
            master,
            tw_style={"bg": APP_THEME["primary"],"color":APP_THEME["onPrimary"]},
            **kwargs,
        )
