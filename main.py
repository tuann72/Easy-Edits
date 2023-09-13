import customtkinter as ctk
from image_widgets import *


class App(ctk.CTk):
    def __init__(self):
        # setup
        super().__init__()
        ctk.set_appearance_mode("Dark")
        self.geometry("1000x600")
        self.title("Easy Edits")
        self.minsize(800, 500)

        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=6)

        # widgets
        # importbutton
        ImageImport(self, self.import_image)

        # run
        self.mainloop()

    def import_image(self, path):
        print(path)


App()
