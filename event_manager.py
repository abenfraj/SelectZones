import os
import pathlib
import shutil
from os.path import exists

import numpy as np
from PIL import Image, ImageEnhance
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QMainWindow

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
            self.quitApp)  # Connect the quit button to the close function from QMainWindow
        self.ui.save_bmp_data_button.clicked.connect(
            self.saveBmpData)  # Connect the save bitmap data button to the saveBmpData function
        self.ui.mouse_tracker.positionChanged.connect(
            self.on_positionChanged)  # Connect the mouse tracker to the on_positionChanged function

    def openFileDialog(self):
        """
            This function is used to open the file dialog
        """
        if self.ui.bitmap_label.bitmap_image is not None:  # If the bitmap image is not None
            self.ui.bitmap_label.bitmap_image.close()  # Close the bitmap image
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Open File",
                                                  "",
                                                  "BMP files (*.bmp);;PNG files (*.png);;All Files (*)",
                                                  )  # Get the file name from the file explorer
        if fileName:  # If the file name is not empty
            self.ui.file_name = os.path.basename(fileName).split('.', 1)[
                0]  # Set the file name attribute to the file name without the extension
            self.ui.bitmap_label.bitmap_image = Image.open(fileName)  # Open the image
            self.ui.original_image = self.ui.bitmap_label.bitmap_image  # Set the original image to the bitmap image
            self.ui.bitmap_data = np.array(self.ui.bitmap_label.bitmap_image)  # Convert the image to a numpy array
            resized_image = self.ui.bitmap_label.bitmap_image.resize(
                (1837, 367),
                QtCore.Qt.KeepAspectRatio)  # Resize the image to fit the bitmap label
            resized_image.save("_resized.bmp")  # Save the resized image
            self.ui.bitmap_label.bitmap_image = resized_image  # Set the bitmap label to the resized image
            self.ui.pixmap = QPixmap("_resized.bmp")  # Create a QPixmap from the resized image
            self.ui.bitmap_label.pixmap = self.ui.pixmap  # Set the bitmap label to the resized image
            self.ui.bitmap_label.setPixmap(self.ui.pixmap)  # Set the bitmap label's pixmap to the QPixmap object

            file_exists = exists("_previous_rectangles_data.txt")  # Check if the file exists
            if file_exists:  # If the file exists
                with open("_previous_rectangles_data.txt", "r") as f:  # Open the file
                    self.ui.previous_rectangles_data = f.readlines()  # Read the file
                    for rectangle_data in self.ui.previous_rectangles_data:  # For each rectangle data
                        rectangle_data = rectangle_data[rectangle_data.find("(") + 1:rectangle_data.find(")")].split(
                            ", ")  # Split the data
                        self.ui.rectangles.append(QtCore.QRect(int(rectangle_data[0]), int(rectangle_data[1]),
                                                               int(rectangle_data[2]) - int(rectangle_data[0]),
                                                               int(rectangle_data[3]) - int(
                                                                   rectangle_data[1])))  # Create a rectangle

            if self.ui.image_is_displayed is False:  # If the image is not displayed
                self.ui.flip_image_button.setEnabled(True)  # Enable the flip image button
                self.ui.flip_image_button.clicked.connect(
                    self.flip_image)  # Connect the flip image button to the flip_image function
                self.ui.image_is_displayed = True  # Set the image is displayed attribute to True
                self.ui.horizontalSlider.setEnabled(True)  # Enable the horizontal slider
                self.ui.horizontalSlider.valueChanged.connect(
                    self.setContrast)  # Connect the horizontal slider to the setContrast function

    # This function is used to save the bitmap data
    def saveBmpData(self):
        directoryName = QFileDialog.getExistingDirectory(self,
                                                         'Select a directory')  # Get the directory name from the file explorer
        if directoryName:  # If the file name is not empty
            path = directoryName + "/" + self.ui.file_name
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
            shutil.rmtree(path)
            for rectangle in self.ui.rectangles:  # For each rectangle
                x0 = int(self.ui.real_width * rectangle.x() / self.ui.bitmap_label.size().width())
                xf = int(
                    self.ui.real_width * (rectangle.x() + rectangle.width()) / self.ui.bitmap_label.size().width())
                y0 = int(self.ui.real_height * rectangle.y() / self.ui.bitmap_label.size().height())
                yf = int(
                    self.ui.real_height * (rectangle.y() + rectangle.height()) / self.ui.bitmap_label.size().height())
                str_iteration = ''
                path = directoryName + "/" + self.ui.file_name + "/" + "SP" + str(
                    self.ui.rectangles.index(rectangle) + 1) + self.ui.file_name
                pathlib.Path(path).mkdir(parents=True, exist_ok=True)
                str_iteration += 'HEADER\n\n'
                str_iteration += 'FLIPPED = ' + str(self.ui.flipped) + '\n\n'
                str_iteration += 'Pixel X \tAverage Y Value\n\n'
                with open(path + "/" + "SP" + str(self.ui.rectangles.index(rectangle) + 1) + self.ui.file_name + ".txt",
                          'w') as file:
                    for x in range(x0, xf):
                        average_value = 0
                        for y in range(y0, yf):
                            np_sum = (256 ** 2) - (int(self.ui.bitmap_data[y][x][0]) ** 2)
                            average_value += np_sum
                        average_value /= (yf - y0 + 1)
                        str_iteration += str("{:.3f}".format(x / 100)) + "\t\t" + str(int(average_value)) + '\n'
                        file.write(str_iteration)
                        file.flush()
                        str_iteration = ''
                file.close()
                cropped_image = self.ui.original_image.crop((x0, y0, xf, yf))
                cropped_image.save(
                    path + "/" + "SP" + str(self.ui.rectangles.index(rectangle) + 1) + self.ui.file_name + ".png")

    @QtCore.pyqtSlot(QtCore.QPoint)
    # This function is used to update the mouse tracker label
    def on_positionChanged(self, pos):
        try:
            self.ui.real_width, self.ui.real_height = self.ui.original_image.size  # Get the real width and height of the image
            self.ui.mousetracker_label.setText("x: %.3f, y: %.3f" % (
                (self.ui.real_width * pos.x() / self.ui.bitmap_label.size().width()) * 0.21,
                (
                        self.ui.real_height * pos.y() / self.ui.bitmap_label.size().height()) * 0.21))  # Update the mouse tracker label
        except AttributeError:  # If the bitmap image is not set
            pass

    def flip_image(self):
        self.ui.bitmap_data = self.ui.bitmap_data[::-1]  # Flip the bitmap data
        # TODO : DeprecationWarning: FLIP_LEFT_RIGHT is deprecated and will be removed in Pillow 10 (2023-07-01). Use Transpose.FLIP_LEFT_RIGHT instead
        self.ui.bitmap_label.bitmap_image = self.ui.bitmap_label.bitmap_image.transpose(
            method=Image.FLIP_LEFT_RIGHT)  # Flip the image
        self.ui.bitmap_label.bitmap_image.save("_resized.bmp")  # Save the flipped image
        self.ui.pixmap = QPixmap("_resized.bmp")  # Create a QPixmap from the resized image
        self.ui.bitmap_label.pixmap = self.ui.pixmap  # Set the bitmap label to the resized image
        self.ui.bitmap_label.setPixmap(self.ui.pixmap)  # Set the bitmap label's pixmap to the QPixmap object
        self.ui.flipped = not self.ui.flipped  # Update the flipped boolean

    def setContrast(self):
        contrast_value = self.ui.horizontalSlider.value()  # Get the contrast value
        contrast = ImageEnhance.Contrast(self.ui.bitmap_label.bitmap_image)  # Create an image enhancer object
        modified_contrast_image = contrast.enhance((contrast_value - 50) / 25. + 0.5)
        modified_contrast_image.resize(
            (self.ui.pixmap.width(), self.ui.pixmap.height()),
            QtCore.Qt.KeepAspectRatio).save("_contrasted.bmp")  # Save the enhanced image
        self.ui.pixmap = QPixmap("_contrasted.bmp")  # Create a QPixmap from the resized image
        self.ui.bitmap_label.pixmap = self.ui.pixmap  # Set the bitmap label to the resized image
        self.ui.bitmap_label.setPixmap(self.ui.pixmap)  # Set the bitmap label's pixmap to the QPixmap object
        self.ui.bitmap_label.update()  # Update the bitmap label

    def quitApp(self):
        with open("_previous_rectangles_data.txt", 'w') as file:
            for rectangle in self.ui.rectangles:
                print(rectangle)
                str_iteration = str(rectangle.getCoords()) + '\n'
                file.write(str_iteration)
                file.flush()
        file.close()
        QCoreApplication.exit(0)
