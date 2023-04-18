# for ... everything?
from fileinput import filename
from multiprocessing import Event
from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView

# for events
from PySide2.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent


# for rife
import src.insert_frame as sri

# for previewing
import src.ui_previewwidget as preview

# for encoding
import ffmpeg as ffm


class DynamicInterpolationWidget(QWidget):
    def __init__(self, parent=None):
        super(DynamicInterpolationWidget, self).__init__(parent)
        self.setAcceptDrops(True)

        # TODO get parameters from config tab
        self.engine = sri.SimpleRifeInserter()
        self.engine.set_verbose(True)

        self.layout = QVBoxLayout()

        self.setup_table()
        self.setup_output()
        self.setup_main_button()

        self.setLayout(self.layout)

    def setup_table(self):
        self.table_widget = QTableWidget(0, 2)
        column_names = ["Index", "Image"]

        self.__image_size = 200

        self.table_widget.verticalHeader().setDefaultSectionSize(self.__image_size)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.setHorizontalHeaderLabels(column_names)
        self.table_widget.setAcceptDrops(True)

        self.layout.addWidget(self.table_widget)

    def add_row(self, image_path: str) -> None:
        row = self.table_widget.rowCount()
        self.table_widget.insertRow(row)
        item = QTableWidgetItem()
        item.setText(str(row))  # TODO previous index + 1
        self.table_widget.setItem(row, 0, item)
        self.table_widget.setCellWidget(row, 1, preview.PreviewWidget(
            image_path, self.__image_size, self.__image_size, ""))

    def setup_output(self):
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

    def setup_main_button(self):
        # "start" button

        self.button_widget = QWidget()
        l = QHBoxLayout()
        l.setMargin(0)

        self.clearButton = QPushButton("Clear Table")
        self.clearButton.clicked.connect(self.clear_table)

        self.startButton = QPushButton("Interpolate")
        self.startButton.clicked.connect(self.interpolate)

        self.encodeButton = QPushButton("Encode")
        self.encodeButton.clicked.connect(self.encode)

        l.addWidget(self.clearButton)
        l.addStretch()
        l.addWidget(self.startButton)
        l.addWidget(self.encodeButton)

        self.button_widget.setLayout(l)

        self.layout.addWidget(self.button_widget)

    def open_output_folder(self):
        fileName = QFileDialog.getExistingDirectory(
            self, "/tmp/out/")

        self.image3_path_label.setText(
            fileName + '/')  # TODO system independent

    def __row_helper(self, row_index):
        index_column = 0
        content_column = 1

        file_index = int(self.table_widget.item(
            row_index, index_column).text())

        file_name = self.table_widget.cellWidget(
            row_index, content_column).get_image_path()

        return [file_name, file_index]

    def interpolate(self) -> None:
        out_folder = self.image3_path_label.text()

        for i in range(0, self.table_widget.rowCount() - 1):

            begin = self.__row_helper(i)
            end = self.__row_helper(i + 1)

            self.engine.interpolate_image_multiple(begin, end, out_folder)

    def clear_table(self) -> None:
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            # if event.mimeData().text().find("file://"):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        location = event.mimeData().text()
        list = location.splitlines()

        for loc in list:
            print(loc)
            self.add_row(loc.removeprefix("file://"))

    def encode(self, file_name: str = "out", file_format_out: str = ".mp4") -> None:
        # TODO output video format
        out_file = self.image3_path_label.text()

        file_format_in = self.table_widget.cellWidget(
            0, 1).get_image_path().split(".")

        file_format_in = file_format_in[len(file_format_in)-1]

        input = ffm.input(out_file + "*." + file_format_in,
                          pattern_type='glob', framerate=600)

        # TODO quality improvements
        output = ffm.output(input, out_file + file_name + file_format_out)
        ffm.run(output, overwrite_output=True)
