from PyQt5 import QtWidgets

from event_manager import Event_Manager
from interface_setup import Ui_SelectZones

# Main function
from main_window import MainWindow

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)  # Create an application instance
    ui = Ui_SelectZones()  # Create an instance of the UI class
    SelectZones = MainWindow()  # Create a main window instance
    ui.setupUi(SelectZones)  # Set up the UI with created UI instance and main window
    SelectZones.show()  # Show the main window
    event_manager = Event_Manager(ui)  # Create an event manager instance and pass the UI instance
    SelectZones.setEventManager(event_manager)  # Set the event manager instance to the main window
    sys.exit(app.exec_())  # Execute the application
