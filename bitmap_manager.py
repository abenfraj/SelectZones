from PyQt5.QtGui import QImage, QPixmap


class BitmapManager:
    def __init__(self):
        self.img_file = None
        self.image = None
        self.scaling_factor = None

    def setImage(self, file_name):
        self.image = QImage(file_name)

    def displayInScene(self, view):
        pixmap = QPixmap.fromImage(self.image)
        pixmap_scaled = pixmap.scaledToHeight(view.height())
        view.scene.addPixmap(pixmap_scaled)
        original_size = pixmap.size()
        scaled_size = pixmap_scaled.size()
        self.scaling_factor = scaled_size.height() / original_size.height()
