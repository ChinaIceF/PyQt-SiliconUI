from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.Qt import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit

class SiLayoutV(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.contents_top = []
        self.contents_bottom = []
        self.align_center = False

        self.interval = 16

    def setCenter(self, b):
        self.align_center = b

    def setInterval(self, interval):
        self.interval = interval

    def addVacant(self, length, side = 'top'):
        new_label = QLabel(self)
        new_label.setStyleSheet('')
        new_label.resize(0, length)
        self.addItem(new_label, side = side)

    def addItem(self, item, side = 'top'):
        item.setParent(self)
        item.parent = self

        if side != 'top' and side != 'bottom':
            raise ValueError(side)

        if side == 'top':
            self.contents_top.append(item)
        if side == 'bottom':
            self.contents_bottom.append(item)
        self.refresh_components()
        self.adjustSize()

    def refresh_components(self):
        size = self.geometry()
        w, h = size.width(), size.height()

        top_used = 0
        bottom_used = 0

        for obj in self.contents_top:
            obj_geo = obj.geometry()
            ow, oh = obj_geo.width(), obj_geo.height()
            obj.move((w - ow)//2 if self.align_center else 0, top_used)
            top_used += oh + self.interval

        for obj in self.contents_bottom:
            obj_geo = obj.geometry()
            ow, oh = obj_geo.width(), obj_geo.height()
            obj.move((w - ow)//2 if self.align_center else 0, h - oh - bottom_used)
            bottom_used += oh + self.interval

        total_used = top_used + bottom_used
        total_used -= 0 if self.contents_top == [] else self.interval
        total_used -= 0 if self.contents_bottom == [] else self.interval

        self.setMinimumSize(0, total_used)

    def resizeEvent(self, event):
        self.refresh_components()

    def adjustSize(self):

        top_used = 0
        bottom_used = 0
        for obj in self.contents_top:
            top_used += obj.height() + self.interval
        for obj in self.contents_bottom:
            bottom_used += obj.height() + self.interval
        total_used = top_used + bottom_used
        total_used -= 0 if self.contents_top == [] else self.interval
        total_used -= 0 if self.contents_bottom == [] else self.interval
        prefered_h = total_used

        prefered_w = 0
        for obj in (self.contents_top + self.contents_bottom):
            if obj.width() > prefered_w:
                prefered_w = obj.width()   # 找最大的宽度

        prefered_w = max(prefered_w, self.width())
        prefered_h = max(prefered_h, self.height())

        self.resize(prefered_w, prefered_h)

class SiLayoutH(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.contents_left = []
        self.contents_right = []
        self.interval = 16
        self.align_center = False

    def setCenter(self, b):
        self.align_center = b

    def setInterval(self, interval):
        self.interval = interval

    def addVacant(self, length, side = 'left'):
        new_label = QLabel(self)
        new_label.setStyleSheet('')
        new_label.resize(length, 0)
        self.addItem(new_label, side = side)

    def addItem(self, item, side = 'left'):
        item.setParent(self)
        item.parent = self

        if side != 'left' and side != 'right':
            raise ValueError(side)

        if side == 'left':
            self.contents_left.append(item)
        if side == 'right':
            self.contents_right.append(item)
        self.refresh_components()
        self.adjustSize()

    def refresh_components(self):
        size = self.geometry()
        w, h = size.width(), size.height()

        left_used = 0
        right_used = 0

        for obj in self.contents_left:
            obj_geo = obj.geometry()
            ow, oh = obj_geo.width(), obj_geo.height()
            obj.move(left_used, (h - oh) // 2 if self.align_center else 0)
            left_used += ow + self.interval

        for obj in self.contents_right:
            obj_geo = obj.geometry()
            ow, oh = obj_geo.width(), obj_geo.height()
            obj.move(w - ow - right_used, (h - oh) // 2 if self.align_center else 0)
            right_used += ow + self.interval

        total_used = left_used + right_used
        total_used -= 0 if self.contents_left == [] else self.interval
        total_used -= 0 if self.contents_right == [] else self.interval

        self.setMinimumSize(total_used, 0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.refresh_components()

    def adjustSize(self):
        left_used = 0
        right_used = 0
        for obj in self.contents_left:
            left_used += obj.width() + self.interval
        for obj in self.contents_right:
            right_used += obj.width() + self.interval
        total_used = left_used + right_used
        total_used -= 0 if self.contents_left == [] else self.interval
        total_used -= 0 if self.contents_right == [] else self.interval
        prefered_w = total_used

        prefered_h = 0
        for obj in (self.contents_left + self.contents_right):
            if obj.height() > prefered_h:
                prefered_h = obj.height()   # 找最大的宽度


        prefered_w = max(prefered_w, self.width())
        prefered_h = max(prefered_h, self.height())

        self.resize(prefered_w, prefered_h)
