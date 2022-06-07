import os
import pathlib
import shutil
from os.path import exists

import numpy as np
from PIL import Image, ImageEnhance
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox

from sample_group_box import SampleGroupBox

Image.MAX_IMAGE_PIXELS = None


class Event_Manager(QMainWindow):
    """
    This class is used to manage some events applied on widgets of the main window and more
    """

    def __init__(self, ui):
        """
        This function is used to initialize the class

        :param ui: The main window's UI object
        """

        super(Event_Manager, self).__init__()
        self.ui = ui
        self.connectAllWidgets()

    def connectAllWidgets(self):
        """
        This function is used to connect all the widgets of the main window to their corresponding functions

        :return: None
        """

        self.ui.select_bitmap_button.clicked.connect(self.openFileDialog)
        self.ui.quit_button.clicked.connect(self.quitApp)
        self.ui.save_bmp_data_button.clicked.connect(self.saveBmpData)
        self.ui.mouse_tracker.positionChanged.connect(self.on_positionChanged)

    def openFileDialog(self):
        """
            This function is used to open the file dialog and select an image to display in the label.
            It will then call the functions to retrieve the rectangle data and enable the widgets.

            :return: None
        """

        if self.ui.bitmap_label.bitmap_image is not None:
            self.ui.bitmap_label.bitmap_image.close()
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Open File",
                                                  "",
                                                  "BMP files (*.bmp);;PNG files (*.png);;All Files (*)",
                                                  )
        if fileName:
            self.ui.file_name = os.path.basename(fileName).split('.', 1)[0]
            self.ui.bitmap_label.bitmap_image = Image.open(fileName)
            self.ui.original_image = self.ui.bitmap_label.bitmap_image
            self.ui.bitmap_data = np.array(self.ui.bitmap_label.bitmap_image)
            resized_image = self.ui.bitmap_label.bitmap_image.resize(
                (1837, 367),
                QtCore.Qt.KeepAspectRatio)
            resized_image.save("_resized.bmp")
            self.ui.bitmap_label.bitmap_image = resized_image
            self.ui.pixmap = QPixmap("_resized.bmp")
            self.ui.bitmap_label.pixmap = self.ui.pixmap
            self.ui.bitmap_label.setPixmap(self.ui.pixmap)
            self.ui.real_width, self.ui.real_height = self.ui.original_image.size
            self.retrieveRectangleData()
            self.enableWidgets()

    def retrieveRectangleData(self):
        """
        This function is used to retrieve the rectangle data and store it in the sample group boxes.

        :return: None
        """

        file_exists = exists("_previous_rectangles_data.txt")
        if file_exists:
            with open("_previous_rectangles_data.txt", "r") as f:
                self.ui.previous_rectangles_data = f.readlines()
                for rectangle_data in self.ui.previous_rectangles_data:
                    rectangle_data = rectangle_data[rectangle_data.find("(") + 1:rectangle_data.find(")")].split(
                        ", ")
                    self.ui.rectangles.append(QtCore.QRect(int(rectangle_data[0]), int(rectangle_data[1]),
                                                           int(rectangle_data[2]) - int(rectangle_data[0]),
                                                           int(rectangle_data[3]) - int(rectangle_data[1])))
                    self.ui.sample_group_boxes.append(SampleGroupBox(self.ui, len(self.ui.rectangles) - 1))
                    self.ui.sample_group_boxes[-1].setX0(self.ui.number_format)
                    self.ui.sample_group_boxes[-1].setY0(self.ui.number_format)
                    self.ui.sample_group_boxes[-1].setXF(self.ui.number_format)
                    self.ui.sample_group_boxes[-1].setYF(self.ui.number_format)

    def enableWidgets(self):
        """
        This function is used to enable the widgets of the main window. This is called when an image is loaded.

        :return: None
        """

        if self.ui.image_is_displayed is False:
            self.ui.flip_image_button.setEnabled(True)
            self.ui.flip_image_button.clicked.connect(self.flipImage)
            self.ui.pixel_conversion_button.setEnabled(True)
            self.ui.pixel_conversion_button.clicked.connect(self.pixelConvert)
            self.ui.millimeter_conversion_button.setEnabled(True)
            self.ui.millimeter_conversion_button.clicked.connect(self.millimeterConvert)
            self.ui.micron_conversion_button.setEnabled(True)
            self.ui.micron_conversion_button.clicked.connect(self.micronConvert)
            self.ui.image_is_displayed = True
            self.ui.horizontalSlider.setEnabled(True)
            self.ui.horizontalSlider.valueChanged.connect(self.setContrast)
            self.ui.contrastValueLabel.setText(str(self.ui.horizontalSlider.value()))

    def saveBmpData(self):
        """
        This function is used to save the bitmap data in a defined format.
        That format consists in a tree of directories and files.

        :except FileNotFoundError
        :return: None
        """

        directoryName = QFileDialog.getExistingDirectory(self, 'Select a directory')
        if directoryName:
            path = directoryName + "/" + self.ui.file_name
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
            try:
                shutil.rmtree(path)
            except OSError:
                print(OSError)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("File(s) still open")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setText("Please close the files that are still open before overwriting them with the new ones.")
                x = msg.exec_()
            for rectangle in self.ui.rectangles:
                x0 = int(self.ui.real_width * rectangle.x() / self.ui.bitmap_label.size().width())
                xf = int(self.ui.real_width * (rectangle.x() + rectangle.width()) / self.ui.bitmap_label.size().width())
                y0 = int(self.ui.real_height * rectangle.y() / self.ui.bitmap_label.size().height())
                yf = int(
                    self.ui.real_height * (rectangle.y() + rectangle.height()) / self.ui.bitmap_label.size().height())
                str_iteration = ''
                path = directoryName + "/" + self.ui.file_name + "/" + "SP" + str(
                    self.ui.rectangles.index(rectangle) + 1) + self.ui.file_name
                pathlib.Path(path).mkdir(parents=True, exist_ok=True)
                str_iteration += "HEADER\n\n"
                str_iteration += "SP" + str(self.ui.rectangles.index(rectangle) + 1) + self.ui.file_name + '\n'
                str_iteration += 'FLIPPED = ' + str(self.ui.flipped) + '\n'
                str_iteration += str(rectangle.getCoords()) + ' => (X, Y, Width, Length)' + '\n\n\n'
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
                    path + "/" + "SP" + str(self.ui.rectangles.index(rectangle) + 1) + self.ui.file_name + ".bmp")

    @QtCore.pyqtSlot(QtCore.QPoint)
    def on_positionChanged(self, pos):
        """
        This function is called everytime the mouse is moved.
        It updates the position of the mouse in the main window and displays it on top of the label.

        :param pos: The position of the mouse cursor.
        :return: None
        """
        try:
            x = self.ui.real_width * pos.x() / self.ui.bitmap_label.size().width() / self.ui.value_type
            y = self.ui.real_height * pos.y() / self.ui.bitmap_label.size().height() / self.ui.value_type
            self.ui.mousetracker_label.setText(
                "x: " + self.ui.number_format % x + ", y: " + self.ui.number_format % y + ", value: %d" % (
                        int((256 ** 2) - self.ui.bitmap_data[int(y)][int(x)][0] ** 2) - 1))
        except AttributeError:
            pass
        except IndexError:
            pass

    def flipImage(self):
        """
        This function is used to flip the image from left to right.

        :return: None
        """

        # TODO : DeprecationWarning: FLIP_LEFT_RIGHT is deprecated and will be removed in Pillow 10 (2023-07-01). Use Transpose.FLIP_LEFT_RIGHT instead
        self.ui.bitmap_data = self.ui.bitmap_data[::-1]
        self.ui.bitmap_label.bitmap_image = self.ui.bitmap_label.bitmap_image.transpose(
            method=Image.FLIP_LEFT_RIGHT)
        self.ui.bitmap_label.bitmap_image.save("_resized.bmp")
        self.ui.pixmap = QPixmap("_resized.bmp")
        self.ui.bitmap_label.pixmap = self.ui.pixmap
        self.ui.bitmap_label.setPixmap(self.ui.pixmap)
        self.ui.flipped = not self.ui.flipped

    def setContrast(self):
        """
        This function is used to set the contrast of the image with the slider.

        :return: None
        """
        self.ui.contrastValueLabel.setText(str(self.ui.horizontalSlider.value()))
        contrast_value = self.ui.horizontalSlider.value()
        contrast = ImageEnhance.Contrast(self.ui.bitmap_label.bitmap_image)
        modified_contrast_image = contrast.enhance((contrast_value - 50) / 25. + 0.5)
        modified_contrast_image.resize(
            (self.ui.pixmap.width(), self.ui.pixmap.height()),
            QtCore.Qt.KeepAspectRatio).save("_contrasted.bmp")
        self.ui.pixmap = QPixmap("_contrasted.bmp")
        self.ui.bitmap_label.pixmap = self.ui.pixmap
        self.ui.bitmap_label.setPixmap(self.ui.pixmap)
        self.ui.bitmap_label.update()

    def quitApp(self):
        """
        This function is used to quit the application. Either with the quit button or the red cross.
        It writes down the rectangles' coordinates in the corresponding file.

        :return: None
        """
        if self.ui.bitmap_label.bitmap_image is not None:
            while self.ui.bitmap_label.scale > 1:
                self.ui.bitmap_label.onZoomOut()
            with open("_previous_rectangles_data.txt", 'w') as file:
                for rectangle in self.ui.rectangles:
                    str_iteration = str(rectangle.getCoords()) + '\n'
                    file.write(str_iteration)
                    file.flush()
            file.close()
        QCoreApplication.exit(0)

    def pixelConvert(self):
        """
        This function is used to convert the image to a pixel-based representation.

        :return: None
        """
        for sample_group_box in self.ui.bitmap_label.sample_group_boxes:
            self.ui.value_type = 1
            sample_group_box.updateLineEdits("%d")
            self.ui.number_format = "%d"

    def millimeterConvert(self):
        """
        This function is used to convert the image to a millimeter-based representation.

        :return: None
        """
        for sample_group_box in self.ui.bitmap_label.sample_group_boxes:
            self.ui.value_type = 100
            sample_group_box.updateLineEdits("%.2f")
            self.ui.number_format = "%.2f"

    def micronConvert(self):
        """
        This function is used to convert the image to a micron-based representation.

        :return: None
        """
        for sample_group_box in self.ui.bitmap_label.sample_group_boxes:
            self.ui.value_type = 0.1
            sample_group_box.updateLineEdits("%d")
            self.ui.number_format = "%d"
