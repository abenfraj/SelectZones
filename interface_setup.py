from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QScrollArea, QSlider

from bitmap_label import BitmapLabel
from mouse_tracker import MouseTracker


class Ui_SelectZones(object):
    """
    This class is used to create the interface.
    """

    def __init__(self):
        """
        This function is used to initialize the interface.
        """

        self.vert_lay = None  # Vertical layout
        self.scrollAreaWidgetContents_2 = None  # Scroll area widget contents
        self.groupBox = None  # Group box
        self.verticalLayout_2 = None  # Vertical layout
        self.verticalLayoutWidget = None  # Vertical layout widget
        self.contrast_slider = None  # Contrast slider
        self.scrollArea_2 = None  # Scroll area
        self.horizontalSlider = None  # Horizontal slider
        self.contrastValueLabel = None  # Contrast value label
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
        self.number_format = "%d"  # type str
        self.conversion_factor_label = None  # type QWidget.QLabel
        self.conversion_factor_line_edit = None  # type QWidget.QLineEdit
        self.conversion_factor_button = None  # type QtWidgets.QPushButton
        self.value_type = 100  # type int

    def retranslateUi(self, SelectZones):
        """
        This function is used to translate the interface. It displays the titles and icons of every widget.

        :param SelectZones: The interface.
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate
        SelectZones.setWindowTitle(_translate("SelectZones", "SelectZones"))
        SelectZones.setWindowIcon(QIcon("CNRS_logo.png"))
        self.quit_button.setText(_translate("SelectZones", "Quit"))
        self.select_bitmap_button.setText(_translate("SelectZones", "Choose Bitmap"))
        self.flip_image_button.setText(_translate("SelectZones", "Flip Image"))
        self.save_bmp_data_button.setText(_translate("SelectZones", "Save selected zones"))
        self.contrast_slider.setText(_translate("SelectZones", "Contrast"))
        self.conversion_factor_label.setText(_translate("SelectZones", "Conversion factor (pixel per millimeter)\nfactor 100 by default"))
        self.conversion_factor_button.setText(_translate("SelectZones", "Apply"))

    def setupUi(self, SelectZones):
        """
        This function is used to create/define the interface.

        :param SelectZones: The interface.
        :return: None
        """
        SelectZones.setObjectName("SelectZones")
        SelectZones.resize(1920, 1080)
        SelectZones.showMaximized()
        self.centralwidget = QtWidgets.QWidget(SelectZones)
        self.centralwidget.setObjectName("centralwidget")

        self.quit_button = QtWidgets.QPushButton(self.centralwidget)
        self.quit_button.setGeometry(QtCore.QRect(1500, 20, 341, 28))
        self.quit_button.setObjectName("quit_button")

        self.select_bitmap_button = QtWidgets.QPushButton(self.centralwidget)
        self.select_bitmap_button.setGeometry(QtCore.QRect(60, 20, 341, 31))
        self.select_bitmap_button.setObjectName("select_bitmap_button")

        self.flip_image_button = QtWidgets.QPushButton(self.centralwidget)
        self.flip_image_button.setGeometry(QtCore.QRect(420, 20, 341, 31))
        self.flip_image_button.setObjectName("flip_image_button")
        self.flip_image_button.setEnabled(False)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 70, 1861, 391))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1859, 389))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")

        self.bitmap_label = BitmapLabel(self)
        self.bitmap_label.setText("")
        self.bitmap_label.setAlignment(QtCore.Qt.AlignCenter)
        self.bitmap_label.setObjectName("bitmap_label")

        self.verticalLayout.addWidget(self.bitmap_label)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.contrast_slider = QtWidgets.QLabel(self.centralwidget)
        self.contrast_slider.setGeometry(QtCore.QRect(750, 500, 55, 16))
        self.contrast_slider.setObjectName("Contrast slider")

        self.conversion_factor_button = QtWidgets.QPushButton(self.centralwidget)
        self.conversion_factor_button.setGeometry(QtCore.QRect(1750, 500, 100, 25))
        self.conversion_factor_button.setObjectName("conversion_factor_button")
        self.conversion_factor_button.setEnabled(False)

        self.conversion_factor_label = QtWidgets.QLabel(self.centralwidget)
        self.conversion_factor_label.setGeometry(QtCore.QRect(1325, 495, 250, 40))
        self.conversion_factor_label.setObjectName("conversion_factor_label")

        self.conversion_factor_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.conversion_factor_line_edit.setGeometry(QtCore.QRect(1575, 500, 150, 25))
        self.conversion_factor_line_edit.setObjectName("conversion_factor_line_edit")
        self.conversion_factor_line_edit.setEnabled(False)

        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(820, 500, 250, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setMinimum(50)
        self.horizontalSlider.setMaximum(500)
        self.horizontalSlider.setValue(50)
        self.horizontalSlider.setTickInterval(1)
        self.horizontalSlider.setSingleStep(10)
        self.horizontalSlider.setPageStep(10)
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

        self.save_bmp_data_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_bmp_data_button.setGeometry(
            QtCore.QRect(780, 780, 331, 28))
        self.save_bmp_data_button.setObjectName("save_bmp_data_button")

        self.mousetracker_label = QtWidgets.QLabel(self.centralwidget)
        self.mousetracker_label.setGeometry(
            QtCore.QRect(780, 40, 300, 16))
        self.mousetracker_label.setText("")
        self.mousetracker_label.setObjectName("mousetracker_label")

        SelectZones.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(SelectZones)
        self.statusbar.setObjectName("statusbar")
        SelectZones.setStatusBar(self.statusbar)

        self.mouse_tracker = MouseTracker(self.bitmap_label)

        self.retranslateUi(SelectZones)
        QtCore.QMetaObject.connectSlotsByName(SelectZones)
