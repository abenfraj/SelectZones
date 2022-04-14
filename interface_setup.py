from PyQt5 import QtCore, QtWidgets

from bitmap_label import BitmapLabel
from mouse_tracker import MouseTracker


class Ui_SelectZones(object):
    def __init__(self):
        self.centralwidget = None
        self.quit_button = None
        self.quit_button = None
        self.select_bitmap_button = None
        self.scrollArea = None
        self.scrollAreaWidgetContents_2 = None
        self.verticalLayout = None
        self.save_bmp_data_button = None
        self.bitmap_label = None
        self.mousetracker_label = None
        self.statusbar = None
        self.mouse_tracker = None

    def retranslateUi(self, SelectZones):
        _translate = QtCore.QCoreApplication.translate
        SelectZones.setWindowTitle(_translate("SelectZones", "SelectZones"))
        self.quit_button.setText(_translate("SelectZones", "Quit"))
        self.select_bitmap_button.setText(_translate("SelectZones", "Choose Bitmap"))
        self.save_bmp_data_button.setText(_translate("SelectZones", "Save Bitmap Data"))

    def setupUi(self, SelectZones):
        SelectZones.setObjectName("SelectZones")
        SelectZones.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(SelectZones)
        self.centralwidget.setObjectName("centralwidget")

        self.quit_button = QtWidgets.QPushButton(self.centralwidget)
        self.quit_button.setGeometry(QtCore.QRect(1500, 20, 341, 28))
        self.quit_button.setObjectName("quit_button")

        self.select_bitmap_button = QtWidgets.QPushButton(self.centralwidget)
        self.select_bitmap_button.setGeometry(QtCore.QRect(60, 20, 341, 31))
        self.select_bitmap_button.setObjectName("select_bitmap_button")

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 70, 1861, 391))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 1859, 389))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout.setObjectName("verticalLayout")

        self.bitmap_label = BitmapLabel()
        self.bitmap_label.setText("")
        self.bitmap_label.setAlignment(QtCore.Qt.AlignCenter)
        self.bitmap_label.setObjectName("bitmap_label")

        self.verticalLayout.addWidget(self.bitmap_label)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.save_bmp_data_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_bmp_data_button.setGeometry(QtCore.QRect(780, 780, 331, 28))
        self.save_bmp_data_button.setObjectName("save_bmp_data_button")

        self.mousetracker_label = QtWidgets.QLabel(self.centralwidget)
        self.mousetracker_label.setGeometry(QtCore.QRect(780, 40, 141, 16))
        self.mousetracker_label.setText("")
        self.mousetracker_label.setObjectName("mousetracker_label")

        SelectZones.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(SelectZones)
        self.statusbar.setObjectName("statusbar")
        SelectZones.setStatusBar(self.statusbar)

        self.mouse_tracker = MouseTracker(self.bitmap_label)

        self.retranslateUi(SelectZones)
        QtCore.QMetaObject.connectSlotsByName(SelectZones)
