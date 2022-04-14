from PyQt5 import QtCore
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QLabel


class BitmapLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bitmap_image = None
        self.pixmap = None

        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.flag = False
        self.scale = 1.0

        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.show()

    def mousePressEvent(self, event):
        print("mousePressEvent")
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()
        # Mouse release event

    def mouseReleaseEvent(self, event):
        print("mouseReleaseEvent")
        self.flag = False
        # Mouse movement events

    def mouseMoveEvent(self, event):
        print("mouseMoveEvent")
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        rect = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.drawRect(rect)

    def wheelEvent(self, event):
        if self is not None:
            if event.angleDelta().y() > 0:
                if self.bitmap_image is not None:
                    self.on_zoom_in()
            else:
                if self.bitmap_image is not None:
                    self.on_zoom_out()

    def on_zoom_in(self):
        self.scale *= 2
        self.resize_image()

    def on_zoom_out(self):
        self.scale /= 2
        self.resize_image()

    def resize_image(self):
        print(self.pixmap)
        size = self.pixmap.size()
        scaled_pixmap = self.pixmap.scaled(self.scale * size)
        self.setPixmap(scaled_pixmap)
