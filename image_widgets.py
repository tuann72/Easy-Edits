import customtkinter as ctk
from tkinter import filedialog, Canvas
from settings import *


class ImageImport(ctk.CTkFrame):
    def __init__(self, parent, import_function):
        super().__init__(master=parent)
        self.grid(column=0, columnspan=2, row=0, sticky="nsew")
        self.import_function = import_function

        ctk.CTkButton(self, text="Open Image", command=self.open_dialog).pack(
            expand=True
        )

    def open_dialog(self):
        path = filedialog.askopenfile().name
        self.import_function(path)


class ImageOutput(Canvas):
    def __init__(self, parent, resize_function):
        super().__init__(
            master=parent,
            background=BACKGROUND_COLOR,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        self.grid(row=0, column=1, sticky="nsew")
        self.bind("<Configure>", resize_function)
