import pathlib
from PIL import Image
from PIL.Image import Resampling
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap, QWheelEvent
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QApplication, QPushButton, QLabel, QWidget, QScrollArea

# To prevent the following error: "Image size (460000000 pixels) exceeds limit of 178956970 pixels, could be decompression bomb DOS attack"
from numpy import asarray

from mouse_tracker import MouseTracker

Image.MAX_IMAGE_PIXELS = None


class UI(QMainWindow):
    # Initialize the main window's UI components
    def __init__(self):
        super(UI, self).__init__()

        # Initialize the UI component variables
        self.mousetracker_label = None
        self.label_position = None
        self.mouse_tracker = None
        self.image_is_displayed = False
        self.bitmap_image = None
        self.bitmap_data = None
        self.save_bmp_data_button = None
        self.pixmap = None
        self.select_bitmap_button = None
        self.quit_button = None
        self.bitmap_label = None
        self.scrollAreaWidgetContents = None
        self.scrollArea = None
        self.centralwidget = None

        self.scale = 1.0

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
        self.save_bmp_data_button = self.findChild(QPushButton, "save_bmp_data_button")
        self.centralwidget = self.findChild(QWidget, "centralwidget")
        self.scrollArea = self.findChild(QScrollArea, "scrollArea")
        self.mousetracker_label = self.findChild(QLabel, "mousetracker_label")
        self.scrollAreaWidgetContents = self.findChild(QWidget, "scrollAreaWidgetContents")
        self.mouse_tracker = MouseTracker(self.bitmap_label)

    # Function to connect all the UI components to their respective functions
    # @param self The object pointer
    def connectAllWidgets(self):
        self.select_bitmap_button.clicked.connect(
            self.openFileDialog)  # Connect the select bitmap button to the openFileNameDialog function
        self.quit_button.clicked.connect(self.close)  # Connect the quit button to the close function from QMainWindow
        self.save_bmp_data_button.clicked.connect(
            self.saveBmpData)  # Connect the save bitmap data button to the saveBmpData function
        self.mouse_tracker.positionChanged.connect(
            self.on_positionChanged)  # Connect the mouse tracker to the on_positionChanged function

    # Select BMP file from file explorer and directly display it
    # @param self The object pointer
    def openFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Open File",
                                                  "D:\\Workspace\\LERMA\\SelectZones",
                                                  "BMP files (*.bmp);;PNG files (*.png);;All Files (*)",
                                                  )  # Get the file name from the file explorer
        if fileName:
            self.bitmap_image = Image.open(fileName)
            self.bitmap_data = asarray(self.bitmap_image)

            resized_image = self.bitmap_image.resize(
                (self.bitmap_label.width(), self.bitmap_label.height()),
                resample=Resampling.BILINEAR)
            resized_image.save("_resized.bmp")
            # TODO : DeprecationWarning: FLIP_LEFT_RIGHT is deprecated and will be removed in Pillow 10 (2023-07-01). Use Transpose.FLIP_LEFT_RIGHT instead
            # im = im.transpose(method=Image.FLIP_LEFT_RIGHT)

            self.pixmap = QPixmap("_resized.bmp")
            self.bitmap_label.setPixmap(self.pixmap)  # Set the bitmap label's pixmap to the QPixmap object
            self.bitmap_image.close()
            self.image_is_displayed = True

    # Save the bitmap data to a file
    # @param self The object pointer
    def saveBmpData(self):
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "Save File",
                                                  "D:\\Workspace\\LERMA\\SelectZones",
                                                  "TXT files (*.txt)",
                                                  )  # Get the file name from the file explorer
        if fileName:
            print(self.bitmap_data)
            print(self.bitmap_data.size)
            str_iteration = ''
            with open(fileName, 'w') as file:
                for i in range(self.image_height):
                    for j in range(self.image_width):
                        str_iteration = str_iteration + str(self.bitmap_data[i][j]) + '\n'
                    file.write(str_iteration)
            file.close()

    @QtCore.pyqtSlot(QtCore.QPoint)
    def on_positionChanged(self, pos):
        self.mousetracker_label.setText("x: %d, y: %d" % (pos.x(), pos.y()))

    def wheelEvent(self, event: QWheelEvent):
        if self.bitmap_label is not None:
            if event.angleDelta().y() > 0:
                self.on_zoom_in(event)
                # self.resize_image()
            else:
                self.on_zoom_out(event)
                # self.resize_image()

    def on_zoom_in(self, event):
        self.scale *= 2

    def on_zoom_out(self, event):
        self.scale /= 2

    # TODO : have to fix this
    def resize_image(self):
        size = self.pixmap.size()
        scaled_pixmap = self.pixmap.scaled(self.scale * size)
        self.label.setPixmap(scaled_pixmap)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)  # Create the application
    ui = UI()  # Create the main window object
    sys.exit(app.exec_())  # Execute the application

# End of main2.py
