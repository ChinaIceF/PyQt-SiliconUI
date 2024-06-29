from PyQt5.Qt import *
from PyQt5.QtWidgets import *

from .SiGlobal import *
from .SiFont import *

class SiInfo(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        
        self.type = 0
        self.color = colorset.INF_HEX

        self.interval_h = 10
        self.interval_w = 16

        self.background = QLabel(self)
        self.background.setStyleSheet('border-radius: 6px')

        self.title = QLabel(self)
        self.title.setStyleSheet('color:#b0ffffff')
        self.title.setFont(font_L1_bold)

        self.divition_line = QLabel(self)
        self.divition_line.setStyleSheet('background-color:#30ffffff')

        self.discription = QLabel(self)
        self.discription.setStyleSheet('color:#90ffffff')
        self.discription.setFont(font_L1)
        self.discription.setWordWrap(True)

        self.setType(self.type)

    def setType(self, type):
        self.type = type
        self.background.setStyleSheet('''
            border-radius: 6px;
            background-color:{} '''.format(self.color[self.type]))

    def setContent(self, title, discription):
        self.title.setText(title)
        self.discription.setText(discription)
        self.discription.adjustSize()
        self.adjustSize_()

    def adjustSize_(self):
        h = self.discription.geometry().height()
        self.resize(0, h + self.interval_h * 4 + 16 + 1)

    def setFixedWidth(self, width):
        super().setFixedWidth(width + self.interval_w * 2)
        self.discription.setFixedWidth(width)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), self.height()
        cw = w - 2 * self.interval_w
        ch = h - 2 * self.interval_h

        self.background.resize(w, h)
        self.title.setGeometry(self.interval_w, self.interval_h, cw, 16)
        self.divition_line.setGeometry(self.interval_w, self.interval_h + 16 + self.interval_h, cw, 1)
        self.discription.setGeometry(
            self.interval_w,
            self.interval_h + 16 + self.interval_h + self.interval_h,
            cw,
            ch - 16 - 2 * self.interval_h
        )
