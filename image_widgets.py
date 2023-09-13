import customtkinter as ctk


class ImageImport(ctk.CTkFrame):
    def __init__(self, parent, import_function):
        super().__init__(master=parent)
        self.grid(column=0, columnspan=2, row=0, sticky="nsew")
        self.import_function = import_function

        ctk.CTkButton(self, text="Open Image", command=self.open_dialog).pack(
            expand=True
        )

    def open_dialog(self):
        path = "test"
        self.import_function(path)
