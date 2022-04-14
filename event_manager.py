from PIL import Image
from PIL.Image import Resampling
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap, QWheelEvent
from PyQt5.QtWidgets import QFileDialog, QWidget, QMainWindow
from numpy import asarray

Image.MAX_IMAGE_PIXELS = None


# This class is used to take care of the events of the widgets
class Event_Manager(QMainWindow):
    # Constructor of the class Event_Manager
    def __init__(self, ui):
        super(Event_Manager, self).__init__()  # Call the constructor of the parent class
        self.ui = ui  # Set the ui attribute to the ui parameter
        self.connectAllWidgets()  # Connect all the widgets to their corresponding functions

    # This function is used to connect all the widgets to their corresponding functions
    def connectAllWidgets(self):
        self.ui.select_bitmap_button.clicked.connect(
            self.openFileDialog)  # Connect the select bitmap button to the openFileNameDialog function
        self.ui.quit_button.clicked.connect(
            QCoreApplication.instance().quit)  # Connect the quit button to the close function from QMainWindow
        self.ui.save_bmp_data_button.clicked.connect(
            self.saveBmpData)  # Connect the save bitmap data button to the saveBmpData function
        self.ui.mouse_tracker.positionChanged.connect(
            self.on_positionChanged)  # Connect the mouse tracker to the on_positionChanged function

    # This function is used to open the file dialog
    def openFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Open File",
                                                  "D:\\Workspace\\LERMA\\SelectZones",
                                                  "BMP files (*.bmp);;PNG files (*.png);;All Files (*)",
                                                  )  # Get the file name from the file explorer
        if fileName:  # If the file name is not empty
            self.ui.bitmap_image = Image.open(fileName)  # Open the image
            self.ui.bitmap_data = asarray(self.ui.bitmap_image)  # Convert the image to a numpy array

            resized_image = self.ui.bitmap_image.resize(
                (self.ui.bitmap_label.width(), self.ui.bitmap_label.height()),
                resample=Resampling.BILINEAR)  # Resize the image to fit the bitmap label
            resized_image.save("_resized.bmp")  # Save the resized image
            self.ui.bitmap_label.bitmap_image = resized_image  # Set the bitmap label to the resized image
            # TODO : DeprecationWarning: FLIP_LEFT_RIGHT is deprecaqted and will be removed in Pillow 10 (2023-07-01). Use Transpose.FLIP_LEFT_RIGHT instead
            # im = im.transpose(method=Image.FLIP_LEFT_RIGHT)

            self.ui.pixmap = QPixmap("_resized.bmp")  # Create a QPixmap from the resized image
            self.ui.bitmap_label.pixmap = self.ui.pixmap  # Set the bitmap label to the resized image
            self.ui.bitmap_label.setPixmap(self.ui.pixmap)  # Set the bitmap label's pixmap to the QPixmap object
            self.ui.bitmap_image.close()  # Close the image
            self.ui.image_is_displayed = True  # Set the image is displayed attribute to True

    # This function is used to save the bitmap data
    def saveBmpData(self):
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "Save File",
                                                  "D:\\Workspace\\LERMA\\SelectZones",
                                                  "TXT files (*.txt)",
                                                  )  # Get the file name from the file explorer
        if fileName:  # If the file name is not empty
            print(self.ui.bitmap_data)
            print(self.ui.bitmap_data.size)
            str_iteration = ''
            with open(fileName, 'w') as file:
                for i in range(50):
                    for j in range(50):
                        str_iteration = str_iteration + str(self.ui.bitmap_data[i][j]) + '\n'
                    file.write(str_iteration)
            file.close()

    @QtCore.pyqtSlot(QtCore.QPoint)
    # This function is used to update the mouse tracker label
    def on_positionChanged(self, pos):
        self.ui.mousetracker_label.setText("x: %d, y: %d" % (pos.x(), pos.y()))  # Update the mouse tracker label
