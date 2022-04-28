from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QGridLayout


class SampleGroupBox(QtWidgets.QWidget):
    def __init__(self, ui, sample_number):
        super(SampleGroupBox, self).__init__()

        self.grid = None
        self.radioButton = None
        self.groupBox = None

        self.labelX0 = None
        self.labelY0 = None
        self.labelXF = None
        self.labelYF = None

        self.lineEditX0 = None
        self.lineEditY0 = None
        self.lineEditXF = None
        self.lineEditYF = None

        self.ui = ui
        self.sample_number = sample_number

        self.rectangle = self.ui.rectangles[-1]
        self.scrollAreaWidgetContents = self.ui.scrollAreaWidgetContents
        self.centralwidget = self.ui.centralwidget
        self.scrollArea_2 = self.ui.scrollArea_2

        self.init_ui()

    def init_ui(self):
        self.labelX0 = QtWidgets.QLabel(self.groupBox)
        self.labelY0 = QtWidgets.QLabel(self.groupBox)
        self.labelXF = QtWidgets.QLabel(self.groupBox)
        self.labelYF = QtWidgets.QLabel(self.groupBox)

        self.lineEditX0 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditY0 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditXF = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditYF = QtWidgets.QLineEdit(self.groupBox)

        lay = QtWidgets.QVBoxLayout(self)
        box = QtWidgets.QGroupBox()
        lay.addWidget(box)

        self.radioButton = QtWidgets.QRadioButton()
        self.radioButton.setGeometry(QtCore.QRect(10, 20, 95, 21))
        self.radioButton.setObjectName("radioButton" + str(self.sample_number))

        self.labelX0.setGeometry(QtCore.QRect(130, 20, 21, 21))
        self.labelX0.setObjectName("labelX0" + str(self.sample_number))

        self.labelY0.setGeometry(QtCore.QRect(230, 20, 21, 21))
        self.labelY0.setObjectName("labelY0" + str(self.sample_number))
        self.labelXF.setGeometry(QtCore.QRect(370, 20, 21, 21))
        self.labelXF.setObjectName("labelXF" + str(self.sample_number))
        self.labelYF.setGeometry(QtCore.QRect(460, 20, 21, 21))
        self.labelYF.setObjectName("labelYF" + str(self.sample_number))

        self.lineEditX0.setGeometry(QtCore.QRect(150, 20, 61, 22))
        self.lineEditX0.setObjectName("lineEditX0" + str(self.sample_number))
        self.lineEditX0.setInputMask("00000")
        self.lineEditX0.textEdited[str].connect(self.onX0Changed)

        self.lineEditY0.setGeometry(QtCore.QRect(250, 20, 61, 22))
        self.lineEditY0.setObjectName("lineEditY0" + str(self.sample_number))
        self.lineEditY0.setInputMask("00000")
        self.lineEditY0.textEdited[str].connect(self.onY0Changed)

        self.lineEditXF.setGeometry(QtCore.QRect(390, 20, 61, 22))
        self.lineEditXF.setObjectName("lineEditXF" + str(self.sample_number))
        self.lineEditXF.setInputMask("00000")
        self.lineEditXF.textEdited[str].connect(self.onXFChanged)

        self.lineEditYF.setGeometry(QtCore.QRect(480, 20, 61, 22))
        self.lineEditYF.setObjectName("lineEditYF" + str(self.sample_number))
        self.lineEditYF.setInputMask("00000")
        self.lineEditYF.textEdited[str].connect(self.onYFChanged)

        self.radioButton.setText("Sample " + str(self.sample_number + 1))
        self.labelX0.setText("x0")
        self.labelY0.setText("y0")
        self.labelXF.setText("xf")
        self.labelYF.setText("yf")

        self.grid = QGridLayout()
        self.grid.addWidget(self.radioButton, 0, 0)
        self.grid.addWidget(self.labelX0, 0, 1)
        self.grid.addWidget(self.lineEditX0, 0, 2)
        self.grid.addWidget(self.labelY0, 0, 3)
        self.grid.addWidget(self.lineEditY0, 0, 4)
        self.grid.addWidget(self.labelXF, 0, 5)
        self.grid.addWidget(self.lineEditXF, 0, 6)
        self.grid.addWidget(self.labelYF, 0, 7)
        self.grid.addWidget(self.lineEditYF, 0, 8)

        box.setLayout(self.grid)
        box.setFixedSize(609, 59)

        self.ui.vert_lay.addWidget(self)

    def setX0(self):
        real_width, real_height = self.ui.original_image.size
        x0 = self.rectangle.x()
        self.lineEditX0.setText("%d" % (real_width * x0 / self.ui.bitmap_label.size().width()))

    def setY0(self):
        real_width, real_height = self.ui.original_image.size
        y0 = self.rectangle.y()
        self.lineEditY0.setText("%d" % (real_height * y0 / self.ui.bitmap_label.size().height()))

    def setXF(self):
        real_width, real_height = self.ui.original_image.size
        xf = self.rectangle.x() + self.rectangle.width()
        self.lineEditXF.setText("%d" % (real_width * xf / self.ui.bitmap_label.size().width()))

    def setYF(self):
        real_width, real_height = self.ui.original_image.size
        yf = self.rectangle.y() + self.rectangle.height()
        self.lineEditYF.setText("%d" % (real_height * yf / self.ui.bitmap_label.size().height()))

    def onX0Changed(self, text):
        real_width, real_height = self.ui.original_image.size
        self.rectangle.setX(int(self.ui.bitmap_label.size().width() * int(text) / real_width))

    def onY0Changed(self, text):
        real_width, real_height = self.ui.original_image.size
        self.rectangle.setY(int(self.ui.bitmap_label.size().height() * int(text) / real_height))

    # TODO: BUG dans le calcul rectangle.setWidth
    def onXFChanged(self, text):
        real_width, real_height = self.ui.original_image.size
        self.rectangle.setWidth(int(self.ui.bitmap_label.size().width() * int(text) / real_width))

    # TODO: BUG dans le calcul rectangle.setHeight
    def onYFChanged(self, text):
        real_width, real_height = self.ui.original_image.size
        self.rectangle.setHeight(int(self.ui.bitmap_label.size().height() * int(text) / real_height))
        print(str(int(self.ui.bitmap_label.size().height() * int(text) / real_height)))

    def updateRectangle(self, rectangle):
        self.rectangle = rectangle
