from PyQt5 import QtWidgets, QtCore


class SampleGroupBox:
    def __init__(self, ui, sample_number):
        super(SampleGroupBox, self).__init__()

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
        self.groupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setGeometry(QtCore.QRect(10, 20 + 50 * self.sample_number, 551, 51))
        self.groupBox.setObjectName("groupBox")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(10, 20, 95, 21))
        self.radioButton.setObjectName("radioButton")

        self.labelX0 = QtWidgets.QLabel(self.groupBox)
        self.labelX0.setGeometry(QtCore.QRect(130, 20, 21, 21))
        self.labelX0.setObjectName("labelX0")
        self.labelY0 = QtWidgets.QLabel(self.groupBox)
        self.labelY0.setGeometry(QtCore.QRect(230, 20, 21, 21))
        self.labelY0.setObjectName("labelY0")
        self.labelXF = QtWidgets.QLabel(self.groupBox)
        self.labelXF.setGeometry(QtCore.QRect(370, 20, 21, 21))
        self.labelXF.setObjectName("labelXF")
        self.labelYF = QtWidgets.QLabel(self.groupBox)
        self.labelYF.setGeometry(QtCore.QRect(460, 20, 21, 21))
        self.labelYF.setObjectName("labelYF")

        self.lineEditX0 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditX0.setGeometry(QtCore.QRect(150, 20, 61, 22))
        self.lineEditX0.setObjectName("lineEditX0")
        self.lineEditX0.setInputMask("00000")
        self.lineEditX0.textEdited[str].connect(self.onX0Changed)

        self.lineEditY0 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditY0.setGeometry(QtCore.QRect(250, 20, 61, 22))
        self.lineEditY0.setObjectName("lineEditY0")
        self.lineEditY0.setInputMask("00000")
        self.lineEditY0.textEdited[str].connect(self.onY0Changed)

        self.lineEditXF = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditXF.setGeometry(QtCore.QRect(390, 20, 61, 22))
        self.lineEditXF.setObjectName("lineEditXF")
        self.lineEditXF.setInputMask("00000")
        self.lineEditXF.textEdited[str].connect(self.onXFChanged)

        self.lineEditYF = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditYF.setGeometry(QtCore.QRect(480, 20, 61, 22))
        self.lineEditYF.setObjectName("lineEditYF")
        self.lineEditYF.setInputMask("00000")
        self.lineEditYF.textEdited[str].connect(self.onYFChanged)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents)

        self.groupBox.setTitle("Sample 1")
        self.radioButton.setText("Select")
        self.labelX0.setText("x0")
        self.labelY0.setText("y0")
        self.labelXF.setText("xf")
        self.labelYF.setText("yf")

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

    def onXFChanged(self, text):
        real_width, real_height = self.ui.original_image.size
        self.rectangle.setWidth(int(self.ui.bitmap_label.size().width() * int(text) / real_width))

    def onYFChanged(self, text):
        real_width, real_height = self.ui.original_image.size
        self.rectangle.setHeight(int(self.ui.bitmap_label.size().height() * int(text) / real_height))

    def updateRectangle(self, rectangle):
        self.rectangle = rectangle
