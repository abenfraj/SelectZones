from tkinter import *
from tkinter import ttk
import tkinter.filedialog
import tkinter.messagebox
from PyQt5 import QtWidgets
import PIL
from PIL import Image, ImageTk

PIL.Image.MAX_IMAGE_PIXELS = None

###############################################################################
# GLOBAL VARIABLES
bitmap_to_display = None  # The bitmap to display after being loaded


###############################################################################


# Set size to fullscreen
def setSizeToScreen():
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight() - 20
    root.geometry('%dx%d+-10+0' % (w, h))


# Choose BMP file from file explorer and directly display it
def chooseAndDisplayFileFromFileExplorer():
    path = tkinter.filedialog.askopenfilename(filetypes=[("BMP files", "*.bmp"), ("All files", "*.*")])
    displayBMP(path)


# Choose BMP file from file explorer
# bitmap_path: path of BMP file
def displayBMP(bitmap_path):
    global bitmap_to_display
    bitmap_to_display = ImageTk.PhotoImage(Image.open(bitmap_path))
    bmp_label = Label(initial_frame, image=bitmap_to_display)
    bmp_label.pack()
    print("bitmap displayed with path: " + bitmap_path)


###############################################################################
# ROOT WINDOW CONFIGURATION
root = Tk()  # Create a root window
root.title("SELECT ZONES")  # Set window title
# TODO root.iconbitmap("path")  # Set window icon
setSizeToScreen()  # Set size to fullscreen
###############################################################################

initial_frame = ttk.Frame(root)  # Create a frame
canvas = Canvas(initial_frame)  # Create a canvas
vertical_bitmap_scrollbar = Scrollbar(
    initial_frame, orient="vertical", command=canvas.yview)  # Create a vertical scrollbar for the bitmap
horizontal_bitmap_scrollbar = Scrollbar(
    initial_frame, orient="horizontal", command=canvas.xview)  # Create a horizontal scrollbar for the bitmap

scrollable_frame = ttk.Frame(canvas)  # Create a scrollable frame
scrollable_frame.bind(  # Bind scrollable frame to scrollbar
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=vertical_bitmap_scrollbar.set)
canvas.configure(xscrollcommand=horizontal_bitmap_scrollbar.set)

Label(initial_frame, text="Hello World!").pack()
Button(initial_frame, text="Quit", command=root.destroy).pack()
Button(
    initial_frame,
    text="Choose BMP file in explorer",
    command=chooseAndDisplayFileFromFileExplorer) \
    .pack()

initial_frame.pack()
canvas.pack(side="left", fill="both", expand=True)
vertical_bitmap_scrollbar.pack(side="right", fill="y")
horizontal_bitmap_scrollbar.pack(side="bottom", fill="x")

root.mainloop()
