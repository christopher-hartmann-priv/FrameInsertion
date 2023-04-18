import src.ui as ui
import sys

from PySide2.QtWidgets import QApplication

if __name__ == '__main__':
    '''main function'''

    app = QApplication(sys.argv)

    window = ui.MainWindow()
    window.show()

    sys.exit(app.exec_())
