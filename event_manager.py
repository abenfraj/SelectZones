from PIL import Image
from PIL.Image import Resampling
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap, QWheelEvent
from PyQt5.QtWidgets import QFileDialog, QWidget, QMainWindow
from numpy import asarray

Image.MAX_IMAGE_PIXELS = None


class Event_Manager(QMainWindow):
    def __init__(self, ui):
        super(Event_Manager, self).__init__()
        self.ui = ui
        self.connectAllWidgets()

    def connectAllWidgets(self):
        self.ui.select_bitmap_button.clicked.connect(
            self.openFileDialog)  # Connect the select bitmap button to the openFileNameDialog function
        self.ui.quit_button.clicked.connect(
            QCoreApplication.instance().quit)  # Connect the quit button to the close function from QMainWindow
        self.ui.save_bmp_data_button.clicked.connect(
            self.saveBmpData)  # Connect the save bitmap data button to the saveBmpData function
        self.ui.mouse_tracker.positionChanged.connect(
            self.on_positionChanged)  # Connect the mouse tracker to the on_positionChanged function

    def openFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Open File",
                                                  "D:\\Workspace\\LERMA\\SelectZones",
                                                  "BMP files (*.bmp);;PNG files (*.png);;All Files (*)",
                                                  )  # Get the file name from the file explorer
        if fileName:
            self.ui.bitmap_image = Image.open(fileName)
            self.ui.bitmap_data = asarray(self.ui.bitmap_image)

            resized_image = self.ui.bitmap_image.resize(
                (self.ui.bitmap_label.width(), self.ui.bitmap_label.height()),
                resample=Resampling.BILINEAR)
            resized_image.save("_resized.bmp")
            self.ui.bitmap_label.bitmap_image = resized_image
            # TODO : DeprecationWarning: FLIP_LEFT_RIGHT is deprecaqted and will be removed in Pillow 10 (2023-07-01). Use Transpose.FLIP_LEFT_RIGHT instead
            # im = im.transpose(method=Image.FLIP_LEFT_RIGHT)

            self.ui.pixmap = QPixmap("_resized.bmp")
            self.ui.bitmap_label.pixmap = self.ui.pixmap
            self.ui.bitmap_label.setPixmap(self.ui.pixmap)  # Set the bitmap label's pixmap to the QPixmap object
            self.ui.bitmap_image.close()
            self.ui.image_is_displayed = True

    def saveBmpData(self):
        fileName, _ = QFileDialog.getSaveFileName(self,
                                                  "Save File",
                                                  "D:\\Workspace\\LERMA\\SelectZones",
                                                  "TXT files (*.txt)",
                                                  )  # Get the file name from the file explorer
        if fileName:
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
    def on_positionChanged(self, pos):
        self.ui.mousetracker_label.setText("x: %d, y: %d" % (pos.x(), pos.y()))
