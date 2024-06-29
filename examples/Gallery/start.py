
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

import ui as ui

if __name__ == '__main__':

    # 适应高DPI设备
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    Window = ui.UserInterface()
    Window.show()
    sys.exit(app.exec_())
