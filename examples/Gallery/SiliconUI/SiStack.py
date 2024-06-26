from PyQt5.QtWidgets import QLabel
from .SiFont import *
from .SiGlobal import *

class SiStack(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.items = []
        self.h = 0
        self.interval = 8

        # debug 用
        #self.bg = QLabel(self)
        #self.bg.setStyleSheet('background-color:#30ffffff')

    def setInterval(self, interval):
        self.interval = interval

    def setTitle(self, title):  # 如果不运行这个方法，这个组就没有标题
        self.title = QLabel(self)
        self.title.setGeometry(0, 0, 700, 24)  # 底下自己调整
        self.title.setFont(font_L2_bold)
        self.title.setStyleSheet('color: {}'.format(colorset.TEXT_GRAD_HEX[0]))
        self.title.setText(title)
        self.title.adjustSize()

        g = self.title.geometry()
        self.title_highlight = QLabel(self)
        self.title_highlight.setGeometry(0, 12, g.width() + 6, 13)
        self.title_highlight.setStyleSheet('''
            background-color: {};
            border-radius: 4px'''.format(colorset.STK_HL_HEX))
        self.title_highlight.lower()

        self.addH(self.title.height() + self.interval)

    def getH(self):
        return self.h

    def addH(self, num):
        self.h += num

    def addItem(self, option, extra_interval = 0):
        option.setParent(self)
        option.parent = self
        self.items.append(option)

        g = option.geometry()
        option.setGeometry(0, self.h + extra_interval, self.width(), g.height())
        self.addH(g.height() + self.interval + extra_interval)
        self.adjustSize()

    def adjustSize(self):
        g = self.geometry()
        w_max = max([0] + [item.width() for item in self.items])
        self.setGeometry(g.x(), g.y(), max([w_max, g.width()]), self.getH())
        #self.bg.setGeometry(0, 0, g.width(), self.getH())

    def resizeEvent(self, event):
        w = event.size().width()

        for item in self.items:
            g = item.geometry()
            item.resize(w, g.height())
