from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import time
import numpy

from . import SiAnimationObject
from . import SiGlobal

class SiScrollBar(QLabel):
    value_change_to_parent = pyqtSignal(float)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        
        self.setMouseTracking(True)  # 开启鼠标追踪

    def mousePressEvent(self, event):
        self.start_pos = self.frameGeometry().topLeft() - event.pos()
        self.start_pos = QCursor.pos()
        self.anchor = self.parent.target_y * self.height() / self.parent.height()

    def mouseMoveEvent(self, event: QMouseEvent):
        if not (event.buttons() & Qt.LeftButton):
            return

        newpos = QCursor.pos() - self.start_pos
        newy = abs(self.anchor) + newpos.y()
        max_y = self.parent.height() - self.height()
        y = int(max(0, min(newy, max_y)))

        self.value_change_to_parent.emit(self.value(y))
        event.accept()

    def value(self, y):
        max_y = self.parent.height() - self.height()
        return y / max_y

    def showEvent(self, event):
        super().showEvent(event)
        self.raise_()

class SiScrollArea(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        
        self.content = None

        self.target_y = 0

        self.scrollbar = SiScrollBar(self)
        self.scrollbar.setStyleSheet('background-color: #7fffffff; border-radius: 4px')
        self.scrollbar.value_change_to_parent.connect(self.bar_pos_to_target_y)

        self.animation = SiAnimationObject.SiAnimation(self.distance, self.stepLength, 1000 / SiGlobal.fps, lambda : self.distance() == 0)
        self.animation.ticked.connect(self.change_position)

    def stepLength(self, dis):
        if abs(dis) > 1:
            return (abs(dis) * 1/6 + 1) * (1 if dis > 0 else -1)
        else:
            return dis

    def distance(self):
        return self.target_y - self.content.y()

    def bar_pos_to_target_y(self, p):
        self.target_y = -int(p * (self.content.height() - self.height()))

        if self.animation.isActive() == False:    # 如果线程没在运行，就启动
            self.animation.start()

    def attach_content(self, content): # 这里的content是一个以这个scrollarea为父对象的东西
        self.content = content
        self.content.setParent(self)
        self.refresh_components()  # 刷新滚动条

    def refresh_components(self):
        g = self.geometry()
        g_content = self.content.geometry()

        self.content.setGeometry(
            g_content.x(), g_content.y(), g.width(), g_content.height())

        h = g.height() * g.height() / g_content.height()

        if g_content.height() <= g.height():
            self.scrollbar.setVisible(False)
        else:
            self.scrollbar.setVisible(True)

            self.scrollbar.setGeometry(g.width() - 8, 0, 8, int(h))
            self.refresh_bar_geometry()

    def change_position(self, y):
        self.content.move(0, int(y))
        self.refresh_bar_geometry()

    def refresh_bar_geometry(self):
        available_range = self.height() - self.scrollbar.height()
        rollable_range = self.content.height() - self.height()
        rolled = abs(self.content.y())

        bar_y =  available_range * rolled / rollable_range
        self.scrollbar.move(self.width() - 8, int(bar_y))

    def wheelEvent(self, event: QWheelEvent):
        strength = 100

        if self.animation.isActive() == False:      # 如果线程没在运行
            if self.scrollbar.isVisible() == True:  # 而且现在有必要滚动，就启动
                self.animation.start()


        temp = self.target_y

        angleDelta = event.angleDelta()   # 获取滚动的角度和滚动方向
        if angleDelta.y() > 0:
            temp += strength
        elif angleDelta.y() < 0:
            temp -= strength

        h = self.content.height()
        h_me = self.height()
        if temp < -h + h_me:
            temp = -h + h_me
        if temp > 0:
            temp = 0

        self.target_y = temp
        if self.scrollbar.isVisible():
            event.accept()

    def resizeEvent(self, event):
        w = event.size().width()

        self.content.resize(w, max(self.content.height(), self.height()))
        self.refresh_components()
