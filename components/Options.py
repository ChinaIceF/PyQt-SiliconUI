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
        self.about.setIcon(SiGlobal.icons.get('fi-rr-info'))

        self.license = silicon.SiOption(self.stack_about)
        self.license.setText('开源许可','本项目遵循 GNU General Public License v3.0')
        self.license.setIcon(SiGlobal.icons.get('fi-rr-diploma'))

        self.copyright = silicon.SiOption(self.stack_about)
        self.copyright.setText('版权','<strong>霏泠冰 IceF</strong> 版权所有')
        self.copyright.setIcon(SiGlobal.icons.get('fi-rr-copyright'))

        # 添加
        self.stack_about.addItem(self.about)
        self.stack_about.addItem(self.license)
        self.stack_about.addItem(self.copyright)

        ## ================ Stack 开始 ===================

        self.stack_quotes = silicon.SiStack(self)
        self.stack_quotes.setTitle('第三方资源')

        self.icons = silicon.SiOptionSourceCode(self.stack_about)
        self.icons._setMinimumHeight(80)
        self.icons.setText('图标','Silicon Gallery 使用了 FLATICON 的图标，<strong>这些图标不应被认为是 Silicon UI 的一部分</strong>')
        self.icons.setIcon(SiGlobal.icons.get('fi-rr-quote-right'))
        self.icons.load(SiGlobal.icons.get('fi-rr-link'))
        self.icons.setURL('www.flaticon.com')

        self.stack_quotes.addItem(self.icons)


        self.addItem(self.stack_about)
        self.addItem(self.stack_quotes)
