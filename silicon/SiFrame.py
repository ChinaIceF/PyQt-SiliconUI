from PyQt5.QtWidgets import QLabel
from .SiFont import *

class SiFrame(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.items = []
        self.h = 0
        self.interval = 64
        self.delta = 16  # 每个 item 之间的间隔
        self.rightside_interval = 64 # 右边界的距离

    def getH(self):
        return self.h

    def addH(self, num):
        self.h += num

    def addItem(self, stack, addH = True):
        self.items.append(stack)
        stack.setParent(self)
        stack.move(self.interval, self.h)

        g = stack.geometry()
        if addH:
            self.addH(g.height() + self.delta)

        self.adjustSize()

    def adjustSize(self):
        g = self.geometry()
        self.setGeometry(g.x(), g.y(), g.width(), self.getH())


    def resizeEvent(self, event):
        w = event.size().width()

        for item in self.items:
            try:
                if item.noresize == True:
                    continue
            except:
                pass
            g = item.geometry()
            item.resize(w - self.interval - self.rightside_interval, g.height())
