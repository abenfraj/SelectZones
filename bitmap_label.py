from PyQt5 import QtCore
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QLabel


# This is a subclass of QLabel that allows the program to track the events happening on the label.
class BitmapLabel(QLabel):
    # This is the constructor for the class.
    def __init__(self, parent=None):
        super().__init__(parent)  # Call the parent class's (QLabel) constructor
        self.bitmap_image = None  # This is the image that will be displayed on the label
        self.pixmap = None  # This is the pixmap that will be displayed on the label

        self.x0 = 0  # These are the coordinates of the mouse press event (top)
        self.y0 = 0  # These are the coordinates of the mouse press event (left)
        self.x1 = 0  # These are the coordinates of the mouse release event (bottom)
        self.y1 = 0  # These are the coordinates of the mouse release event (right)
        self.flag = False  # This is a flag that indicates whether the mouse is pressed or not
        self.scale = 1.0  # This is the scale of the image

        self.begin = QtCore.QPoint()  # This is the point where the mouse press event occurred
        self.end = QtCore.QPoint()  # This is the point where the mouse release event occurred
        self.show()  # Show the label

    # This method is called when the mouse is pressed.
    def mousePressEvent(self, event):
        self.flag = True  # Set the flag to true so that the mouse move event will occur
        self.x0 = event.x()  # Set the x0 coordinate to the x coordinate of the mouse press event
        self.y0 = event.y()  # Set the y0 coordinate to the y coordinate of the mouse press event

    # This method is called when the mouse is released.
    def mouseReleaseEvent(self, event):
        self.flag = False  # Set the flag to false so that the mouse move event will not occur

    # This method is called when the mouse is moved.
    def mouseMoveEvent(self, event):
        if self.flag:  # If the mouse is pressed
            self.x1 = event.x()  # Set the x1 coordinate to the x coordinate of the mouse move event
            self.y1 = event.y()  # Set the y1 coordinate to the y coordinate of the mouse move event
            self.update()  # Update the label

    # This method draws the rectangle that is drawn by the mouse.
    def paintEvent(self, event):
        super().paintEvent(event)  # Call the parent class's paintEvent method
        rect = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))  # Create a QRect object
        painter = QPainter(self)  # Create a QPainter object
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))  # Set the pen to red and 2 pixels wide
        painter.drawRect(rect)  # Draw the rectangle

    # This method sets the image that will be displayed on the label.
    def wheelEvent(self, event):
        if self is not None:  # If the image is not None
            if event.angleDelta().y() > 0:  # If the mouse wheel is rotated up
                if self.bitmap_image is not None:  # If the image is not None
                    self.on_zoom_in()  # Call the zoom in method
            else:  # If the mouse wheel is rotated down
                if self.bitmap_image is not None:  # If the image is not None
                    self.on_zoom_out()  # Call the zoom out method

    # This method is called when the user zooms in with his mouse wheel.
    def on_zoom_in(self):
        self.scale *= 2  # Increase the scale by 2
        self.resize_image()  # Resize the image

    # This method is called when the user zooms out with his mouse wheel.
    def on_zoom_out(self):
        self.scale /= 2  # Decrease the scale by 2
        self.resize_image()  # Resize the image

    # This method resizes the image depending on the scale.
    def resize_image(self):
        print(self.pixmap)  # Print the pixmap
        size = self.pixmap.size()  # Get the size of the pixmap
        scaled_pixmap = self.pixmap.scaled(self.scale * size)  # Scale the pixmap
        self.setPixmap(scaled_pixmap)  # Set the pixmap to the scaled pixmap
