from PyQt5 import QtWidgets

from event_manager import Event_Manager
from interface_setup import Ui_SelectZones

# Main function
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)  # Create an application instance
    SelectZones = QtWidgets.QMainWindow()  # Create a main window instance
    ui = Ui_SelectZones()  # Create an instance of the UI class
    ui.setupUi(SelectZones)  # Set up the UI with created UI instance and main window
    SelectZones.show()  # Show the main window
    event_manager = Event_Manager(ui)  # Create an event manager instance and pass the UI instance
    sys.exit(app.exec_())  # Execute the application
