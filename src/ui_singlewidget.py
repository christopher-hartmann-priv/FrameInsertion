# for ... everything?
from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QFileDialog

# for pixmap
from PySide2.QtGui import QPixmap

# for aspectratio
from PySide2.QtCore import Qt, QMargins

# for rife
import src.insert_frame as inserter

# for previewing
import src.ui_previewwidget as preview


class SingleInterpolationWidget(QWidget):
    def __init__(self, parent=None):
        super(SingleInterpolationWidget, self).__init__(parent)

        # TODO get parameters from config tab
        self.engine = inserter.SimpleRifeInserter()
        self.engine.set_verbose(True)

        self.layout = QVBoxLayout()

        self.setup_group1()
        self.setup_group2()
        self.setup_group3()
        self.setup_preview()
        self.setup_main_button()

        self.setLayout(self.layout)

    def setup_group1(self):
        # first image
        self.open_image1_button = QPushButton("Open Image")
        self.image1_path_label = QLabel("Open First Image")
        self.image1_widget = QWidget()
        l = QHBoxLayout()
        l.setMargin(0)
        l.addWidget(self.open_image1_button)
        l.addWidget(self.image1_path_label)
        l.addStretch()
        self.image1_widget.setLayout(l)
        self.open_image1_button.clicked.connect(self.open_image1)
        self.layout.addWidget(self.image1_widget)

    def setup_group2(self):
        # second image
        self.open_image2_button = QPushButton("Open Image")
        self.image2_path_label = QLabel("Open Second image")
        self.image2_widget = QWidget()
        l = QHBoxLayout()
        l.setMargin(0)
        l.addWidget(self.open_image2_button)
        l.addWidget(self.image2_path_label)
        l.addStretch()
        self.image2_widget.setLayout(l)
        self.open_image2_button.clicked.connect(self.open_image2)
        self.layout.addWidget(self.image2_widget)

    def setup_group3(self):
        # output image
        self.open_image3_button = QPushButton("Select Output Image")
        self.image3_path_label = QLabel("Set Output Image")
        self.image3_widget = QWidget()
        l = QHBoxLayout()
        l.setMargin(0)
        l.addWidget(self.open_image3_button)
        l.addWidget(self.image3_path_label)
        l.addStretch()
        self.image3_widget.setLayout(l)
        self.open_image3_button.clicked.connect(self.open_image3)
        self.layout.addWidget(self.image3_widget)

    def setup_preview(self):
        # image preview
        self.preview1 = preview.PreviewWidget(
            image_path="src/blank.jpg", min_width=200, min_height=200, title="")
        self.preview2 = preview.PreviewWidget(
            image_path="src/blank.jpg", min_width=200, min_height=200, title="")

        self.preview_widget = QWidget()
        l = QHBoxLayout()
        l.setMargin(0)
        l.addWidget(self.preview1)
        l.addWidget(self.preview2)
        self.preview_widget.setLayout(l)
        self.layout.addWidget(self.preview_widget)

    def setup_main_button(self):
        # "start" button

        self.button_widget = QWidget()
        l = QHBoxLayout()
        l.setMargin(0)

        self.startButton = QPushButton("Interpolate")
        self.startButton.clicked.connect(self.interpolate)

        l.addStretch()
        l.addWidget(self.startButton)

        self.button_widget.setLayout(l)

        self.layout.addWidget(self.button_widget)

    def open_image1(self):
        # TODO kinda redundant
        fileName = QFileDialog.getOpenFileName(
            self, "Open First Image", "", "Image Files (*.png *.jpg *.bmp)")

        self.image1_path_label.setText(fileName[0])
        self.preview1.reset_pixmap(fileName[0])

    def open_image2(self):
        # TODO kinda redundant
        fileName = QFileDialog.getOpenFileName(
            self, "Open Second Image", "", "Image Files (*.png *.jpg *.bmp)")

        self.image2_path_label.setText(fileName[0])
        self.preview2.reset_pixmap(fileName[0])

    def open_image3(self):
        # TODO kinda redundant
        fileName = QFileDialog.getSaveFileName(
            self, "Select Output Filename", "", "Image Files (*.png *.jpg *.bmp)")

        self.image3_path_label.setText(fileName[0])

    def interpolate(self):
        out = self.image3_path_label.text()

        self.engine.interpolate_image_single(self.image1_path_label.text(
        ), self.image2_path_label.text(), out)

        self.pre = preview.PreviewWidget(out, 200, 200, out)
        self.pre.setWindowState(Qt.WindowMaximized)
        self.pre.show()


def closeEvent(self, event):
    # close previews
    # TODO doesn't work
    self.pre.close()
    event.accept()
