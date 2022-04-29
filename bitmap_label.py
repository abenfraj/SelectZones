from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QPoint, QRect, QSize
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QLabel

from sample_group_box import SampleGroupBox

FREE_STATE = 1
BUILDING_SQUARE = 2
BEGIN_SIDE_EDIT = 3
END_SIDE_EDIT = 4
TOP_SIDE_EDIT = 5
BOTTOM_SIDE_EDIT = 6

CURSOR_ON_BEGIN_SIDE = 1
CURSOR_ON_END_SIDE = 2
CURSOR_ON_TOP_SIDE = 3
CURSOR_ON_BOTTOM_SIDE = 4


# This is a subclass of QLabel that allows the program to track the events happening on the label.
class BitmapLabel(QLabel):
    # This is the constructor for the class.
    def __init__(self, ui):
        super().__init__()  # Call the parent class's (QLabel) constructor
        self.bitmap_image = None  # This is the image that will be displayed on the label
        self.pixmap = None  # This is the pixmap that will be displayed on the label
        self.scale = 1.0  # This is the scale of the image
        self.ui = ui
        self.rectangles = self.ui.rectangles  # This is a list of rectangles that will be drawn on the image
        self.sample_group_boxes = self.ui.sample_group_boxes  # This is a list of SampleGroupBox objects
        self.beginning = QtCore.QPoint()  # This is the point where the mouse press event occurred
        self.end = QtCore.QPoint()  # This is the point where the mouse release event occurred
        self.rectangle_border_color = None  # This is the color of the rectangle's border
        self.color_index = 0  # This is the index of the color in the colors list
        self.colors = [QColor(255, 0, 0, 170),
                       QColor(0, 255, 0, 170),
                       QColor(0, 0, 255, 170),
                       QColor(255, 255, 0, 170),
                       QColor(0, 255, 255, 170),
                       QColor(255, 0, 255, 170),
                       QColor(128, 0, 0, 170),
                       QColor(0, 128, 0, 170),
                       QColor(0, 0, 128, 170),
                       QColor(128, 128, 0, 170),
                       QColor(0, 128, 128, 170),
                       QColor(128, 0, 128, 170),
                       QColor(0, 0, 0, 170),
                       ]  # This is a list of colors
        self.state = FREE_STATE

        self.setMouseTracking(True)
        self.free_cursor_on_side = 0

        self.show()  # Show the label

    # This method draws the rectangle that is drawn by the mouse.
    def paintEvent(self, event):
        if self.bitmap_image is not None:  # If the image is not None
            super().paintEvent(event)  # Call the parent class's paintEvent method
            painter = QPainter(self)  # Create a QPainter object
            self.rectangle_border_color = self.colors[
                0]  # Set the rectangle's border color to the first color in the list

            painter.setPen(
                QPen(self.rectangle_border_color, 2))  # Set the pen's color to black and the pen's width to 1
            for rectangle in self.rectangles:
                painter.drawRect(rectangle)  # Draw the rectangle
                try:
                    self.rectangle_border_color = self.colors[self.rectangles.index(
                        rectangle) + 1]  # Set the rectangle's border color to the next color in the list
                    painter.setPen(QPen(self.rectangle_border_color, 2))
                except IndexError:
                    self.rectangle_border_color = self.colors[0]

            if not self.free_cursor_on_side:
                return

            painter.setPen(QPen(Qt.black, 3, Qt.DashLine))
            if self.free_cursor_on_side == CURSOR_ON_BEGIN_SIDE:
                end = QPoint(self.end)
                end.setX(self.beginning.x())
                painter.drawLine(self.beginning, end)

            elif self.free_cursor_on_side == CURSOR_ON_END_SIDE:
                beginning = QPoint(self.beginning)
                beginning.setX(self.end.x())
                painter.drawLine(self.end, beginning)

            elif self.free_cursor_on_side == CURSOR_ON_TOP_SIDE:
                end = QPoint(self.end)
                end.setY(self.beginning.y())
                painter.drawLine(self.beginning, end)

            elif self.free_cursor_on_side == CURSOR_ON_BOTTOM_SIDE:
                beginning = QPoint(self.beginning)
                beginning.setY(self.end.y())
                painter.drawLine(self.end, beginning)

    def cursor_on_side(self, e_pos) -> int:
        if not self.beginning.isNull() and not self.end.isNull():
            x1, x2 = sorted([self.beginning.x(), self.end.x()])
            y1, y2 = sorted([self.beginning.y(), self.end.y()])

            if x1 <= e_pos.x() <= x2:

                if abs(self.beginning.y() - e_pos.y()) <= 5:
                    return CURSOR_ON_TOP_SIDE
                elif abs(self.end.y() - e_pos.y()) <= 5:
                    return CURSOR_ON_BOTTOM_SIDE

            if y1 <= e_pos.y() <= y2:
                if abs(self.beginning.x() - e_pos.x()) <= 5:
                    return CURSOR_ON_BEGIN_SIDE
                elif abs(self.end.x() - e_pos.x()) <= 5:
                    return CURSOR_ON_END_SIDE
        return 0

    # This method is called when the mouse is pressed.
    def mousePressEvent(self, event):
        if self.bitmap_image is not None:  # If the image is not None
            super().mousePressEvent(event)  # Call the parent class's mousePressEvent method
            side = self.cursor_on_side(event.pos())
            if side == CURSOR_ON_BEGIN_SIDE:
                self.state = BEGIN_SIDE_EDIT
            elif side == CURSOR_ON_END_SIDE:
                self.state = END_SIDE_EDIT
            elif side == CURSOR_ON_TOP_SIDE:
                self.state = TOP_SIDE_EDIT
            elif side == CURSOR_ON_BOTTOM_SIDE:
                self.state = BOTTOM_SIDE_EDIT
            else:
                self.state = BUILDING_SQUARE
                self.rectangles.append(QRect(self.beginning, self.end))
                self.sample_group_boxes.append(SampleGroupBox(self.ui, len(self.rectangles) - 1))
                self.beginning = event.pos()
                self.end = event.pos()
                self.update()  # Update the label

    # This method is called when the mouse is released.
    def mouseReleaseEvent(self, event):
        if self.bitmap_image is not None:  # If the image is not None
            self.apply_event(event)
            self.state = FREE_STATE
            self.sample_group_boxes[-1].setX0()
            self.sample_group_boxes[-1].setY0()
            self.sample_group_boxes[-1].setXF()
            self.sample_group_boxes[-1].setYF()
            super().mouseReleaseEvent(event)  # Call the parent class's mouseReleaseEvent method

    # This method is called when the mouse is moved.
    def mouseMoveEvent(self, event):
        if self.bitmap_image is not None:  # If the mouse is pressed and the image is not None
            super().mouseMoveEvent(event)  # Call the parent class's mouseMoveEvent method
            if self.state == FREE_STATE:
                self.free_cursor_on_side = self.cursor_on_side(event.pos())
                if self.free_cursor_on_side == CURSOR_ON_BEGIN_SIDE or self.free_cursor_on_side == CURSOR_ON_END_SIDE:
                    self.setCursor(Qt.SizeHorCursor)
                elif self.free_cursor_on_side == CURSOR_ON_TOP_SIDE or self.free_cursor_on_side == CURSOR_ON_BOTTOM_SIDE:
                    self.setCursor(Qt.SizeVerCursor)
                else:
                    self.unsetCursor()
                self.update()
            else:
                self.apply_event(event)
                self.update()

    def apply_event(self, event):
        if self.state == BUILDING_SQUARE:  # If the state is BUILDING_SQUARE
            self.end = event.pos()  # Set the end point to the current position
            self.rectangles[-1] = QRect(self.beginning, self.end)  # Update the rectangle
            self.sample_group_boxes[-1].updateRectangle(self.rectangles[-1])  # Update the rectangle
        elif self.state == BEGIN_SIDE_EDIT:  # If the state is BEGIN_SIDE_EDIT
            self.beginning.setX(event.x())  # Set the beginning point's x to the current position's x
            self.rectangles[-1] = QRect(self.beginning, self.end)
            self.sample_group_boxes[-1].updateRectangle(self.rectangles[-1])  # Update the rectangle
            self.sample_group_boxes[-1].setX0()
            self.sample_group_boxes[-1].setY0()
        elif self.state == END_SIDE_EDIT:  # If the state is END_SIDE_EDIT
            self.end.setX(event.x())  # Set the end point's x to the current position's x
            self.rectangles[-1] = QRect(self.beginning, self.end)
            self.sample_group_boxes[-1].updateRectangle(self.rectangles[-1])  # Update the rectangle
            self.sample_group_boxes[-1].setXF()
            self.sample_group_boxes[-1].setYF()
        elif self.state == TOP_SIDE_EDIT:  # If the state is TOP_SIDE_EDIT
            self.beginning.setY(event.y())  # Set the beginning point's y to the current position's y
            self.rectangles[-1] = QRect(self.beginning, self.end)
            self.sample_group_boxes[-1].updateRectangle(self.rectangles[-1])  # Update the rectangle
            self.sample_group_boxes[-1].setY0()
            self.sample_group_boxes[-1].setYF()
        elif self.state == BOTTOM_SIDE_EDIT:  # If the state is BOTTOM_SIDE_EDIT
            self.end.setY(event.y())  # Set the end point's y to the current position's y
            self.rectangles[-1] = QRect(self.beginning, self.end)
            self.sample_group_boxes[-1].updateRectangle(self.rectangles[-1])  # Update the rectangle
            self.sample_group_boxes[-1].setX0()
            self.sample_group_boxes[-1].setYF()

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
        if self.scale < 15:  # If the scale is less than 20
            self.scale *= 2  # Increase the scale by 2
            self.resize_image()  # Resize the image
            for rectangle in self.rectangles:
                print(self.scale, " * ", rectangle.width(), " = ", int(rectangle.width() * self.scale))
                qp = QPoint(int(rectangle.x() * self.scale), int(rectangle.y() * self.scale))
                qs = QSize(int(rectangle.width() * self.scale), int(rectangle.height() * self.scale))
                print("before:", rectangle)
                rectangle.moveTo(qp)
                rectangle.setSize(qs)
                print("after:", rectangle)

    # This method is called when the user zooms out with his mouse wheel.
    def on_zoom_out(self):
        if self.scale > 1:
            for rectangle in self.rectangles:
                print(self.scale, " / ", rectangle.width(), " = ", int(rectangle.width() / self.scale))
                qp = QPoint(int(rectangle.x() / self.scale), int(rectangle.y() / self.scale))
                qs = QSize(int(rectangle.width() / self.scale), int(rectangle.height() / self.scale))
                print("before:", rectangle)
                rectangle.moveTo(qp)
                rectangle.setSize(qs)
                print("after:", rectangle)
            self.scale /= 2  # Decrease the scale by 2
            self.resize_image()  # Resize the image

    # This method resizes the image depending on the scale.
    def resize_image(self):
        size = self.pixmap.size()  # Get the size of the pixmap
        scaled_pixmap = self.pixmap.scaled(self.scale * size)  # Scale the pixmap
        self.setPixmap(scaled_pixmap)  # Set the pixmap to the scaled pixmap

    def setBeginning(self, beginning):
        self.beginning = beginning

    def setEnd(self, end):
        self.end = end

