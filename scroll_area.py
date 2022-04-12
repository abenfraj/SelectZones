from PyQt5 import QtCore
from PyQt5.QtWidgets import QScrollArea


class Scroller(QScrollArea):
    def __init__(self):
        QScrollArea.__init__(self)

    def wheelEvent(self, ev):
        if ev.type() == QtCore.QEvent.Wheel:
            ev.ignore()
