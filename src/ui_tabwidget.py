# for ... everything?
from PySide2.QtWidgets import QWidget, QTabWidget

# for individual tabs
import src.ui_singlewidget as single
import src.ui_multiplewidget as multi
import src.ui_dynamicwidget as dynamic


class TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super(TabWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.tab1 = single.SingleInterpolationWidget()
        self.tab2 = multi.MultipleInterpolationWidget()
        self.tab3 = QWidget()  # TODO dummy
        self.tab4 = dynamic.DynamicInterpolationWidget()
        self.tab5 = QWidget()  # TODO dummy
        self.tab6 = QWidget()  # TODO dummy
        self.addTab(self.tab1, "Single Interpolation")
        self.addTab(self.tab2, "Recursive Interpolation")
        #self.addTab(self.tab3, "Static Recursive Interpolation")
        self.addTab(self.tab4, "Dynamic Recursive Interpolations")
        self.addTab(self.tab5, "Rife Configuration")
        self.addTab(self.tab6, "Encoder Configuration")
