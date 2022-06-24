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
    This class is used to manage some events applied on widgets of the main window. It connects some widgets to their
    corresponding functions, retrieves some data from the last usage of the program and enables some widgets after the
    image is loaded.
    """
    def __init__(self, ui):
        """
        This function is used to initialize the class.

        :param ui: The main window's UI object
        :return: None
        """
        super(Event_Manager, self).__init__()
        self.ui = ui
        self.connectAllWidgets()

    def connectAllWidgets(self):
        """
        This function is used to connect all the widgets of the main window to their corresponding functions.

        :return: None
        """
        self.ui.select_bitmap_button.clicked.connect(self.openFileDialog)
        self.ui.quit_button.clicked.connect(self.quitApp)
        self.ui.save_bmp_data_button.clicked.connect(self.saveBmpData)
        self.ui.mouse_tracker.positionChanged.connect(self.on_positionChanged)

    def openFileDialog(self):
        """
        This function is used to open the file dialog and select an image to display in the label. You are only able to
        choose a bitmap file (*.bmp). When the image is chosen, a label will display its name in the bottom right corner
        of the window. The data of the image is stored in the bitmap_data variable. The image is also resized to fit the
        label. Only then, the image is displayed in the label with the last drawn rectangles from the previous session
        and the widgets are enabled. The path of the chosen image is also saved with the saveFilePath function.

        :return: None
        """
        if self.ui.bitmap_label.bitmap_image is not None:
            self.ui.bitmap_label.bitmap_image.close()
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Open File",
                                                  self.openFilePath(),
                                                  "BMP files (*.bmp)",
                                                  )
        if fileName:
            self.ui.file_name = os.path.basename(fileName).split('.', 1)[0]
            self.ui.file_name_label.setText("SelectZones - " + self.ui.file_name)
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
            self.saveFilePath(fileName)

    def retrieveRectangleData(self):
        """
        This function is used to retrieve the rectangle data from the "_previous_rectangles_data.txt" file and store it
        in the sample group boxes. It automatically displays them in the label.

        :return: None
        """
        file_exists = exists("_previous_rectangles_data.txt")
        if file_exists and len(self.ui.rectangles) == 0:
            with open("_previous_rectangles_data.txt", "r") as f:
                self.ui.previous_rectangles_data = f.readlines()
                for rectangle_data in self.ui.previous_rectangles_data:
                    rectangle_data = rectangle_data[rectangle_data.find("(") + 1:rectangle_data.find(")")].split(
                        ", ")
                    qp = QtCore.QPoint(int(rectangle_data[0]), int(rectangle_data[1]))
                    qs = QtCore.QSize(int(rectangle_data[2]), int(rectangle_data[3]))
                    self.ui.rectangles.append(QtCore.QRect(qp, qs))
                    self.ui.sample_group_boxes.append(SampleGroupBox(self.ui, len(self.ui.rectangles) - 1))
                    self.ui.sample_group_boxes[-1].setX0()
                    self.ui.sample_group_boxes[-1].setY0()
                    self.ui.sample_group_boxes[-1].setXF()
                    self.ui.sample_group_boxes[-1].setYF()

    def enableWidgets(self):
        """
        This function is used to enable some widgets of the main window. This is mainly called when an image is loaded.

        :return: None
        """
        if self.ui.image_is_displayed is False:
            self.ui.flip_image_button.setEnabled(True)
            self.ui.flip_image_button.clicked.connect(self.flipImage)
            self.ui.image_is_displayed = True
            self.ui.contrastLineEdit.setEnabled(True)
            self.ui.contrast_apply_button.setEnabled(True)
            self.ui.contrast_apply_button.clicked.connect(self.setContrast)
            self.ui.conversion_factor_button.setEnabled(True)
            self.ui.conversion_factor_button.clicked.connect(self.setConversionFactor)
            self.ui.conversion_factor_line_edit.setEnabled(True)
            self.ui.conversion_factor_line_edit.setValidator(
                QtGui.QRegExpValidator(QtCore.QRegExp(r"[0-9]+[,.]?[0-9]*([\/][0-9]+[,.]?[0-9]*)*\/?")))
            self.ui.sp_to_ip_value_label.setText(self.ui.bitmap_label.calculateSPToIPValue())

    def saveBmpData(self):
        """
        This function is used to save the bitmap data in a defined format. That format consists in a tree of directories
        and files. It allows you to select a directory in which the tree will be created. If the directory already
        exists, it will be overwritten. The tree will contain the following directories and files:
            - a directory named after the image.
            - a set of directories each associated with a corresponding number and the file name.
            - a cropped image corresponding to the associated rectangle in its directory.
            - an output file in its directory.
        Rectangles must be drawn on the label to use this feature successfully. If not, a message will pop up and tell
        the user to do so. You also have to close all the old output files before using this feature. A message will pop
        up if you try to save the data while the output file is still open.

        :except FileNotFoundError
        :return: None
        """
        if len(self.ui.rectangles) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("No rectangle drawn")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setText("There are no drawn rectangle to save any data.")
            x = msg.exec_()
            button = msg.clickedButton()
            sb = msg.standardButton(button)
            if sb == QMessageBox.Ok:
                return
        directoryName = QFileDialog.getExistingDirectory(self, 'Select a directory', self.openFilePath())
        if directoryName:
            path = directoryName + "/" + self.ui.file_name
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
            try:
                shutil.rmtree(path)
            except OSError:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("File(s) still open")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setText("Please close the files that are still open before overwriting them with the new ones.")
                x = msg.exec_()
            for rectangle in self.ui.rectangles:
                self.ui.sample_group_boxes[self.ui.rectangles.index(rectangle)].correctSample()
                x0 = round(float(self.ui.sample_group_boxes[self.ui.rectangles.index(rectangle)].lineEditX0.text()) / (
                        1 / self.ui.value_type))
                xf = round(float(self.ui.sample_group_boxes[self.ui.rectangles.index(rectangle)].lineEditXF.text()) / (
                        1 / self.ui.value_type))
                y0 = round(float(self.ui.sample_group_boxes[self.ui.rectangles.index(rectangle)].lineEditY0.text()) / (
                        1 / self.ui.value_type))
                yf = round(
                    float(self.ui.sample_group_boxes[self.ui.rectangles.index(rectangle)].lineEditYF.text()) / (
                            1 / self.ui.value_type))
                str_iteration = ''
                path = directoryName + "/" + self.ui.file_name + "/" + "SP" + str(
                    self.ui.rectangles.index(rectangle) + 1) + self.ui.file_name
                pathlib.Path(path).mkdir(parents=True, exist_ok=True)
                str_iteration += "HEADER\n\n"
                str_iteration += "SP" + str(self.ui.rectangles.index(rectangle) + 1) + self.ui.file_name + '\n'
                str_iteration += "FLIPPED = " + str(self.ui.flipped) + '\n'
                str_iteration += "(" + self.ui.sample_group_boxes[
                    self.ui.rectangles.index(rectangle)].lineEditX0.text() + ", " + self.ui.sample_group_boxes[
                                     self.ui.rectangles.index(rectangle)].lineEditY0.text() + ", " + \
                                 self.ui.sample_group_boxes[
                                     self.ui.rectangles.index(rectangle)].lineEditXF.text() + ", " + \
                                 self.ui.sample_group_boxes[
                                     self.ui.rectangles.index(
                                         rectangle)].lineEditYF.text() + ") => (X0, Y0, XF, YF)" + "\n"
                str_iteration += "Conversion factor in pixels per millimeter = " + str(
                    self.ui.value_type) + " (default value is 100)\n\n\n"
                str_iteration += 'X Value \tAverage Y Value\n\n'
                with open(path + "/" + "SP" + str(self.ui.rectangles.index(rectangle) + 1) + self.ui.file_name + ".txt",
                          'w') as file:
                    file.write(str_iteration)
                    file.flush()
                    str_iteration = ''
                    for x in range(x0, xf + 1):
                        average_value = 0
                        for y in range(y0, yf):
                            np_sum = 256 - int(self.ui.bitmap_data[y][x][0]) - 1
                            average_value += np_sum
                        average_value /= (yf - y0)
                        str_iteration += str("{:.3f}".format(x / self.ui.value_type)) + "\t\t" + str(
                            int(average_value)) + '\n'
                        file.write(str_iteration)
                        file.flush()
                        str_iteration = ''
                file.close()
                try:
                    cropped_image = self.ui.original_image.crop((x0, y0, xf, yf))
                except ValueError:
                    try:
                        cropped_image = self.ui.original_image.crop((xf, yf, x0, y0))
                    except ValueError:
                        try:
                            cropped_image = self.ui.original_image.crop((x0, yf, xf, y0))
                        except ValueError:
                            cropped_image = self.ui.original_image.crop((xf, y0, x0, yf))
                cropped_image.save(
                    path + "/" + "SP" + str(self.ui.rectangles.index(rectangle) + 1) + self.ui.file_name + ".bmp")

    @QtCore.pyqtSlot(QtCore.QPoint)
    def on_positionChanged(self, pos):
        """
        This function is called everytime the mouse is moved. It updates the position of the mouse in the main window
        and displays it on top of the label. The value displayed is the value of the pixel at the position of the mouse
        in millimeters. It depends on the value_type variable.

        :param pos: The position of the mouse cursor.
        :return: None
        """
        try:
            x = self.ui.real_width * pos.x() / self.ui.bitmap_label.size().width()
            y = self.ui.real_height * pos.y() / self.ui.bitmap_label.size().height()
            self.ui.mousetracker_label.setText(
                "x: " + "%.3f" % self.roundTo(x / self.ui.value_type, base=1 / self.ui.value_type,
                                              prec=3) + ", y: " + "%.3f" % self.roundTo(
                    y / self.ui.value_type, base=1 / self.ui.value_type, prec=3) + ", value: %d" % (
                        256 - self.ui.bitmap_data[int(y)][int(x)][0] - 1))
        except IndexError:
            pass
        except TypeError:
            pass
        except AttributeError:
            pass

    @staticmethod
    def roundTo(x, prec, base):
        """
        This function rounds a number to a certain precision.

        :param x: The number to be rounded.
        :param prec: The precision of the number (meaning the number of digits after the decimal point).
        :param base: The base of the number. The step between each value.
        :return: The rounded number.
        """
        return round(base * round(float(x) / base), prec)

    def flipImage(self):
        """
        This function is used to laterally flip the image from left to right. It is called when the user clicks on the
        flip button. It doesn't flip the rectangles.

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
        This function is used to set the contrast of the image with the slider. It is called when the user enters a
        numeric value in it's associated lineEdit. If the value is below 60, the image's colors will be reversed. If the
        value is above 60, the image's colors will be darker. The way Image.Contrast() works is that, depending on the
        value you input, it will thicken the pixels that are darker or lighter.

        :return: None
        """
        if self.ui.contrastLineEdit.text() == "":
            return
        contrast_value = int(self.ui.contrastLineEdit.text())
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
        It writes down the rectangles' coordinates in the "_previous_rectangles_data.txt" file.

        :return: None
        """
        if self.ui.bitmap_label.bitmap_image is not None:
            while self.ui.bitmap_label.scale > 1:
                self.ui.bitmap_label.onZoomOut()
            with open("_previous_rectangles_data.txt", 'w') as file:
                for rectangle in self.ui.rectangles:
                    str_iteration = str(rectangle.getRect()) + '\n'
                    file.write(str_iteration)
                    file.flush()
            file.close()
        QCoreApplication.exit(0)

    def setConversionFactor(self):
        """
        This function is used to set the conversion factor that is entered in its line edit. It updates the value of
        each sample box and the mouse tracker

        :return: None
        """
        if self.isFractionValid(self.ui.conversion_factor_line_edit.text()):
            self.ui.value_type = self.convertToFloat(self.ui.conversion_factor_line_edit.text())
        else:
            try:
                self.ui.value_type = float(self.ui.conversion_factor_line_edit.text())
            except ValueError:
                pass
        for sample_group_box in self.ui.sample_group_boxes:
            sample_group_box.updateLineEdits()

    @staticmethod
    def convertToFloat(frac_str):
        """
        This function is used to convert a string to a float.

        :param frac_str: The string to be converted.
        :return: The float value of the string.
        """
        try:
            return float(frac_str)
        except ValueError:
            num, denominator = frac_str.split('/')
            try:
                leading, num = num.split(' ')
                whole = float(leading)
            except ValueError:
                whole = 0
            frac = float(num) / float(denominator)
            return whole - frac if whole < 0 else whole + frac

    @staticmethod
    def isFractionValid(string):
        """
        This function is used to check if a string is a valid fraction. This only works with round numbers.

        :param string: The string to be checked.
        :return: True if the string is a valid fraction, False otherwise.
        """
        values = string.split('/')
        return len(values) == 2 and all(i.isdigit() for i in values)

    @staticmethod
    def saveFilePath(filePath):
        """
        This function is used to save the file path of the chosen file in the "_file_path.txt" file.

        :param filePath: The file path of the chosen file.
        :return: None
        """
        path = filePath.rsplit("/", 1)[0]
        with open("_file_path.txt", 'w') as file:
            file.write(path)
            file.flush()
            file.close()

    def openFilePath(self) -> str:
        """
        This function is used to open and read the file path of the previously chosen file in the "_file_path.txt" file.

        :return: The file path of the previously chosen file.
        """
        file_exists = exists("_file_path.txt")
        if file_exists:
            with open("_file_path.txt", "r") as f:
                self.ui.file_path = f.readline()
                return self.ui.file_path
