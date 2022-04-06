import os
import pathlib

from scipy import misc
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import uic, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QPushButton, QLabel

# To prevent the following error: "Image size (460000000 pixels) exceeds limit of 178956970 pixels, could be decompression bomb DOS attack"
Image.MAX_IMAGE_PIXELS = None


class UI(QMainWindow):
    # Initialize the main window's UI components
    def __init__(self):
        super(UI, self).__init__()

        # Initialize the UI component variables
        self.pixmap = None
        self.select_bitmap_button = None
        self.quit_button = None
        self.bitmap_label = None

        uic.loadUi(str(pathlib.Path(__file__).parent.resolve()) + "\\main.ui", self)  # Load the UI file
        self.retranslateUi()  # Translate the UI components into Python Objects
        self.connectAllWidgets()  # Connect all the UI components to their respective functions

        self.show()  # Show the main window

    # Function to translate the main window's UI components into Python Objects
    # @param self The object pointer
    def retranslateUi(self):
        self.quit_button = self.findChild(QPushButton, "quit_button")
        self.select_bitmap_button = self.findChild(QPushButton, "select_bitmap_button")
        self.bitmap_label = self.findChild(QLabel, "bitmap_label")

    # Function to connect all the UI components to their respective functions
    # @param self The object pointer
    def connectAllWidgets(self):
        self.select_bitmap_button.clicked.connect(
            self.openFileNameDialog)  # Connect the select bitmap button to the openFileNameDialog function
        self.quit_button.clicked.connect(self.close)  # Connect the quit button to the close function from QMainWindow

    # Select BMP file from file explorer and directly display it
    # @param self The object pointer
    def openFileNameDialog(self):
        fileName = QFileDialog.getOpenFileName(self,
                                               "Open File",
                                               "",
                                               "BMP files (*.bmp);;PNG files (*.png);;All Files (*)",
                                               )  # Get the file name from the file explorer
        self.pixmap = QPixmap(fileName[0])  # Create a QPixmap object from the selected file
        self.bitmap_label.setPixmap(self.pixmap)  # Set the bitmap label's pixmap to the QPixmap object
        self.bitmap_label.adjustSize()  # Adjust the bitmap label's size to fit the QPixmap object


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)  # Create the application
    ui = UI()  # Create the main window object
    sys.exit(app.exec_())  # Execute the application

# End of main2.py
