from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import time

from . import SiStyle
from . import SiGlobal
from . import SiAnimationObject
from .SiButton import *
from .SiLayout import *
from .SiGlobal import *

class TabButton(QLabel):
    def __init__(self, parent, func, index):
        super().__init__(parent)
        self.parent = parent
        self.index = index
        self.setStyleSheet('')

        self.button = SiButtonFlat(self)
        self.button.setGeometry(0, 0, 40, 40)
        self.button.setStyleSheet(SiStyle._button_flat_qss)

        self.colorbar = QLabel(self)
        self.colorbar.setStyleSheet('''
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                              stop:0 {}, stop:1 {});
            border-radius:2px'''.format(*colorset.THEME_HEX))
        self.colorbar.setGeometry(0, 10, 4, 20)

        self.button.clicked.connect(lambda : func(self.index))


    def setStatus(self, status):
        if status == True:
            self.setStyleSheet('background-color:{} ;border-radius:6px'.format(colorset.BG_GRAD_HEX[1]))
            self.colorbar.setVisible(True)
        else:
            self.setStyleSheet('')
            self.colorbar.setVisible(False)

    def setIcon(self, path):
        self.button.load(path)


class AnimationTab(SiAnimationObject.SiAnimation):
    def __init__(self, parent):
        super().__init__(parent)

    def distance(self):
        return self.target - self.current

    def stepLength(self, dis):
        if abs(dis) <= 1:
            return dis
        else:
            return (abs(dis) * 1/5 + 1) * (1 if dis > 0 else -1)

    def isCompleted(self):
        return self.distance() == 0

class SiTabArea(QLabel):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.animation = AnimationTab(self)
        self.animation.ticked.connect(self.change_content_position)
        self.animation.setTarget(0)

        # 设定图标栏宽度
        self.icon_area_w = 48 + 8
        self.interval = 0
        self.title_interval = 64

        self.animation_h = 64  # 动画开始的高度

        self.icon_h = self.title_interval
        self.content = []
        self.icon = []

        self.bg = QLabel(self)
        self.bg.setGeometry(0, 0, 0, 0)
        self.bg.setStyleSheet('background-color: {}'.format(colorset.BG_GRAD_HEX[0]))

        self.content_bg = QLabel(self)
        self.content_bg.setGeometry(self.icon_area_w + self.interval, self.title_interval, 0, 0)
        self.content_bg.setStyleSheet('''
            background-color: {};
            border-top-left-radius:6px;
            border:1px solid {}'''.format(colorset.BG_GRAD_HEX[1], colorset.BG_GRAD_HEX[2]))

        self.content_area = QLabel(self)
        self.content_area.setGeometry(self.icon_area_w + self.interval, self.title_interval, 0, 0)
        self.content_area.setStyleSheet('')

        self.icon_layout = SiLayoutV(self)
        self.icon_layout.setCenter(True)
        self.icon_layout.setInterval(8)

        self.details_icon = TabButton(self.icon_layout, self.setShowing, 0)
        self.details_icon.setGeometry(8, 12, 40, 40)
        self.details_icon.setIcon(SiGlobal.icons.get('fi-rr-menu-burger'))
        self.details_icon.setStatus(False)
        self.icon_layout.addItem(self.details_icon, 'top')

    def change_content_position(self, y):
        g = self.content[self.index].geometry()
        self.content[self.index].move(0, int(y))

    def addTab(self, obj, icon_path, hint, side = 'top'):
        obj.setParent(self.content_area)
        obj.setStyleSheet('')
        obj.setGeometry(0, 0, 0, 0)

        icon = TabButton(self.icon_layout, self.setShowing, len(self.content))
        icon.button.setHint(hint)
        icon.setIcon(icon_path)
        icon.setGeometry(8, self.icon_h, 40, 40)

        if len(self.content) == 0:
            icon.setStatus(True)
        else:
            icon.setStatus(False)
            obj.setVisible(False)

        self.icon_h += 48

        self.content.append(obj)
        self.icon.append(icon)
        self.icon_layout.addItem(icon, side)

        self.refresh_content_size()

    def setShowing(self, index):
        self.index = index
        for i in range(len(self.content)):
            self.content[i].setVisible(False)
            self.content[i].move(0, self.animation_h)
            self.icon[i].setStatus(False)

        self.content[index].setVisible(True)
        self.icon[index].setStatus(True)

        self.animation.setCurrent(self.animation_h)
        self.animation.try_to_start()

    def resizeEvent(self, event):
        w = event.size().width()
        h = event.size().height()

        content_w = w - self.icon_area_w - self.interval

        self.resize(w, h)
        self.bg.resize(w, h)

        self.icon_layout.setGeometry(0, 16, self.icon_area_w, h- 24)
        #self.stack_icon_area.resize(self.icon_area_w, h)
        self.content_area.resize(content_w, h - self.title_interval)
        self.content_bg.resize(content_w, h - self.title_interval)

        self.refresh_content_size()

    def refresh_content_size(self):
        g = self.geometry()
        for c in self.content:
            c.resize(g.width() - self.icon_area_w - self.interval, g.height() - self.title_interval)

    def showEvent(self, event):
        self.setShowing(0)
