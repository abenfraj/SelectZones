from PyQt5 import QtCore


class MouseTracker(QtCore.QObject):
    """
    This is the class that sends the signal that is emitted when the mouse position changes.
    """
    positionChanged = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, widget):
        """
        This is the constructor for the MouseTracker class.

        :param widget: The widget that the mouse is being tracked on.
        """
        super().__init__(widget)
        self._widget = widget
        self.widget.setMouseTracking(True)
        self.widget.installEventFilter(self)

    @property
    def widget(self):
        """
        This is the getter for the widget property.

        :return: The widget that the mouse is being tracked on.
        """
        return self._widget

    def eventFilter(self, o, e):
        """
        This is the event filter for the widget.

        :param o: The object that the event is being sent to.
        :param e: The event that is being sent.
        :return: True if the event is handled, False if not.
        """
        if o is self.widget and e.type() == QtCore.QEvent.MouseMove:
            self.positionChanged.emit(e.pos())
        return super().eventFilter(o, e)
