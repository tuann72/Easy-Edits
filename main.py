import customtkinter as ctk
from image_widgets import *
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter
from menu import Menu


class App(ctk.CTk):
    def __init__(self):
        # setup
        super().__init__()
        ctk.set_appearance_mode("Dark")
        self.geometry("1000x600")
        self.title("Easy Edits")
        self.minsize(800, 500)
        self.init_parameters()

        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform="a")
        self.columnconfigure(1, weight=6, uniform="a")

        # canvas and image data
        self.image_width = 0
        self.image_height = 0
        self.canvas_width = 0
        self.canvas_height = 0

        # widgets
        # importbutton
        self.image_import_btn = ImageImport(self, self.import_image)

        # run
        self.mainloop()

    def init_parameters(self):
        self.pos_vars = {
            "rotate": ctk.DoubleVar(value=ROTATE_DEFAULT),
            "zoom": ctk.DoubleVar(value=ZOOM_DEFAULT),
            "flip": ctk.StringVar(value=FLIP_OPTIONS[0]),
        }

        self.colors_vars = {
            "brightness": ctk.DoubleVar(value=BRIGHTNESS_DEFAULT),
            "grayscale": ctk.BooleanVar(value=GRAYSCALE_DEFAULT),
            "invert": ctk.BooleanVar(value=INVERT_DEFAULT),
            "vibrance": ctk.DoubleVar(value=VIBRANCE_DEFAULT),
        }

        self.effect_vars = {
            "blur": ctk.DoubleVar(value=BLUR_DEFAULT),
            "contrast": ctk.IntVar(value=CONTRAST_DEFAULT),
            "effect": ctk.StringVar(value=EFFECT_OPTIONS[0]),
        }

        # tracing checks if the image changes every time
        for var in (
            list(self.pos_vars.values())
            + list(self.colors_vars.values())
            + list(self.effect_vars.values())
        ):
            var.trace("w", self.manipulate_image)

    def manipulate_image(self, *args):
        self.image = self.orginal

        # rotate
        if self.pos_vars["rotate"].get() != ROTATE_DEFAULT:
            self.image = self.image.rotate(self.pos_vars["rotate"].get())

        # zoom
        if self.pos_vars["zoom"].get() != ZOOM_DEFAULT:
            self.image = ImageOps.crop(
                image=self.image, border=self.pos_vars["zoom"].get()
            )

        # flip
        if self.pos_vars["flip"].get() != FLIP_OPTIONS[0]:
            if self.pos_vars["flip"].get() == "X":
                self.image = ImageOps.mirror(self.image)
            if self.pos_vars["flip"].get() == "Y":
                self.image = ImageOps.flip(self.image)
            if self.pos_vars["flip"].get() == "Both":
                self.image = ImageOps.mirror(self.image)
                self.image = ImageOps.flip(self.image)

        # brightness
        if self.colors_vars["brightness"].get() != BRIGHTNESS_DEFAULT:
            brightness_enhancer = ImageEnhance.Brightness(self.image)
            self.image = brightness_enhancer.enhance(
                self.colors_vars["brightness"].get()
            )

        if self.colors_vars["vibrance"].get() != VIBRANCE_DEFAULT:
            virbrance_enhancer = ImageEnhance.Color(self.image)
            self.image = virbrance_enhancer.enhance(self.colors_vars["vibrance"].get())

        # colors (grayscale/invert)
        if self.colors_vars["grayscale"].get():
            self.image = ImageOps.grayscale(self.image)

        if self.colors_vars["invert"].get():
            self.image = ImageOps.invert(self.image)

        # blurs
        if self.effect_vars["blur"] != BLUR_DEFAULT:
            self.image = self.image.filter(
                ImageFilter.GaussianBlur(self.effect_vars["blur"].get())
            )

        if self.effect_vars["contrast"] != CONTRAST_DEFAULT:
            self.image = self.image.filter(
                ImageFilter.UnsharpMask(self.effect_vars["contrast"].get())
            )

        match self.effect_vars["effect"].get():
            case "Emboss":
                self.image = self.image.filter(ImageFilter.EMBOSS)
            case "Find Edges":
                self.image = self.image.filter(ImageFilter.FIND_EDGES)
            case "Contour":
                self.image = self.image.filter(ImageFilter.CONTOUR)
            case "Edge Enhance":
                self.image = self.image.filter(ImageFilter.EDGE_ENHANCE_MORE)

        self.place_image()

    def import_image(self, path):
        # imports image
        self.orginal = Image.open(path)
        self.image = self.orginal

        # gets the image ratio
        self.image_ratio = self.image.size[0] / self.image.size[1]
        self.image_tk = ImageTk.PhotoImage(self.image)

        # get rid of input btn and display image
        self.image_import_btn.grid_forget()
        self.image_output = ImageOutput(self, self.resize_image)
        self.closed_btn = CloseOutput(self, self.close_edit)
        self.menu = Menu(
            self, self.pos_vars, self.colors_vars, self.effect_vars, self.export_image
        )

    def resize_image(self, event):
        # Current Canvas Ratio
        canvas_ratio = event.width / event.height

        # updating attributes
        self.canvas_width = event.width
        self.canvas_height = event.height

        # Resizing the image
        if canvas_ratio > self.image_ratio:
            self.image_height = int(event.height)
            self.image_width = int(self.image_height * self.image_ratio)
        else:
            self.image_width = int(event.width)
            self.image_height = int(self.image_width / self.image_ratio)

        self.place_image()

    def place_image(self):
        self.image_output.delete("all")

        # setting the new image settings

        resized_image = self.image.resize((self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.image_output.create_image(
            self.canvas_width / 2, self.canvas_height / 2, image=self.image_tk
        )

    def close_edit(self):
        self.image_output.grid_forget()
        self.image_output.place_forget()
        self.menu.grid_forget()
        self.image_import_btn = ImageImport(self, self.import_image)

    def export_image(self, name, file, path):
        export_string = f"{path}/{name}.{file}"
        self.image.save(export_string)


App()
