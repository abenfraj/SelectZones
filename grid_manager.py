import numpy as np
from PyQt5 import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QWidget, QPushButton

from adjustable_grid import AdjustableGrid
from bitmap_manager import BitmapManager
from grid_control import GridControl


class GridView(QGraphicsView):
    def __init__(self, *,
                 parent: QWidget,
                 num_cols: int = 1,
                 num_rows: int = 1):
        super().__init__(parent=parent)
        self.setGeometry(0, 0, 500, 500)
        self.setMouseTracking(True)

        """Scene"""
        self.scene = QGraphicsScene()
        self.setSceneRect(0, 0, 500, 500)
        self.setScene(self.scene)

        """Grids"""
        self.placed_grids = []
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.current_grid = AdjustableGrid(
            scene=self.scene,
            num_cols=self.num_cols,
            num_rows=self.num_rows
        )
        self.parent = self.parentWidget()


class GridWindow(QWidget):
    modes = {'grid': 0, 'training': 1}
    sig_grid_placed = pyqtSignal(np.ndarray)
    sig_change_mode = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 700, 500)
        self.setWindowTitle('SELECT ZONES')

        self.initial_no_cols = 1
        self.initial_no_rows = 1
        self.mode = GridWindow.modes['grid']

        """Initialize GridView"""
        self.view = GridView(
            parent=self,
            num_rows=self.initial_no_rows,
            num_cols=self.initial_no_cols
        )

        """Initialize GridControl"""
        self.grid_control = GridControl(
            parent=self,
            title='Grid Control',
            num_rows=self.initial_no_rows,
            num_cols=self.initial_no_cols
        )

        """QImage visualized on background"""
        self.bg_image = BitmapManager()

        """Open bg_image/series buttons"""
        self.open_img_button = QPushButton('Load BMP file', parent=self)
        self.open_series_button = QPushButton('Load BMP series', parent=self)

        self._configure_gui()
        self._configure_signals()

        self.show()
        # self.start_work()
