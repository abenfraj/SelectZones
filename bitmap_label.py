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

        :param ui: The main window's UI object.
        """

        super().__init__()
        self.bitmap_image = None
        self.pixmap = None
        self.scale = 1.0
        self.ui = ui
        self.rectangles = self.ui.rectangles
        self.sample_group_boxes = self.ui.sample_group_boxes
        self.beginning = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.rectangle_border_color = None
        self.color_index = 0
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
                       ]
        self.state = FREE_STATE

        self.setMouseTracking(True)
        self.free_cursor_on_side = 0

        self.show()

    def paintEvent(self, event):
        """
        This method makes the rectangle that is drawn by the mouse. The color changes after each drawn rectangle.
        It also draws the editing dashed lines on the sides of the last drawn rectangle.

        :param event: The paint event.
        :return: None.
        """

        if self.bitmap_image is not None:
            super().paintEvent(event)
            painter = QPainter(self)
            self.rectangle_border_color = self.colors[
                0]
            painter.setPen(
                QPen(self.rectangle_border_color, 2))
            for rectangle in self.rectangles:
                painter.drawRect(rectangle)
                try:
                    self.rectangle_border_color = self.colors[self.rectangles.index(
                        rectangle) + 1]
                    painter.setPen(
                        QPen(self.rectangle_border_color, 2))
                except IndexError:
                    self.rectangle_border_color = self.colors[
                        0]

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

    def cursorOnSide(self, e_pos) -> int:
        """
        This method checks if the cursor is on a side of the rectangle.

        :param e_pos: The position of the cursor.
        :return: The side of the rectangle the cursor is on.
        """

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

    def mousePressEvent(self, event):
        """
        This method is called when the mouse is pressed. It sets the state of the action that is being performed.

        :param event: The mouse press event.
        :return: None
        """

        if self.bitmap_image is not None:
            super().mousePressEvent(event)
            side = self.cursorOnSide(event.pos())
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
                self.update()

    def mouseReleaseEvent(self, event):
        """
        This method is called when the mouse is released. It sets the values of the rectangle in its sample group box.

        :param event: The event that occurred.
        :return: None
        """

        if self.bitmap_image is not None:  # If the image is not None
            self.applyEvent(event)  # Apply the event
            self.checkRectangleInImage(self.rectangles[-1])  # Check if the rectangle is out of bounds
            self.state = FREE_STATE  # Set the state to free state
            self.sample_group_boxes[-1].setX0(
                self.ui.number_format)  # Set the x0 of the last sample group box to the x coordinate of the beginning point
            self.sample_group_boxes[-1].setY0(
                self.ui.number_format)  # Set the y0 of the last sample group box to the y coordinate of the beginning point
            self.sample_group_boxes[-1].setXF(
                self.ui.number_format)  # Set the xF of the last sample group box to the x coordinate of the end point
            self.sample_group_boxes[-1].setYF(
                self.ui.number_format)  # Set the yF of the last sample group box to the y coordinate of the end point
            super().mouseReleaseEvent(event)  # Call the parent class's mouseReleaseEvent method

    def mouseMoveEvent(self, event):
        """
        This method is called when the mouse is moved.
        It checks if the mouse is on a side of the rectangle and modifies the icon accordingly.
        If the mouse is moving while not is the free state, it will call the applyEvent method.

        :param event: The mouse move event.
        :return: None
        """

        if self.bitmap_image is not None:  # If the mouse is pressed and the image is not None
            super().mouseMoveEvent(event)  # Call the parent class's mouseMoveEvent method
            if self.state == FREE_STATE:  # If the state is free state
                self.free_cursor_on_side = self.cursorOnSide(
                    event.pos())  # Set the free cursor on side to the cursor on side of the current position
                if self.free_cursor_on_side == CURSOR_ON_BEGIN_SIDE or self.free_cursor_on_side == CURSOR_ON_END_SIDE:  # If the cursor is on the beginning or end side
                    self.setCursor(Qt.SizeHorCursor)  # Set the cursor to a horizontal cursor
                elif self.free_cursor_on_side == CURSOR_ON_TOP_SIDE or self.free_cursor_on_side == CURSOR_ON_BOTTOM_SIDE:  # If the cursor is on the top or bottom side
                    self.setCursor(Qt.SizeVerCursor)  # Set the cursor to a vertical cursor
                else:  # If the cursor is not on any side
                    self.unsetCursor()  # Unset the cursor
                self.update()  # Update the label
            else:  # If the state is not free state
                self.applyEvent(event)  # Apply the event
                self.update()  # Update the label

    def applyEvent(self, event):
        """
        This method is called when the mouse is moved.
        It performs the modifications to the rectangle and its associated sample group box.

        :param event: The event that occurred.
        :return: None
        """

        if self.state == BUILDING_SQUARE:
            self.end = event.pos()
            self.rectangles[-1] = QRect(self.beginning, self.end)
            self.sample_group_boxes[-1].updateRectangle(self.rectangles[-1])
        elif self.state == BEGIN_SIDE_EDIT:
            self.beginning.setX(event.x())
            self.rectangles[-1] = QRect(self.beginning, self.end)
            self.sample_group_boxes[-1].updateRectangle(self.rectangles[-1])
            self.sample_group_boxes[-1].setX0(self.ui.number_format)
            self.sample_group_boxes[-1].setY0(self.ui.number_format)
        elif self.state == END_SIDE_EDIT:
            self.end.setX(event.x())
            self.rectangles[-1] = QRect(self.beginning, self.end)
            self.sample_group_boxes[-1].updateRectangle(self.rectangles[-1])
            self.sample_group_boxes[-1].setXF(self.ui.number_format)
            self.sample_group_boxes[-1].setYF(self.ui.number_format)
        elif self.state == TOP_SIDE_EDIT:
            self.beginning.setY(event.y())
            self.rectangles[-1] = QRect(self.beginning, self.end)
            self.sample_group_boxes[-1].updateRectangle(self.rectangles[-1])
            self.sample_group_boxes[-1].setY0(self.ui.number_format)
            self.sample_group_boxes[-1].setYF(self.ui.number_format)
        elif self.state == BOTTOM_SIDE_EDIT:
            self.end.setY(event.y())
            self.rectangles[-1] = QRect(self.beginning, self.end)
            self.sample_group_boxes[-1].updateRectangle(self.rectangles[-1])
            self.sample_group_boxes[-1].setX0(self.ui.number_format)
            self.sample_group_boxes[-1].setYF(self.ui.number_format)

    def wheelEvent(self, event):
        """
        This method is called when the mouse wheel is moved. It changes the zoom of the image.

        :param event: The wheel event.
        :return: None
        """

        if self is not None:
            if event.angleDelta().y() > 0:
                if self.bitmap_image is not None:
                    self.onZoomIn()
            else:
                if self.bitmap_image is not None:
                    self.onZoomOut()

    def onZoomIn(self):
        """
        This method is called when the user zooms in with his mouse wheel.
        It increases the scaling, resizes the image and the rectangles accordingly.

        :return: None
        """

        if self.scale < 15:
            self.scale *= 2
            self.resizeImage()
            qp = None
            qs = None
            for rectangle in self.rectangles:
                qp = QPoint(int(rectangle.x() * 2), int(rectangle.y() * 2))
                qs = QSize(int(rectangle.width() * 2), int(rectangle.height() * 2))
                rectangle.moveTo(qp)
                rectangle.setSize(qs)
            self.beginning = qp
            self.end = QPoint(qp.x() + qs.width(), qp.y() + qs.height())

    def onZoomOut(self):
        """
        This method is called when the user zooms out with his mouse wheel.
        It decreases the scaling, resizes the image and the rectangles accordingly.

        :return: None
        """

        if self.scale > 1:
            qp = None
            qs = None
            for rectangle in self.rectangles:
                qp = QPoint(int(rectangle.x() / 2), int(rectangle.y() / 2))
                qs = QSize(int(rectangle.width() / 2), int(rectangle.height() / 2))
                rectangle.moveTo(qp)
                rectangle.setSize(qs)
            self.beginning = qp
            self.end = QPoint(qp.x() + qs.width(), qp.y() + qs.height())
            self.scale /= 2
            self.resizeImage()

    def resizeImage(self):
        """
        This method resizes the image depending on the scale.

        :return: None
        """

        size = self.pixmap.size()
        scaled_pixmap = self.pixmap.scaled(self.scale * size)
        self.setPixmap(scaled_pixmap)

    def setBeginning(self, beginning):
        """
        This method sets the beginning point of the rectangle.

        :param beginning: The beginning of the rectangle.
        :return: None
        """

        self.beginning = beginning

    def setEnd(self, end):
        """
        This method sets the end point of the rectangle.

        :para end: The end of the rectangle.
        :return: None
        """

        self.end = end

    def checkRectangleInImage(self, rectangle):
        """
        This method checks if the rectangle is in the image and automatically puts it back in.

        :param rectangle: The rectangle to check.
        :return: None
        """

        if rectangle.x() + rectangle.width() > self.size().width():
            rectangle.setWidth(self.size().width() - rectangle.x() - 1)
            self.end = QPoint(self.size().width(), self.end.y())
        if rectangle.y() + rectangle.height() > self.size().height():
            rectangle.setHeight(self.size().height() - rectangle.y() - 1)
            self.end = QPoint(self.end.x(), self.size().height())
        if rectangle.x() + rectangle.width() < 0:
            rectangle.setWidth(- rectangle.x() + 1)
            self.end = QPoint(0, rectangle.y() + rectangle.height())
        if rectangle.y() + rectangle.height() < 0:
            rectangle.setHeight(- rectangle.y() + 1)
            self.end = QPoint(rectangle.x() + rectangle.width(), 0)
