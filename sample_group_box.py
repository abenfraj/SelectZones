import os

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGridLayout


class SampleGroupBox(QtWidgets.QWidget):
    """
    This class is used to create a group box containing the rectangle coordinates.
    """

    def __init__(self, ui, sample_number):
        """
        This function is used to initialize the class.

        :param ui: The main window.
        :param sample_number: The number of the sample.
        """

        super(SampleGroupBox, self).__init__()
        self.correctButton = None
        self.grid = None
        self.sample_name = None
        self.groupBox = None

        self.labelX0 = None
        self.labelY0 = None
        self.labelXF = None
        self.labelYF = None

        self.lineEditX0 = None
        self.lineEditY0 = None
        self.lineEditXF = None
        self.lineEditYF = None

        self.removeButton = None

        self.ui = ui
        self.sample_number = sample_number

        self.rectangle = self.ui.rectangles[-1]
        self.scrollAreaWidgetContents = self.ui.scrollAreaWidgetContents
        self.centralwidget = self.ui.centralwidget
        self.scrollArea_2 = self.ui.scrollArea_2

        self.initUi()

    def initUi(self):
        """
        This function is used to create/define the interface of this custom widget.

        :return: None
        """

        self.labelX0 = QtWidgets.QLabel(self.groupBox)
        self.labelY0 = QtWidgets.QLabel(self.groupBox)
        self.labelXF = QtWidgets.QLabel(self.groupBox)
        self.labelYF = QtWidgets.QLabel(self.groupBox)

        self.lineEditX0 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditY0 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditXF = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditYF = QtWidgets.QLineEdit(self.groupBox)

        self.removeButton = QtWidgets.QPushButton(self.groupBox)
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'Red-Close-Button-Transparent.png')
        self.removeButton.setIcon(QIcon(filename))
        self.removeButton.setIconSize(QtCore.QSize(20, 20))
        self.removeButton.clicked.connect(self.removeSample)

        self.correctButton = QtWidgets.QPushButton(self.groupBox)
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'Correct-Button.png')
        self.correctButton.setIcon(QIcon(filename))
        self.correctButton.setIconSize(QtCore.QSize(20, 20))
        self.correctButton.clicked.connect(self.correctSample)

        lay = QtWidgets.QVBoxLayout(self)
        box = QtWidgets.QGroupBox()
        lay.addWidget(box)

        self.sample_name = QtWidgets.QLabel()
        self.sample_name.setGeometry(QtCore.QRect(10, 20, 95, 21))
        self.sample_name.setObjectName("sample_name" + str(self.sample_number))

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
        self.lineEditX0.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r"^[+-]?((\d+(\.\d+)?)|(\.\d+))$")))
        self.lineEditX0.textEdited[str].connect(self.onX0Changed)

        self.lineEditY0.setGeometry(QtCore.QRect(250, 20, 61, 22))
        self.lineEditY0.setObjectName("lineEditY0" + str(self.sample_number))
        self.lineEditY0.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r"^[+-]?((\d+(\.\d+)?)|(\.\d+))$")))
        self.lineEditY0.textEdited[str].connect(self.onY0Changed)

        self.lineEditXF.setGeometry(QtCore.QRect(390, 20, 61, 22))
        self.lineEditXF.setObjectName("lineEditXF" + str(self.sample_number))
        self.lineEditXF.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r"^[+-]?((\d+(\.\d+)?)|(\.\d+))$")))
        self.lineEditXF.textEdited[str].connect(self.onXFChanged)

        self.lineEditYF.setGeometry(QtCore.QRect(480, 20, 61, 22))
        self.lineEditYF.setObjectName("lineEditYF" + str(self.sample_number))
        self.lineEditYF.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r"^[+-]?((\d+(\.\d+)?)|(\.\d+))$")))
        self.lineEditYF.textEdited[str].connect(self.onYFChanged)

        self.sample_name.setText("Sample " + str(self.sample_number + 1) + ":  ")
        self.labelX0.setText("x0")
        self.labelY0.setText("y0")
        self.labelXF.setText("xf")
        self.labelYF.setText("yf")

        self.grid = QGridLayout()
        self.grid.addWidget(self.sample_name, 0, 0)
        self.grid.addWidget(self.labelX0, 0, 1)
        self.grid.addWidget(self.lineEditX0, 0, 2)
        self.grid.addWidget(self.labelY0, 0, 3)
        self.grid.addWidget(self.lineEditY0, 0, 4)
        self.grid.addWidget(self.labelXF, 0, 5)
        self.grid.addWidget(self.lineEditXF, 0, 6)
        self.grid.addWidget(self.labelYF, 0, 7)
        self.grid.addWidget(self.lineEditYF, 0, 8)
        self.grid.addWidget(self.removeButton, 0, 9)
        self.grid.addWidget(self.correctButton, 0, 10)

        box.setLayout(self.grid)
        box.setFixedSize(609, 59)

        self.ui.vert_lay.addWidget(self)

    def setX0(self):
        """
        This function is used to set the x0 value of the sample.

        :return: None
        """

        x0 = self.rectangle.x()
        try:
            self.lineEditX0.setText("%.3f" % self.roundTo(
                "%.3f" % (((self.ui.real_width) * x0 / self.ui.bitmap_label.size().width()) / self.ui.value_type),
                base=1 / self.ui.value_type, prec=3)
                                    )
        except RuntimeError:
            pass

    def setY0(self):
        """
        This function is used to set the y0 value of the sample.

        :return: None
        """
        y0 = self.rectangle.y()
        try:
            self.lineEditY0.setText("%.3f" % self.roundTo(
                "%.3f" % (((self.ui.real_height) * y0 / self.ui.bitmap_label.size().height()) / self.ui.value_type),
                base=1 / self.ui.value_type, prec=3))
        except RuntimeError:
            pass

    def setXF(self):
        """
        This function is used to set the xf value of the sample.

        :return: None
        """
        xf = self.rectangle.x() + self.rectangle.width()
        try:
            self.lineEditXF.setText("%.3f" % self.roundTo(
                "%.3f" % (((self.ui.real_width) * xf / self.ui.bitmap_label.size().width()) / self.ui.value_type),
                base=1 / self.ui.value_type, prec=3))
        except RuntimeError:
            pass

    def setYF(self):
        """
        This function is used to set the yf value of the sample.

        :return: None
        """

        yf = self.rectangle.y() + self.rectangle.height()
        try:
            self.lineEditYF.setText("%.3f" % self.roundTo(
                "%.3f" % (((self.ui.real_height) * yf / self.ui.bitmap_label.size().height()) / self.ui.value_type),
                base=1 / self.ui.value_type, prec=3))
        except RuntimeError:
            pass

    @staticmethod
    def roundTo(x, prec, base):
        return round(base * round(float(x) / base), prec)

    def onX0Changed(self, text):
        """
        This function is used to set the x0 value of the sample when the text is changed.

        :param text: The x0 value of the sample.
        :return: None
        """

        try:
            # rounded_value = str(self.roundTo(text, base=1 / self.ui.value_type, prec=3))
            # self.lineEditX0.setText(rounded_value)
            self.rectangle.setX(
                int(self.ui.bitmap_label.size().width() * (float(text) * self.ui.value_type) / self.ui.real_width))
            if self.rectangle == self.ui.rectangles[-1]:
                self.ui.bitmap_label.setBeginning(QPoint(self.rectangle.x(), self.rectangle.y()))
        except ValueError:
            pass

        self.ui.bitmap_label.update()

    def onY0Changed(self, text):
        """
        This function is used to set the y0 value of the sample when the text is changed.

        :param text: The y0 value of the sample.
        :return: None
        """

        try:
            self.rectangle.setY(
                int(self.ui.bitmap_label.size().height() * (float(text) * self.ui.value_type) / self.ui.real_height))
            if self.rectangle == self.ui.rectangles[-1]:
                self.ui.bitmap_label.setBeginning(QPoint(self.rectangle.x(), self.rectangle.y()))
            self.ui.bitmap_label.update()
        except ValueError:
            pass

    def onXFChanged(self, text):
        """
        This function is used to set the xf value of the sample when the text is changed.

        :param text: The xf value of the sample.
        :return: None
        """

        try:
            self.rectangle.setWidth(
                int(self.ui.bitmap_label.size().width() * (
                        float(text) * self.ui.value_type) / self.ui.real_width) - self.rectangle.x())
            if self.rectangle == self.ui.rectangles[-1]:
                self.ui.bitmap_label.setEnd(
                    QPoint(self.rectangle.x() + self.rectangle.width(), self.rectangle.y() + self.rectangle.height()))
            self.ui.bitmap_label.update()
        except ValueError:
            pass

    def onYFChanged(self, text):
        """
        This function is used to set the yf value of the sample when the text is changed.

        :param text: The yf value of the sample.
        :return: None
        """

        try:
            self.rectangle.setHeight(
                int(self.ui.bitmap_label.size().height() * (
                        float(text) * self.ui.value_type) / self.ui.real_height) - self.rectangle.y())
            if self.rectangle == self.ui.rectangles[-1]:
                self.ui.bitmap_label.setEnd(
                    QPoint(self.rectangle.x() + self.rectangle.width(), self.rectangle.y() + self.rectangle.height()))
            self.ui.bitmap_label.update()
        except ValueError:
            pass

    def updateRectangle(self, rectangle):
        """
        This function is used to update the rectangle.

        :param rectangle: The rectangle to update.
        :return: None
        """

        self.rectangle = rectangle

    def updateLineEdits(self):
        """
        This function is used to update the line edits.

        :return: None
        """

        self.setX0()
        self.setY0()
        self.setXF()
        self.setYF()

    def removeSample(self):
        """
        This function is used to remove the sample.

        :return: None
        """

        self.ui.vert_lay.removeWidget(self)
        self.deleteLater()
        self.ui.rectangles.remove(self.rectangle)
        self.ui.sample_group_boxes.remove(self)
        self.ui.bitmap_label.update()
        new_beginning = QPoint()
        new_end = QPoint()
        if len(self.ui.rectangles) != 0:
            new_beginning = QPoint(self.ui.rectangles[-1].getCoords()[0], self.ui.rectangles[-1].getCoords()[1])
            new_end = QPoint(self.ui.rectangles[-1].getCoords()[2], self.ui.rectangles[-1].getCoords()[3])
        self.ui.bitmap_label.setBeginning(new_beginning)
        self.ui.bitmap_label.setEnd(new_end)

    def correctSample(self):
        """
        This function is used to correct the values of the sample.

        :return: None
        """

        self.correctX0()
        self.correctY0()
        self.correctXF()
        self.correctYF()

    def correctX0(self):
        """
        This function is used to correct the x0 value of the sample.

        :return: None
        """
        x0 = self.rectangle.x()
        try:
            rounded_value = self.roundTo(self.lineEditX0.text(), base=1 / self.ui.value_type, prec=3)
            self.lineEditX0.setText("%.3f" % self.roundTo(
                "%.3f" % rounded_value,
                base=(1 / self.ui.value_type),
                prec=3))
        except RuntimeError:
            pass

    def correctY0(self):
        """
        This function is used to correct the x0 value of the sample.

        :return: None
        """
        y0 = self.rectangle.y()
        try:
            rounded_value = self.roundTo(self.lineEditY0.text(), base=1 / self.ui.value_type, prec=3)
            self.lineEditY0.setText("%.3f" % self.roundTo(
                "%.3f" % rounded_value,
                base=1 / self.ui.value_type, prec=3)
                                    )
        except RuntimeError:
            pass

    def correctXF(self):
        """
        This function is used to correct the x0 value of the sample.

        :return: None
        """
        try:
            rounded_value = str("%.3f" % self.roundTo(self.lineEditXF.text(), base=1 / self.ui.value_type, prec=3))
            self.lineEditXF.setText(rounded_value)
            self.rectangle.setWidth(
                int(self.ui.bitmap_label.size().width() * (
                        float(self.lineEditXF.text()) * self.ui.value_type) / self.ui.real_width) - self.rectangle.x())
            if self.rectangle == self.ui.rectangles[-1]:
                self.ui.bitmap_label.setEnd(
                    QPoint(self.rectangle.x() + self.rectangle.width(), self.rectangle.y() + self.rectangle.height()))
            self.ui.bitmap_label.update()
        except ValueError:
            pass

    def correctYF(self):
        """
        This function is used to correct the x0 value of the sample.

        :return: None
        """
        try:
            rounded_value = str("%.3f" % self.roundTo(self.lineEditYF.text(), base=1 / self.ui.value_type, prec=3))
            self.lineEditYF.setText(rounded_value)
            self.rectangle.setHeight(
                int(self.ui.bitmap_label.size().height() * (
                        float(self.lineEditYF.text()) * self.ui.value_type) / self.ui.real_height) - self.rectangle.y())
            if self.rectangle == self.ui.rectangles[-1]:
                self.ui.bitmap_label.setEnd(
                    QPoint(self.rectangle.x() + self.rectangle.width(), self.rectangle.y() + self.rectangle.height()))
            self.ui.bitmap_label.update()
        except ValueError:
            pass
