
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

import ui as ui
import SiliconUI


if __name__ == '__main__':

    # 适应高DPI设备
    #QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    # 适应Windows缩放
    #QtGui.QGuiApplication.setAttribute(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.Ceil)


    app = QApplication(sys.argv)
    Window = ui.UserInterface()
    Window.show()
    sys.exit(app.exec_())
