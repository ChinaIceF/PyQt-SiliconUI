
import sys

import ui as ui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

import siui

siui.gui.set_scale_factor(1)

if __name__ == "__main__":

    # 适应高DPI设备
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    Window = ui.UserInterface()
    Window.show()
    sys.exit(app.exec_())
