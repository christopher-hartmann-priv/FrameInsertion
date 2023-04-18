# for ... everything?
from PySide2.QtWidgets import QWidget, QVBoxLayout

# for tabbed widget
import src.ui_tabwidget as TabWidget


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Simple Rife Frame Interpolation UI")
        self.setAcceptDrops(True)

        # tabwidget
        self.tabs = TabWidget.TabWidget()
        layout = QVBoxLayout()

        layout.addWidget(self.tabs)
        layout.setMargin(2)

        self.setMinimumHeight(800)
        self.setMinimumWidth(1200)
        self.setLayout(layout)
