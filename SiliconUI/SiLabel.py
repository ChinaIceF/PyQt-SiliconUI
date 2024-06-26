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
        self.parent = parent

    def stepLength(self, dis):
        return 2 if dis > 0 else -2

    def distance(self):
        return self.target - self.current

    def isCompleted(self):
        return self.distance() == 0

class MovableLabelMoveAnimation(SiAnimationObject.SiAnimationStandard):
    # 因为这个动画对象的变量是 ndarray，因此需要重写一些方法
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def setTarget(self, x, y):
        self.target = numpy.array([x, y])

    def setCurrent(self, x, y):
        self.current = numpy.array([x, y])

    def stepLength(self, dis):
        if (abs(dis)[0] <= self.bias) and (abs(dis)[1] <= self.bias):
            return dis
        else:
            arr = (abs(dis) * self.factor + self.bias) * (
                numpy.array([(1 if dis[0] > 0 else -1), (1 if dis[1] > 0 else -1)]))
            # 对一个轴上的 dis 进行分析，如果某个轴上差距小于 bias，则返回这个轴上的差距
            if abs(dis)[0] <= self.bias:
                arr[0] = dis[0]
            if abs(dis)[1] <= self.bias:
                arr[1] = dis[1]

            return arr

    def process(self):
        # 如果已经到达既定位置，终止计时器
        if self.isCompleted():
            self.stop()
            return

        dis = self.distance()
        steplength = self.stepLength(dis)

        # 更新数值
        v = self.current + steplength
        self.setCurrent(v[0], v[1])

        # 发射信号
        self.ticked.emit(self.current)

    def isCompleted(self):
        return (self.distance()[0] == 0) and (self.distance()[1] == 0)


class SiLabel(QLabel):
    moved = pyqtSignal(object)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.setFont(SiFont.font_L1)
        self.setStyleSheet('color:{}'.format(colorset.TEXT_GRAD_HEX[0]))

        self.autoAdjustSize = True  # 是否在设置文字时自动调节大小
        self.instant_move = False   # 是否立即移动而不运行动画
        self.move_limits = False    # 是否有限定区域

        self.hint = ''

        self.animation_move = MovableLabelMoveAnimation(self)
        self.animation_move.setFactor(1/3)
        self.animation_move.setBias(1)
        self.animation_move.ticked.connect(self._moveAnimationHandler)


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
        self.animation_move.setCurrent(x, y)
        self.moved.emit([x, y])

    def moveTo(self, x, y):
        # moveTo 方法不同于 move，它经过动画（如果开启）
        x, y = self._legalizeMovingTarget(x, y)
        if self.instant_move == False:
            self.animation_move.setTarget(x, y)
            self.activate()
        else:
            self.move(x, y)

    def activate(self):
        self.animation_move.try_to_start()

    def deactivate(self):
        self.animation_move.stop()

    def isActive(self):
        return self.animation_move.isActive()

    def setInstantMove(self, b):
        self.instant_move = b
        if b == True:  # 如果更改为立即移动，立即终止动画，并完成动画
            self.deactivate()
            x, y = self.animation_move.target
            self.move(x, y)

class SiLabelHasUpdateAnimation(SiLabel):
    def __init__(self, parent):
        super().__init__(parent)

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
        self.parent = parent
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
        self.parent = parent
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
