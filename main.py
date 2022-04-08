import sys
from PyQt5.QtWidgets import QApplication
from grid_manager import GridWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Start Qt application
    main_window = GridWindow()  # Create main window
    sys.exit(app.exec_())  # Start event loop
