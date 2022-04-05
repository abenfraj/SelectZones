import time
from tkinter import *
from tkinter import ttk
import tkinter.filedialog
import tkinter.messagebox

import PIL
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

PIL.Image.MAX_IMAGE_PIXELS = None


def main():
    # Set size to fullscreen
    # root: root window
    def setSizeToScreen(root):
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight() - 20
        root.geometry('%dx%d+-10+0' % (w, h))

    # Choose BMP file from file explorer
    # root: root window
    def chooseAndDisplayFileFromFileExplorer():
        path = tkinter.filedialog.askopenfilename(filetypes=[("BMP files", "*.bmp")])
        displayBMP(path)

    # Choose BMP file from file explorer
    # root: root window
    def displayBMP(path_of_image_to_display):
        print(path_of_image_to_display)
        root.iconbitmap(path_of_image_to_display)
        plt.imshow(Image.open(path_of_image_to_display))
        print("image displayed")

    root = Tk()
    root.title("SELECTZONES")
    setSizeToScreen(root)

    frm = ttk.Frame(root)
    frm.grid()

    ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=1)

    path = "null"
    ttk.Button(frm, text="Choose File", command=lambda: chooseAndDisplayFileFromFileExplorer()).grid(
        column=0, row=2)
    root.mainloop()


main()
