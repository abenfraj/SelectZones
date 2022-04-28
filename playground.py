from PyQt5 import QtCore, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(415, 213)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 801, 601))
        self.groupBox.setObjectName("groupBox")

        self.scrollArea = QtWidgets.QScrollArea(self.groupBox)
        self.scrollArea.move(10, 30)
        self.scrollArea.setFixedWidth(380)
        self.scrollArea.setMinimumHeight(160)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        random_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        random_label.setGeometry(QtCore.QRect(0, 0, 141, 16))
        random_label.setText("Rectangle ")
        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

class CompetencyBox(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(CompetencyBox, self).__init__(parent)
        self.compCodeLineEdit = QtWidgets.QLineEdit()
        self.compDescrpTextEdit = QtWidgets.QTextEdit()
        lay = QtWidgets.QVBoxLayout(self)
        box = QtWidgets.QGroupBox()
        lay.addWidget(box)
        form_lay = QtWidgets.QFormLayout()
        form_lay.addRow(QtWidgets.QLabel("Код: "), self.compCodeLineEdit)
        form_lay.addRow(QtWidgets.QLabel("Описание: "), self.compDescrpTextEdit)
        box.setLayout(form_lay)
        box.setFixedSize(510, 240)

class Test_Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Test_Window, self).__init__(parent)
        self.setupUi(self)
        self.addBox(self.scrollAreaWidgetContents, CompetencyBox, 4)

    def addBox(self, parent, element, number):
        vert_lay = QtWidgets.QVBoxLayout(parent)
        for i in range(number):
            vert_lay.addWidget(element())
        vert_lay.setSpacing(5)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Test_Window()
    w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())