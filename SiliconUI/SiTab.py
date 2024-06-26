from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets

from .SiFont import *
from .SiScrollArea import *
from .SiGlobal import *

class SiTab(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet('')

        self.title_height = 96
        self.left_margin = 64

        self.scrollarea = SiScrollArea(self)
        self.scrollarea.setGeometry(0, self.title_height, 0, 0)

    def setTitleHeight(self, height):
        self.title_height = height
        self.scrollarea.setGeometry(0, height, 0, 0)

    def attachFrame(self, obj):
        self.frame = obj
        self.scrollarea.attach_content(self.frame)

    def setTitle(self, title):  # 如果不运行这个方法，这个组就没有标题
        self.title = QLabel(self)
        self.title.setGeometry(self.left_margin, 32, 0, self.title_height)  # 底下自己调整
        self.title.setFont(font_L3_bold)
        self.title.setStyleSheet('color: {}'.format(colorset.TEXT_GRAD_HEX[0]))
        self.title.setText(title)
        self.title.adjustSize()

    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()

        self.resize(w, h)
        self.scrollarea.resize(w, h - self.title_height)
