from PyQt5 import QtCore


# This class is used to track the mouse position and send it to the main window
class MouseTracker(QtCore.QObject):
    positionChanged = QtCore.pyqtSignal(QtCore.QPoint)  # Signal to send the mouse position to the main window

    # This class is used to draw the mouse position on the screen
    def __init__(self, widget):
        super().__init__(widget)  # Call the parent class
        self._widget = widget  # Store the widget
        self.widget.setMouseTracking(True)  # Enable mouse tracking
        self.widget.installEventFilter(self)  # Install the event filter

    @property
    # This property is used to get the mouse position
    def widget(self):
        return self._widget  # Return the widget

    # This method is used to filter the mouse events
    def eventFilter(self, o, e):
        if o is self.widget and e.type() == QtCore.QEvent.MouseMove:  # If the event is a mouse move event
            self.positionChanged.emit(e.pos())  # Emit the signal with the mouse position
        return super().eventFilter(o, e)  # Return the event
