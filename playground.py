"""

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

FREE_STATE = 1
BUILDING_SQUARE = 2
BEGIN_SIDE_EDIT = 3
END_SIDE_EDIT = 4

CURSOR_ON_BEGIN_SIDE = 1
CURSOR_ON_END_SIDE = 2


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(30, 30, 600, 400)
        self.beginning = QPoint()
        self.end = QPoint()

        self.state = FREE_STATE
        self.setMouseTracking(True)
        self.free_cursor_on_side = 0

    def paintEvent(self, event):
        super().paintEvent(event)  # Call the parent class's paintEvent method
        painter = QPainter(self)  # Create a QPainter object
        br = QBrush(QColor(100, 10, 10, 40))
        painter.setBrush(br)
        painter.drawRect(QRect(self.beginning, self.end))
        # for rectangle in self.rectangles:  # For each rectangle
        #     painter.drawRect(rectangle)  # Draw the rectangle

        # if not self.beginning.isNull() and not self.end.isNull():  # If the begin and end points are not null
        #     painter.drawRect(QRect(self.beginning, self.end).normalized())  # Draw the rectangle
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

    def cursor_on_side(self, e_pos) -> int:
        if not self.beginning.isNull() and not self.end.isNull():
            y1, y2 = sorted([self.beginning.y(), self.end.y()])
            if y1 <= e_pos.y() <= y2:

                # 5 resolution, more easy to pick than 1px
                if abs(self.beginning.x() - e_pos.x()) <= 5:
                    print("beginning")
                    return CURSOR_ON_BEGIN_SIDE
                elif abs(self.end.x() - e_pos.x()) <= 5:
                    print("end")
                    return CURSOR_ON_END_SIDE

        return 0

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        side = self.cursor_on_side(event.pos())
        if side == CURSOR_ON_BEGIN_SIDE:
            self.state = BEGIN_SIDE_EDIT
        elif side == CURSOR_ON_END_SIDE:
            self.state = END_SIDE_EDIT
        else:
            self.state = BUILDING_SQUARE

            self.begin = event.pos()
            self.end = event.pos()
            self.update()

    def applye_event(self, event):
        if self.state == BUILDING_SQUARE:
            self.end = event.pos()
        elif self.state == BEGIN_SIDE_EDIT:
            self.begin.setX(event.x())
        elif self.state == END_SIDE_EDIT:
            self.end.setX(event.x())

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.state == FREE_STATE:
            self.free_cursor_on_side = self.cursor_on_side(event.pos())
            if self.free_cursor_on_side:
                self.setCursor(Qt.SizeHorCursor)
            else:
                self.unsetCursor()
            self.update()
        else:
            self.applye_event(event)
            self.update()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.applye_event(event)
        self.state = FREE_STATE


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())
"""