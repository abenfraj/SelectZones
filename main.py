from PyQt5 import QtWidgets
from event_manager import Event_Manager
from interface_setup import Ui_SelectZones

from main_window import MainWindow

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_SelectZones()
    SelectZones = MainWindow()
    ui.setupUi(SelectZones)
    SelectZones.show()
    event_manager = Event_Manager(ui)
    SelectZones.setEventManager(event_manager)
    sys.exit(app.exec_())
