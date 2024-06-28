from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets

import numpy

from . import SiFont
from . import SiStyle
from . import SiGlobal
from . import SiAnimationObject

from .SiGlobal import *


class LabelTextUpdateAnimation(SiAnimationObject.SiAnimation):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent


    def stepLength(self, dis):
        return 2 if dis > 0 else -2

    def distance(self):
        return self.target - self.current

    def isCompleted(self):
        return self.distance() == 0


class SiLabel(QLabel):
    moved = pyqtSignal(object)
    resized = pyqtSignal(object)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent


        self.setFont(SiFont.font_L1)
        self.setStyleSheet('color:{}'.format(colorset.TEXT_GRAD_HEX[0]))

        self.autoAdjustSize = True  # 是否在设置文字时自动调节大小
        self.instant_move = False   # 是否立即移动而不运行动画
        self.move_limits = False    # 是否有限定区域
        self.instant_resize = False # 是否立即重设大小而不运行动画

        self.hint = ''

        self.animation_move = SiAnimationObject.SiAnimationStandardForArray(self)
        self.animation_move.setFactor(1/3)
        self.animation_move.setBias(1)
        self.animation_move.ticked.connect(self._moveAnimationHandler)

        self.animation_resize = SiAnimationObject.SiAnimationStandardForArray(self)
        self.animation_resize.setFactor(1/3)
        self.animation_resize.setBias(1)
        self.animation_resize.ticked.connect(self._resizeAnimationHandler)

    def _resizeAnimationHandler(self, size_arr):
        w, h = size_arr
        self.resize(int(w), int(h))

    def resizeEvent(self, event):
        # resizeEvent 事件一旦被调用，控件的尺寸会瞬间改变
        # 并且会立即调用动画的 setCurrent 方法，设置动画开始值为 event 中的 size()
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()
        self.animation_resize.setCurrent([w, h])
        self.resized.emit([w, h])

    def resizeTo(self, w, h):
        if self.instant_resize == False and self.isVisible() == True:
            self.animation_resize.setTarget([w, h])
            self.activateResize()
        else:
            self.resize(w, h)

    def setAutoAdjustSize(self, b):
        self.autoAdjustSize = b

    def setHint(self, hint):
        self.hint = hint

    def setText(self, text):
        super().setText(str(text))
        if self.autoAdjustSize == True:
            self.adjustSize()

    def enterEvent(self, event):
        super().enterEvent(event)
        if self.hint != '':
            SiGlobal.floating_window.show_animation()
            SiGlobal.floating_window.setText(self.hint)

    def leaveEvent(self, event):
        super().leaveEvent(event)
        if self.hint != '':
            SiGlobal.floating_window.hide_animation()

    def hasMoveLimits(self):
        return self.move_limits

    def removeMoveLimits(self):
        self.move_limits = False

    def setMoveLimits(self, x1, y1, x2, y2):
        # 拖动控件只能在这个范围内运动
        # 注意！必须满足 x1 <= x2, y1 <= y2
        self.move_limits = True
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def _legalizeMovingTarget(self, x, y):
        # 使移动的位置合法
        if self.move_limits == False:
            return x, y

        x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2
        x = max(x1, min(x2-self.width(), x))
        y = max(y1, min(y2-self.height(), y))
        return x, y

    def _moveAnimationHandler(self, arr):
        x, y = arr
        self.move(int(x), int(y))

    def moveEvent(self, event):
        # moveEvent 事件一旦被调用，控件的位置会瞬间改变
        # 并且会立即调用动画的 setCurrent 方法，设置动画开始值为 event 中的 pos()
        super().moveEvent(event)
        pos = event.pos()
        x, y = pos.x(), pos.y()
        self.animation_move.setCurrent([x, y])
        self.moved.emit([x, y])

    def moveTo(self, x, y):
        # moveTo 方法不同于 move，它经过动画（如果开启）
        x, y = self._legalizeMovingTarget(x, y)
        if self.instant_move == False:
            self.animation_move.setTarget([x, y])
            self.activateMove()
        else:
            self.move(x, y)

    def activateMove(self):
        self.animation_move.try_to_start()

    def deactivateMove(self):
        self.animation_move.stop()

    def isMoveActive(self):
        return self.animation_move.isActive()

    def activateResize(self):
        self.animation_resize.try_to_start()

    def deactivateResize(self):
        self.animation_resize.stop()

    def isResizeActive(self):
        return self.animation_resize.isActive()

    def setInstantMove(self, b):
        self.instant_move = b
        if b == True:  # 如果更改为立即移动，立即终止动画，并完成动画
            self.deactivateMove()
            x, y = self.animation_move.target
            self.move(x, y)

    def setInstantResize(self, b):
        self.instant_resize = b
        if b == True:  # 如果更改为立即移动，立即终止动画，并完成动画
            self.deactivateResize()
            x, y = self.animation_resize.target
            self.move(x, y)

    def propagateAdjustSize(self, widget = None):
        if widget is None:
            widget = self

        # 对比前后两次是否真正调整了大小
        size = [widget.width(), widget.height()]
        widget.adjustSize()

        # 如果调整了大小
        if size != [widget.width(), widget.height()]:
            # 如果有父控件，则继续向上传播
            if widget.parent() is not None:
                self.propagateAdjustSize(widget.parent())
    '''
    def adjustSize(self):
        # 对比前后两次是否真正调整了大小
        size = [self.width(), self.height()]
        super().adjustSize()

        # 如果调整了大小
        if size != [self.width(), self.height()]:
            # 如果有父控件，则继续向上传播
            if self.parent() is not None:
                self.parent.adjustSize()
    '''

class SiLabelHasUpdateAnimation(SiLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent

        self.animation = LabelTextUpdateAnimation(self)
        self.animation.ticked.connect(self._changedAnimationHandler)

    def setAlpha(self, alpha):
        self.setStyleSheet(self.show_stylesheet + ''';
            border-radius: 4px;
            background-color:rgba(255, 255, 255, {});
            '''.format(alpha / 255))

    def _changedAnimationHandler(self, alpha):
        self.setAlpha(alpha)

    def activate(self, *any_args):
        self.animation.setCurrent(40)
        self.animation.setTarget(0)
        self.animation.try_to_start()

    def setText(self, text, ani = False):
        super().setText(text)
        if ani == True:
            self.activate()

    def showEvent(self, event):
        super().showEvent(event)
        self.show_stylesheet = self.styleSheet()


class SiPixLabel(SiLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent

        self.border_radius = 32
        self.blur_radius = 0
        self.path = None

    def setRadius(self, r):
        self.border_radius = r

    def load(self, path):
        self.path = path
        self.draw()

    def draw(self):
        if self.path is None:
            return

        w, h = self.width(), self.height()

        self.target = QPixmap(self.size())
        self.target.fill(Qt.transparent)

        p = QPixmap(self.path).scaled(
            w, h, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        painter = QPainter(self.target)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        path = QPainterPath()
        path.addRoundedRect(0, 0,
                            self.width(),       self.height(),
                            self.border_radius, self.border_radius)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, p)
        self.setPixmap(self.target)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.draw()


class SiDraggableLabel(SiLabel):
    dragged = pyqtSignal(object)
    # 具有跟随功能的标签控件
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent

        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.anchor = event.pos()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
        if not (event.buttons() & Qt.LeftButton):
            return
        newpos = event.pos() - self.anchor + self.frameGeometry().topLeft()
        x, y = self._legalizeMovingTarget(newpos.x(), newpos.y())
        self.moveTo(x, y)
        self.dragged.emit([x, y])

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
