from PyQt5 import QtCore
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


class BitmapLabel(QLabel):
    """
    This class is used to draw a bitmap label.
    """

    def __init__(self, ui):
        """
        This method initializes the BitmapLabel object.

        :param: ui: The main window's UI.
        """
        super().__init__()  # Call the parent class's (QLabel) constructor
        self.bitmap_image = None  # This is the image that will be displayed on the label
        self.pixmap = None  # This is the pixmap that will be displayed on the label
        self.scale = 1.0  # This is the scale of the image
        self.ui = ui  # This is the main window's UI
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
        self.state = FREE_STATE  # This is the state of the mouse

        self.setMouseTracking(True)  # This makes the mouse track the mouse
        self.free_cursor_on_side = 0  # This is the side of the rectangle where the mouse is on

        self.show()  # Show the label

    def paintEvent(self, event):
        """
        This method draws the rectangle that is drawn by the mouse.

        :param: event: The paint event.
        :return: None.
        """
        if self.bitmap_image is not None:  # If the image is not None
            super().paintEvent(event)  # Call the parent class's paintEvent method
            painter = QPainter(self)  # Create a QPainter object
            self.rectangle_border_color = self.colors[
                0]  # Set the rectangle's border color to the first color in the list
            painter.setPen(
                QPen(self.rectangle_border_color, 2))  # Set the pen's color to black and the pen's width to 1
            for rectangle in self.rectangles:  # For each rectangle in the list of rectangles
                painter.drawRect(rectangle)  # Draw the rectangle
                try:  # Try to
                    self.rectangle_border_color = self.colors[self.rectangles.index(
                        rectangle) + 1]  # Set the rectangle's border color to the next color in the list
                    painter.setPen(
                        QPen(self.rectangle_border_color, 2))  # Set the pen's color to black and the pen's width to 1
                except IndexError:  # If the index is out of range
                    self.rectangle_border_color = self.colors[
                        0]  # Set the rectangle's border color to the first color in the list

            if not self.free_cursor_on_side:  # If the mouse is not on the side of the rectangle
                return  # Return

            painter.setPen(QPen(Qt.black, 3, Qt.DashLine))  # Set the pen's color to black and the pen's width to 3
            if self.free_cursor_on_side == CURSOR_ON_BEGIN_SIDE:  # If the mouse is on the beginning side of the rectangle
                end = QPoint(self.end)  # Set the end point to the end point of the rectangle
                end.setX(self.beginning.x())  # Set the end point's x to the beginning point's x
                painter.drawLine(self.beginning, end)  # Draw a line from the beginning point to the end point

            elif self.free_cursor_on_side == CURSOR_ON_END_SIDE:  # If the mouse is on the end side of the rectangle
                beginning = QPoint(self.beginning)  # Set the beginning point to the beginning point of the rectangle
                beginning.setX(self.end.x())  # Set the beginning point's x to the end point's x
                painter.drawLine(self.end, beginning)  # Draw a line from the end point to the beginning point

            elif self.free_cursor_on_side == CURSOR_ON_TOP_SIDE:  # If the mouse is on the top side of the rectangle
                end = QPoint(self.end)  # Set the end point to the end point of the rectangle
                end.setY(self.beginning.y())  # Set the end point's y to the beginning point's y
                painter.drawLine(self.beginning, end)  # Draw a line from the beginning point to the end point

            elif self.free_cursor_on_side == CURSOR_ON_BOTTOM_SIDE:  # If the mouse is on the bottom side of the rectangle
                beginning = QPoint(self.beginning)  # Set the beginning point to the beginning point of the rectangle
                beginning.setY(self.end.y())  # Set the beginning point's y to the end point's y
                painter.drawLine(self.end, beginning)  # Draw a line from the end point to the beginning point

    def cursor_on_side(self, e_pos) -> int:
        """
        This method checks if the cursor is on the side of the rectangle.

        :param: e_pos: The position of the cursor.
        :return: The side of the rectangle the cursor is on.
        """
        if not self.beginning.isNull() and not self.end.isNull():  # If the rectangle is not empty
            x1, x2 = sorted(
                [self.beginning.x(), self.end.x()])  # Sort the x coordinates of the beginning and end points
            y1, y2 = sorted(
                [self.beginning.y(), self.end.y()])  # Sort the y coordinates of the beginning and end points

            if x1 <= e_pos.x() <= x2:  # If the cursor is on the x coordinate of the beginning point

                if abs(self.beginning.y() - e_pos.y()) <= 5:  # If the cursor is on the y coordinate of the beginning point
                    return CURSOR_ON_TOP_SIDE  # Return the top side
                elif abs(self.end.y() - e_pos.y()) <= 5:  # If the cursor is on the y coordinate of the end point
                    return CURSOR_ON_BOTTOM_SIDE  # Return the bottom side

            if y1 <= e_pos.y() <= y2:  # If the cursor is on the y coordinate of the beginning point
                if abs(self.beginning.x() - e_pos.x()) <= 5:  # If the cursor is on the x coordinate of the beginning point
                    return CURSOR_ON_BEGIN_SIDE  # Return the beginning side
                elif abs(self.end.x() - e_pos.x()) <= 5:  # If the cursor is on the x coordinate of the end point
                    return CURSOR_ON_END_SIDE  # Return the end side
        return 0  # Return 0 if the cursor is not on any side

    def mousePressEvent(self, event):
        """
        This method is called when the mouse is pressed.

        :param: event: The event that occurred.
        :return: None
        """
        if self.bitmap_image is not None:  # If the image is not None
            super().mousePressEvent(event)  # Call the parent class's mousePressEvent method
            side = self.cursor_on_side(event.pos())  # Get the side of the rectangle the cursor is on
            if side == CURSOR_ON_BEGIN_SIDE:  # If the cursor is on the beginning side of the rectangle
                self.state = BEGIN_SIDE_EDIT  # Set the state to begin side edit
            elif side == CURSOR_ON_END_SIDE:  # If the cursor is on the end side of the rectangle
                self.state = END_SIDE_EDIT  # Set the state to end side edit
            elif side == CURSOR_ON_TOP_SIDE:  # If the cursor is on the top side of the rectangle
                self.state = TOP_SIDE_EDIT  # Set the state to top side edit
            elif side == CURSOR_ON_BOTTOM_SIDE:  # If the cursor is on the bottom side of the rectangle
                self.state = BOTTOM_SIDE_EDIT  # Set the state to bottom side edit
            else:  # If the cursor is not on any side of the rectangle
                self.state = BUILDING_SQUARE  # Set the state to building square
                self.rectangles.append(QRect(self.beginning, self.end))  # Add the rectangle to the list of rectangles
                self.sample_group_boxes.append(SampleGroupBox(self.ui,
                                                              len(self.rectangles) - 1))  # Add a sample group box to the list of sample group boxes
                self.beginning = event.pos()  # Set the beginning point to the current position
                self.end = event.pos()  # Set the end point to the current position
                self.update()  # Update the label

    def mouseReleaseEvent(self, event):
        """
        This method is called when the mouse is released.

        :param: event: The event that occurred.
        :return: None
        """
        if self.bitmap_image is not None:  # If the image is not None
            self.apply_event(event)  # Apply the event
            self.state = FREE_STATE  # Set the state to free state
            self.sample_group_boxes[-1].setX0()  # Set the x0 of the last sample group box to the x coordinate of the beginning point
            self.sample_group_boxes[-1].setY0()  # Set the y0 of the last sample group box to the y coordinate of the beginning point
            self.sample_group_boxes[-1].setXF()  # Set the xF of the last sample group box to the x coordinate of the end point
            self.sample_group_boxes[-1].setYF()  # Set the yF of the last sample group box to the y coordinate of the end point
            super().mouseReleaseEvent(event)  # Call the parent class's mouseReleaseEvent method

    def mouseMoveEvent(self, event):
        """
        This method is called when the mouse is moved.

        :param: event: The event that occurred.
        :return: None
        """
        if self.bitmap_image is not None:  # If the mouse is pressed and the image is not None
            super().mouseMoveEvent(event)  # Call the parent class's mouseMoveEvent method
            if self.state == FREE_STATE:  # If the state is free state
                self.free_cursor_on_side = self.cursor_on_side(event.pos())  # Set the free cursor on side to the cursor on side of the current position
                if self.free_cursor_on_side == CURSOR_ON_BEGIN_SIDE or self.free_cursor_on_side == CURSOR_ON_END_SIDE:  # If the cursor is on the beginning or end side
                    self.setCursor(Qt.SizeHorCursor)  # Set the cursor to a horizontal cursor
                elif self.free_cursor_on_side == CURSOR_ON_TOP_SIDE or self.free_cursor_on_side == CURSOR_ON_BOTTOM_SIDE:  # If the cursor is on the top or bottom side
                    self.setCursor(Qt.SizeVerCursor)  # Set the cursor to a vertical cursor
                else:  # If the cursor is not on any side
                    self.unsetCursor()  # Unset the cursor
                self.update()  # Update the label
            else:  # If the state is not free state
                self.apply_event(event)  # Apply the event
                self.update()  # Update the label

    def apply_event(self, event):
        """
        This method is called when the mouse is moved.

        :param: event: The event that occurred.
        :return: None
        """
        if self.state == BUILDING_SQUARE:  # If the state is BUILDING_SQUARE
            self.end = event.pos()  # Set the end point to the current position
            self.rectangles[-1] = QRect(self.beginning, self.end)  # Update the rectangle
            self.sample_group_boxes[-1].updateRectangle(self.rectangles[-1])  # Update the rectangle
        elif self.state == BEGIN_SIDE_EDIT:  # If the state is BEGIN_SIDE_EDIT
            self.beginning.setX(event.x())  # Set the beginning point's x to the current position's x
            self.rectangles[-1] = QRect(self.beginning, self.end)  # Update the rectangle
            self.sample_group_boxes[-1].updateRectangle(self.rectangles[-1])  # Update the rectangle
            self.sample_group_boxes[-1].setX0()  # Set the x0 of the last sample group box to the x coordinate of the beginning point
            self.sample_group_boxes[-1].setY0()  # Set the y0 of the last sample group box to the y coordinate of the beginning point
        elif self.state == END_SIDE_EDIT:  # If the state is END_SIDE_EDIT
            self.end.setX(event.x())  # Set the end point's x to the current position's x
            self.rectangles[-1] = QRect(self.beginning, self.end)
            self.sample_group_boxes[-1].updateRectangle(self.rectangles[-1])  # Update the rectangle
            self.sample_group_boxes[-1].setXF()  # Set the xF of the last sample group box to the x coordinate of the end point
            self.sample_group_boxes[-1].setYF()  # Set the yF of the last sample group box to the y coordinate of the end point
        elif self.state == TOP_SIDE_EDIT:  # If the state is TOP_SIDE_EDIT
            self.beginning.setY(event.y())  # Set the beginning point's y to the current position's y
            self.rectangles[-1] = QRect(self.beginning, self.end)  # Update the rectangle
            self.sample_group_boxes[-1].updateRectangle(self.rectangles[-1])  # Update the rectangle
            self.sample_group_boxes[-1].setY0()  # Set the y0 of the last sample group box to the y coordinate of the beginning point
            self.sample_group_boxes[-1].setYF()  # Set the yF of the last sample group box to the y coordinate of the end point
        elif self.state == BOTTOM_SIDE_EDIT:  # If the state is BOTTOM_SIDE_EDIT
            self.end.setY(event.y())  # Set the end point's y to the current position's y
            self.rectangles[-1] = QRect(self.beginning, self.end)
            self.sample_group_boxes[-1].updateRectangle(self.rectangles[-1])  # Update the rectangle
            self.sample_group_boxes[-1].setX0()  # Set the x0 of the last sample group box to the x coordinate of the beginning point
            self.sample_group_boxes[-1].setYF()  # Set the yF of the last sample group box to the y coordinate of the end point

    # This method sets the image that will be displayed on the label.
    def wheelEvent(self, event):
        """
        This method is called when the mouse wheel is moved.

        :param: event: The event that occurred.
        :return: None
        """
        if self is not None:  # If the image is not None
            if event.angleDelta().y() > 0:  # If the mouse wheel is rotated up
                if self.bitmap_image is not None:  # If the image is not None
                    self.on_zoom_in()  # Call the zoom in method
            else:  # If the mouse wheel is rotated down
                if self.bitmap_image is not None:  # If the image is not None
                    self.on_zoom_out()  # Call the zoom out method

    # This method is called when the user zooms in with his mouse wheel.
    def on_zoom_in(self):
        """
        This method is called when the user zooms in with his mouse wheel.

        :return: None
        """
        if self.scale < 15:  # If the scale is less than 20
            self.scale *= 2  # Increase the scale by 2
            self.resize_image()  # Resize the image
            qp = None  # Create a new painter
            qs = None  # Create a new QImage
            for rectangle in self.rectangles:  # For each rectangle
                qp = QPoint(int(rectangle.x() * 2), int(rectangle.y() * 2))  # Create a new point
                qs = QSize(int(rectangle.width() * 2), int(rectangle.height() * 2))  # Create a new size
                rectangle.moveTo(qp)  # Move the rectangle to the new point
                rectangle.setSize(qs)  # Set the rectangle's size to the new size
            self.beginning = qp  # Set the beginning point to the new point
            self.end = QPoint(qp.x() + qs.width(), qp.y() + qs.height())  # Set the end point to the new point

    def on_zoom_out(self):
        """
        This method is called when the user zooms out with his mouse wheel.

        :return: None
        """
        if self.scale > 1:  # If the scale is greater than 1
            for rectangle in self.rectangles:  # For each rectangle
                qp = QPoint(int(rectangle.x() / 2), int(rectangle.y() / 2))  # Create a new point
                qs = QSize(int(rectangle.width() / 2), int(rectangle.height() / 2))  # Create a new size
                rectangle.moveTo(qp)  # Move the rectangle to the new point
                rectangle.setSize(qs)  # Set the rectangle's size to the new size
            self.scale /= 2  # Decrease the scale by 2
            self.resize_image()  # Resize the image

    def resize_image(self):
        """
        This method resizes the image depending on the scale.

        :return: None
        """
        size = self.pixmap.size()  # Get the size of the pixmap
        scaled_pixmap = self.pixmap.scaled(self.scale * size)  # Scale the pixmap
        self.setPixmap(scaled_pixmap)  # Set the pixmap to the scaled pixmap

    def setBeginning(self, beginning):
        """
        This method sets the beginning of the rectangle.

        :param: beginning: The beginning of the rectangle.
        :return: None
        """
        self.beginning = beginning  # Set the beginning to the given beginning

    def setEnd(self, end):
        """
        This method sets the end of the rectangle.

        :param: end: The end of the rectangle.
        :return: None
        """
        self.end = end  # Set the end to the given end