from PyQt5.QtWidgets import QLabel
from .SiFont import *

class SiStack(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.items = []
        self.h = 0

        # debug 用
        #self.bg = QLabel(self)
        #self.bg.setStyleSheet('background-color:#30ffffff')

    def setTitle(self, title):  # 如果不运行这个方法，这个组就没有标题
        self.title = QLabel(self)
        self.title.setGeometry(0, 0, 700, 24)  # 底下自己调整
        self.title.setFont(font_L2_bold)
        self.title.setStyleSheet('color: #fafafa')
        self.title.setText(title)
        self.title.adjustSize()

        g = self.title.geometry()
        self.title_highlight = QLabel(self)
        self.title_highlight.setGeometry(0, 12, g.width() + 6, 13)
        self.title_highlight.setStyleSheet('background-color: #609c4e8b; border-radius: 4px')
        self.title_highlight.lower()

        self.addH(self.title.geometry().height() + 8)

    def getH(self):
        return self.h

    def addH(self, num):
        self.h += num

    def addItem(self, option):
        option.setParent(self)
        option.parent = self
        self.items.append(option)

        g = option.geometry()

        option.move(0, self.h)
        option.setGeometry(0, self.h, self.geometry().width(), g.height())

        self.addH(g.height() + 8)

        self.adjustSize()

    def adjustSize(self):
        g = self.geometry()
        self.setGeometry(g.x(), g.y(), g.width(), self.getH())
        #self.bg.setGeometry(0, 0, g.width(), self.getH())

    def resizeEvent(self, event):
        w = event.size().width()

        for item in self.items:
            g = item.geometry()
            item.resize(w, g.height())
