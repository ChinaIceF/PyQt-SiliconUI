from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.Qt import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit
import numpy
import time
import os

import silicon
import silicon.SiGlobal as SiGlobal

class Options(silicon.SiFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet('')

        ## ================ Stack 开始 ===================

        self.stack_about = silicon.SiStack(self)
        self.stack_about.setTitle('关于')

        self.about = silicon.SiOption(self.stack_about)
        self.about.setText('关于 Silicon UI','<strong>版本号</strong> 1.01&nbsp;&nbsp;&nbsp;<strong>构建日期</strong> 2024.05.26')
        self.about.setIcon('./svg/darkmode/fi-rr-info.svg')

        self.license = silicon.SiOption(self.stack_about)
        self.license.setText('开源许可','本项目遵循 GNU General Public License v3.0')
        self.license.setIcon('./svg/darkmode/fi-rr-diploma.svg')

        self.copyright = silicon.SiOption(self.stack_about)
        self.copyright.setText('版权','<strong>霏泠冰 IceF</strong> 版权所有')
        self.copyright.setIcon('./svg/darkmode/fi-rr-copyright.svg')

        # 添加
        self.stack_about.addItem(self.about)
        self.stack_about.addItem(self.license)
        self.stack_about.addItem(self.copyright)

        self.addItem(self.stack_about)
