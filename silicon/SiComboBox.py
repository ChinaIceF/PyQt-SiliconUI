from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QLabel, QDialog, QPushButton
from PyQt5.QtSvg import QSvgWidget

from . import SiFont
from . import SiGlobal
from .SiMenu import *
from .SiButton import *

class SiComboBox(ClickableLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.highlight_alpha = 4
        self.setHoverAnimation(True)

        self.arrow = QSvgWidget(self)
        self.arrow.lower()
        self.arrow.resize(16, 16)
        self.arrow.load(SiGlobal.icons.get('fi-rr-angle-small-down'))

        self.label = QLabel(self)
        self.label.lower()
        self.label.setStyleSheet('''
            background-color:#252229;
            padding-left: 12px;
            padding-right: 12px;
            border-radius: 4px;
            color: #ffffff;
            ''')
        self.label.setFont(SiFont.font_L1)
        self.label.setText('测试文字')

        self.menu = SiMenu(None)
        self.menu.textChanged.connect(lambda x: self.label.setText(x))

        self.clicked.connect(self.popup)

    def addOption(self, name, value):
        self.menu.addOption(name, value)

    def setOption(self, name):
        self.menu.setOption(name)

    def popup(self):
        global_pos = self.label.mapToGlobal(self.label.pos())
        self.menu.popup(global_pos.x() - self.menu.margin, global_pos.y() + 24)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.label.resize(w, h)
        self.arrow.move(w - 24, (h-16)//2)
        self.menu.resize(w + 2 * self.menu.margin, self.menu.height())

    def initialize_stylesheet(self):
        pass
