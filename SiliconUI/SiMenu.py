from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy

from . import SiGlobal

from .SiFont import *
from .SiLayout import *
from .SiAnimationObject import *
from .SiGlobal import *


class OptionHoverAnimation(SiAnimation):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent

    def stepLength(self, dis):
        return 2 if dis > 0 else -2

    def distance(self):
        return self.target - self.current

    def isCompleted(self):
        return self.distance() == 0


class PopupAnimation(SiAnimation):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent
        self.parent = parent

    def distance(self):
        return self.target - self.current

    def stepLength(self, dis):
        if abs(dis) <= 1:
            return dis
        else:
            return (abs(dis) * 1/8 + 1) * (1 if dis > 0 else -1)

    def isCompleted(self):
        return self.distance() == 0

    def stop(self):
        super().stop()
        if self.target == 0:
            self.parent.close()


class SingleOption(QLabel):
    clicked = pyqtSignal(list)

    def __init__(self, parent, name, value):
        super().__init__(parent)
        self.parent =  parent

        self.name = name
        self.value = value

        self.clicked.connect(self.parent._changeHandler)

        self.resize(self.parent.geometry().width(), 32)
        self.setText(name)
        self.setFont(font_L1)
        self.setStyleSheet('padding-left: 12px; padding-right: 12px; color:{};'.format(colorset.TEXT_GRAD_HEX[0]))

        self.colorbar = QLabel(self)
        self.colorbar.lower()
        self.colorbar.setVisible(False)
        self.colorbar.setStyleSheet('''
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #30{}, stop:1 #30{});
            border-radius:6px; '''.format(colorset.THEME_HEX[0][1:], colorset.THEME_HEX[1][1:]))

        self.animation = OptionHoverAnimation(self)
        self.animation.ticked.connect(self._hoverAnimationHandler)

    def _hoverAnimationHandler(self, alpha):
        self.setStyleSheet('''
            padding-left: 12px;
            padding-right: 12px;
            color:{};
            background-color:rgba(255, 255, 255, {})'''.format(colorset.TEXT_GRAD_HEX[0], alpha))

    def enterEvent(self, event):
        super().enterEvent(event)
        self.animation.setTarget(12)
        self.animation.try_to_start()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self.animation.setTarget(0)
        self.animation.try_to_start()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.clicked.emit([self.name, self.value])

    def value(self):
        return self.value

    def name(self):
        return self.name

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.colorbar.resize(event.size().width(), event.size().height())

class MenuBody(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent

        self.options_label = []
        self.layout = SiLayoutV(self)
        self.layout.interval = 2
        self.preferred_height = 0

        self.setStyleSheet('background-color: {}; border-radius: 6px'.format(colorset.BG_GRAD_HEX[2]))

    def addOption(self, name, value):
        new_option = SingleOption(self, name, value)
        self.layout.addItem(new_option)
        self.options_label.append(new_option)
        self.adjustSize()

    def adjustSize(self):
        self.layout.adjustSize()
        g = self.layout.geometry()
        self.resize(self.width(), g.height())
        self.preferred_height = g.height()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()
        self.layout.resize(w, h)
        for obj in self.options_label:
            obj.resize(w, obj.geometry().height())

    def _changeHandler(self, list_):
        name, value = list_
        for obj in self.options_label:
            if obj.name == name:
                obj.colorbar.setVisible(True)
            else:
                obj.colorbar.setVisible(False)
        self.parent.textChanged.emit(name)
        self.parent.valueChanged.emit(value)
        self.parent.closeup()

class SiMenu(QWidget):
    valueChanged = pyqtSignal(object)
    textChanged = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent

        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.status = False    # 展开为 True

        self.menubody = MenuBody(self)
        self.popup_animation = PopupAnimation(self)
        self.popup_animation.ticked.connect(self._popupAnimationHandler)

        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(0, 0, 0, 128))
        shadow.setOffset(0, 0)
        shadow.setBlurRadius(16)
        self.menubody.setGraphicsEffect(shadow)

        self.direction = 1
        self.margin = 16  # 目录距离边框有多远

    def closeEvent(self, event):
        super().closeEvent(event)
        self.status = False

    def setOption(self, name):
        for obj in self.menubody.options_label:
            if obj.name == name:
                self.menubody._changeHandler([obj.name, obj.value])
                return
        print('未找到选项名为', name)
        obj = self.menubody.options_label[0]
        self.menubody._changeHandler([obj.name, obj.value])

    def addOption(self, name, value):
        self.menubody.addOption(name, value)

    def isReversed(self):
        return False if self.direction == 1 else True

    def isUnfold(self):
        return self.status

    def _popupAnimationHandler(self, h):
        # 阴影有问题，所以需要采用重设大小的方法
        g = self.menubody.geometry()
        x, y, w, h = g.x(), g.y(), g.width(), int(h)

        if self.isReversed() == False:
            self.menubody.resize(w, h)
        else:
            self.menubody.setGeometry(x, self.height() - self.margin - h, w, h)

    def _adjustedPopupPosAndDirection(self, x, y, w, h):
        # 获取合适的弹出位置，避免显示在有效显示范围之外
        #
        # x     : int 弹出缝的左侧全局坐标
        # y     : int 弹出缝的左侧全局坐标
        # w     : int 菜单的宽度
        # h     : int 菜单的高度

        margin = 24
        direction = 1
        desktop_geo = QApplication.desktop().geometry()
        dw, dh = desktop_geo.width(), desktop_geo.height()
        # 宽度上，压缩到有效显示范围内
        if (margin <= x <= dw - margin - w) == False:
            x = margin if x < margin else dw - margin - w
        # 高度上，调整弹出方向
        if (margin <= y <= dh - margin - h) == False:
            if y < margin: # 位置偏高
                direction = 1  # 向下弹出
                y = margin
            if y > dh - margin - h: # 位置偏低
                direction = -1  # 向上弹出
                y = dh - margin - h

        return x, y, direction

    def popup(self, x, y):
        # 弹出菜单
        #
        # x     : int 弹出缝的左侧全局坐标
        # y     : int 弹出缝的左侧全局坐标

        if self.status == True:
            self.closeup()
            return

        self.show()
        self.status = True
        margin = self.margin   # 弹出缝比目录左右宽多少
        g = self.menubody.geometry()
        w, h = g.width(), self.menubody.preferred_height
        x, y, direction = self._adjustedPopupPosAndDirection(x, y, w, h)

        self.direction = direction
        self.setGeometry(x, y, w + 2 * margin, self.menubody.preferred_height + 2 * margin)

        if self.isReversed() == False:
            self.menubody.setGeometry(margin, margin, w, 0)  # 内容就绪
        else:
            self.menubody.setGeometry(margin, self.menubody.preferred_height - margin, w, 0)

        # 设置动画的起点和终点，动画操作对象是目录
        self.popup_animation.setCurrent(0)
        self.popup_animation.setTarget(self.menubody.preferred_height)
        self.popup_animation.try_to_start()

    def closeup(self):
        self.popup_animation.setTarget(0)
        self.popup_animation.try_to_start()

    def resize(self, w, h):
        super().resize(w, h)
        self.menubody.resize(w - 2 * self.margin, self.menubody.height())
