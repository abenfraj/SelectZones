from PyQt5 import QtWidgets

from event_manager import Event_Manager
from interface_setup import Ui_SelectZones

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    SelectZones = QtWidgets.QMainWindow()
    ui = Ui_SelectZones()
    ui.setupUi(SelectZones)
    SelectZones.show()
    event_manager = Event_Manager(ui)
    sys.exit(app.exec_())
