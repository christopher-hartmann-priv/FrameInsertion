from email.policy import Policy
from PySide2.QtWidgets import QLabel, QWidget, QVBoxLayout, QSizePolicy

from PySide2.QtGui import QPainter, QPixmap

from PySide2.QtCore import QPoint, Qt

# for checking if file exists
from pathlib import Path


class Preview(QLabel):
    def __init__(self, img: str):
        super(Preview, self).__init__()
        if (Path(img).is_file()):
            self.pixmap = QPixmap(img)
        else:
            self.pixmap = QPixmap()

    def resetPixmap(self, img: str):
        self.pixmap = QPixmap(img)
        self.repaint()

    def paintEvent(self, event):
        size = self.size()
        scaledPix = self.pixmap.scaled(
            size, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)

        # get for label
        point = QPoint(0, 0)
        point.setX((size.width() - scaledPix.width())/2)
        point.setY((size.height() - scaledPix.height())/2)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: pink;')

        painter = QPainter(self)
        painter.drawPixmap(point, scaledPix)


class PreviewWidget(QWidget):
    def __init__(self, image_path: str, min_width: int, min_height: int, title: str):
        QWidget.__init__(self)

        self.image_path = image_path

        self.setWindowTitle(title)

        # sizes
        self.setMinimumHeight(min_height)
        self.setMinimumWidth(min_width)
        self.setSizePolicy(QSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))

        # layout and label
        layout = QVBoxLayout()
        layout.setMargin(0)
        self.label = Preview(image_path)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def reset_pixmap(self, img: str):
        self.label.resetPixmap(img)

    def get_image_path(self) -> str:
        return self.image_path
