from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QScrollArea, QSlider

from bitmap_label import BitmapLabel
from mouse_tracker import MouseTracker


# This class is used to create the interface for the application.


class Ui_SelectZones(object):
    # Initialize each of the widgets in the interface.
    def __init__(self):
        self.vert_lay = None
        self.scrollAreaWidgetContents_2 = None
        self.groupBox = None
        self.verticalLayout_2 = None
        self.verticalLayoutWidget = None
        self.contrast_slider = None
        self.scrollArea_2 = None
        self.horizontalSlider = None
        self.contrastValueLabel = None
        self.centralwidget = None  # type QtWidgets.QWidget
        self.quit_button = None  # type QtWidgets.QPushButton
        self.flip_image_button = None  # type QtWidgets.QPushButton
        self.flipped = False  # type bool
        self.select_bitmap_button = None  # type QtWidgets.QPushButton
        self.scrollArea = None  # type QtWidgets.QScrollArea
        self.scrollAreaWidgetContents = None  # type QtWidgets.QWidget
        self.verticalLayout = None  # type QtWidgets.QVBoxLayout
        self.save_bmp_data_button = None  # type QtWidgets.QPushButton
        self.bitmap_label = None  # type QWidget.QLabel
        self.bitmap_data = None  # type list
        self.mousetracker_label = None  # type MouseTracker
        self.statusbar = None  # type QtWidgets.QStatusBar
        self.mouse_tracker = None  # type MouseTracker (made in mouse_tracker.py)
        self.image_is_displayed = False  # type bool
        self.rectangles = []  # type list of Rectangle
        self.sample_group_boxes = []  # type list of QGroupBox
        self.original_image = None  # type QtGui.QImage

    # This function is used to translate the interface.
    def retranslateUi(self, SelectZones):
        _translate = QtCore.QCoreApplication.translate
        SelectZones.setWindowTitle(_translate("SelectZones", "SelectZones"))  # Set the title of the window.
        SelectZones.setWindowIcon(QIcon("CNRS_logo.png"))  # Set the icon of the window.
        self.quit_button.setText(_translate("SelectZones", "Quit"))  # Set the text of the quit button.
        self.select_bitmap_button.setText(
            _translate("SelectZones", "Choose Bitmap"))  # Set the text of the select bitmap button.
        self.flip_image_button.setText(
            _translate("SelectZones", "Flip Image"))  # Set the text of the flip image button.
        self.save_bmp_data_button.setText(
            _translate("SelectZones", "Save selected zones"))  # Set the text of the save bitmap data button.
        self.contrast_slider.setText(_translate("SelectZones", "Contrast"))

    # This function is used to set up the interface.
    def setupUi(self, SelectZones):
        SelectZones.setObjectName("SelectZones")  # Set the name of the window.
        SelectZones.resize(1920, 1080)  # Set the size of the window.
        SelectZones.showMaximized()  # Set to fullscreen on start.
        self.centralwidget = QtWidgets.QWidget(SelectZones)  # Create the central widget.
        self.centralwidget.setObjectName("centralwidget")  # Set the name of the central widget.

        self.quit_button = QtWidgets.QPushButton(self.centralwidget)  # Create the quit button.
        self.quit_button.setGeometry(QtCore.QRect(1500, 20, 341, 28))  # Set the geometry of the quit button.
        self.quit_button.setObjectName("quit_button")  # Set the name of the quit button.

        self.select_bitmap_button = QtWidgets.QPushButton(self.centralwidget)  # Create the select bitmap button.
        self.select_bitmap_button.setGeometry(
            QtCore.QRect(60, 20, 341, 31))  # Set the geometry of the select bitmap button.
        self.select_bitmap_button.setObjectName("select_bitmap_button")  # Set the name of the select bitmap button.

        self.flip_image_button = QtWidgets.QPushButton(self.centralwidget)  # Create the flip image button.
        self.flip_image_button.setGeometry(
            QtCore.QRect(420, 20, 341, 31))  # Set the geometry of the flip image button.
        self.flip_image_button.setObjectName("flip_image_button")  # Set the name of the flip image button.
        self.flip_image_button.setEnabled(False)  # Disable the flip image button.

        self.scrollArea = QScrollArea(self.centralwidget)  # Create the scroll area.
        self.scrollArea.setGeometry(QtCore.QRect(10, 70, 1861, 391))  # Set the geometry of the scroll area.
        self.scrollArea.setWidgetResizable(True)  # Set the scroll area to be resizable.
        self.scrollArea.setObjectName("scrollArea")  # Set the name of the scroll area.

        self.scrollAreaWidgetContents = QtWidgets.QWidget()  # Create the scroll area widget contents.
        self.scrollAreaWidgetContents.setGeometry(
            QtCore.QRect(0, 0, 1859, 389))  # Set the geometry of the scroll area widget contents.
        self.scrollAreaWidgetContents.setObjectName(
            "scrollAreaWidgetContents")  # Set the name of the scroll area widget contents.

        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)  # Create the vertical layout.
        self.verticalLayout.setObjectName("verticalLayout")  # Set the name of the vertical layout.

        self.bitmap_label = BitmapLabel(self)  # Create the bitmap label.
        self.bitmap_label.setText("")  # Set the text of the bitmap label.
        self.bitmap_label.setAlignment(QtCore.Qt.AlignCenter)  # Set the alignment of the bitmap label.
        self.bitmap_label.setObjectName("bitmap_label")  # Set the name of the bitmap label.

        self.verticalLayout.addWidget(self.bitmap_label)  # Add the bitmap label to the vertical layout.

        self.scrollArea.setWidget(
            self.scrollAreaWidgetContents)  # Set the scroll area to the scroll area widget contents.

        self.contrast_slider = QtWidgets.QLabel(self.centralwidget)
        self.contrast_slider.setGeometry(QtCore.QRect(750, 500, 55, 16))
        self.contrast_slider.setObjectName("Contrast slider")

        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(820, 500, 250, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setMinimum(50)
        self.horizontalSlider.setMaximum(500)
        self.horizontalSlider.setValue(50)
        self.horizontalSlider.setTickInterval(1)
        self.horizontalSlider.setSingleStep(10)  # arrow-key step-size
        self.horizontalSlider.setPageStep(10)  # mouse-wheel/page-key step-size
        self.horizontalSlider.setTickPosition(QSlider.TicksBelow)
        self.horizontalSlider.setEnabled(False)

        self.contrastValueLabel = QtWidgets.QLabel(self.centralwidget)
        self.contrastValueLabel.setGeometry(QtCore.QRect(1100, 500, 55, 16))
        self.contrastValueLabel.setObjectName("contrastValueLabel")

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 480, 670, 361))
        self.groupBox.setObjectName("groupBox")

        self.scrollArea_2 = QtWidgets.QScrollArea(self.groupBox)
        self.scrollArea_2.setFixedWidth(670)
        self.scrollArea_2.setMinimumHeight(361)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")

        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.vert_lay = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.vert_lay.setObjectName("vert_lay")

        self.save_bmp_data_button = QtWidgets.QPushButton(self.centralwidget)  # Create the save bitmap data button.
        self.save_bmp_data_button.setGeometry(
            QtCore.QRect(780, 780, 331, 28))  # Set the geometry of the save bitmap data button.
        self.save_bmp_data_button.setObjectName("save_bmp_data_button")  # Set the name of the save bitmap data button.

        self.mousetracker_label = QtWidgets.QLabel(self.centralwidget)  # Create the mouse tracker label.
        self.mousetracker_label.setGeometry(
            QtCore.QRect(780, 40, 300, 16))  # Set the geometry of the mouse tracker label.
        self.mousetracker_label.setText("")  # Set the text of the mouse tracker label.
        self.mousetracker_label.setObjectName("mousetracker_label")  # Set the name of the mouse tracker label.

        SelectZones.setCentralWidget(self.centralwidget)  # Set the central widget to the window.

        self.statusbar = QtWidgets.QStatusBar(SelectZones)  # Create the status bar.
        self.statusbar.setObjectName("statusbar")  # Set the name of the status bar.
        SelectZones.setStatusBar(self.statusbar)  # Set the status bar to the window.

        self.mouse_tracker = MouseTracker(self.bitmap_label)  # Create the mouse tracker.

        self.retranslateUi(SelectZones)  # Translate the UI.
        QtCore.QMetaObject.connectSlotsByName(SelectZones)  # Connect the slots.
