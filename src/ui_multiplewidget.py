# for ... everything?
from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QFileDialog, QSpinBox, QCheckBox

# for pixmap
from PySide2.QtGui import QPixmap

# for aspectratio
from PySide2.QtCore import Qt

# for rife
import src.insert_frame as sri

# for previewing
import src.ui_previewwidget as preview

# for opening preview folder
import glob

# for encoding
import ffmpeg as ffm


class MultipleInterpolationWidget(QWidget):
    def __init__(self, parent=None):
        super(MultipleInterpolationWidget, self).__init__(parent)

        # TODO get parameters from config tab
        self.engine = sri.SimpleRifeInserter()
        self.engine.set_verbose(True)

        self.layout = QVBoxLayout()

        self.setup_group1()
        self.setup_group2()
        self.setup_group3()
        self.setup_config()
        self.setup_preview()
        self.setup_main_button()

        self.setLayout(self.layout)

    def setup_group1(self):
        # first image
        self.open_image1_button = QPushButton("Open Image")
        self.image1_path_label = QLabel("Open first image")
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
        self.image2_path_label = QLabel("Open second image")
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
        # output folder
        self.open_image3_button = QPushButton("Select Output Folder")
        self.image3_path_label = QLabel("Set Output Folder")
        self.image3_widget = QWidget()
        l = QHBoxLayout()
        l.setMargin(0)
        l.addWidget(self.open_image3_button)
        l.addWidget(self.image3_path_label)
        l.addStretch()
        self.image3_widget.setLayout(l)
        self.open_image3_button.clicked.connect(self.open_output_folder)
        self.layout.addWidget(self.image3_widget)

    def setup_config(self):
        self.edit_label = QLabel("Number of interpolated images")
        self.edit = QSpinBox()
        self.edit.setMaximum(999999)
        self.edit.setMinimum(1)
        self.edit.setValue(5)
        self.show_output = QCheckBox("Show results")
        self.show_output.setChecked(False)

        self.config_widget = QWidget()

        l = QHBoxLayout()
        l.setMargin(0)
        l.addWidget(self.edit_label)
        l.addWidget(self.edit)
        l.addWidget(self.show_output)
        l.addStretch()

        self.config_widget.setLayout(l)

        self.layout.addWidget(self.config_widget)

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

        self.encodeButton = QPushButton("Encode")
        self.encodeButton.clicked.connect(self.encode)

        l.addStretch()
        l.addWidget(self.startButton)
        l.addWidget(self.encodeButton)

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

    def open_output_folder(self):
        fileName = QFileDialog.getExistingDirectory(
            self, "/tmp/out/")

        self.image3_path_label.setText(
            fileName + '/')  # TODO system independent

    def interpolate(self):
        out = self.image3_path_label.text()
        num_images = int(self.edit.text())

        begin = [self.image1_path_label.text(), 0]
        end = [self.image2_path_label.text(), num_images + 1]

        self.engine.interpolate_image_multiple(begin, end, out)

        if self.show_output.isChecked():
            files = glob.glob(out + "*")
            files = sorted(files)
            self.pre = []
            for f in files:
                pre = preview.PreviewWidget(f, 200, 200, f)
                self.pre.append(pre)
                pre.setWindowState(Qt.WindowMaximized)
                pre.show()

    def encode(self):
        out = self.image3_path_label.text()
        video = ffm.input(out + "*.jpg", pattern_type='glob',
                          framerate=20).output(out + "video.mp4").run()


def closeEvent(self, event):
    # close previews
    # TODO doesn't work
    for i in self.pre:
        i.close()
