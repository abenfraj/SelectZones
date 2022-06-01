from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.event_manager = None

    def setEventManager(self, event_manager):
        self.event_manager = event_manager

    def closeEvent(self, event):
        self.event_manager.quitApp()
