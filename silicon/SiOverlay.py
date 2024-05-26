from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.Qt import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit

from .SiAnimationObject import *
from .SiLayout import *
from .SiButton import *

class OverlayShowUpAnimation(SiAnimation):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def distance(self):
        return self.target - self.current

    def stepLength(self, dis):
        if abs(dis) <= 1:
            return dis
        else:
            return (abs(dis) * 0.25 + 1) * (1 if dis > 0 else -1)

    def isCompleted(self):
        return self.distance() == 0

class Background(QLabel):
    clicked = QtCore.pyqtSignal()
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()

        event.ignore()


class SiOverlay(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.y_interval = 128  # 中间框架的上留白

        self.showup_animation = OverlayShowUpAnimation(self)
        self.showup_animation.ticked.connect(self.showup_animation_handler)

        self.background = Background(self)
        self.background.setStyleSheet('background-color:rgba(0, 0, 0, 0)')
        self.background.move(0, 0)
        self.background.clicked.connect(self.hide_animation)

        self.frame = QLabel(self)  # 框架

        self.body_frame = QLabel(self.frame)  # 内容框架
        self.body_frame.setStyleSheet('background-color:#252229; border-radius:8px')

        self.opreate_frame = QLabel(self.frame)  # 下方按钮框架
        self.opreate_frame.setStyleSheet('''background-color:#342F39;
                    border-top-left-radius:8px;
                    border-top-right-radius:8px ''')

        self.opreate_layout = SiLayoutH(self.opreate_frame)

        self.body = QLabel(self.frame)  # 内容

        self.init_opreate()

    def init_opreate(self):
        self.btn1 = SiButton(self)
        self.btn1.resize(128, 32)
        self.btn1.setText('取消')
        self.btn1.setStrong(False)

        self.btn2 = SiButton(self)
        self.btn2.resize(128, 32)
        self.btn2.setText('应用')
        self.btn2.setStrong(True)

        self.btn3 = SiButton(self)
        self.btn3.resize(128, 32)
        self.btn3.setText('检查可用性')
        self.btn3.setStrong(False)

        self.opreate_layout.addItem(self.btn1, 'left')
        self.opreate_layout.addItem(self.btn2, 'right')
        self.opreate_layout.addItem(self.btn3, 'right')

    def showup_animation_handler(self, delta):
        v = delta + self.showup_animation.current
        self.moveFrame(v)

        alpha = (1 - v / self.geometry().height()) * 0.5
        if alpha == 0:
            self.hide()
        else:
            self.show()
        self.background.setStyleSheet('background-color:rgba(0, 0, 0, {})'.format((1 - v / self.geometry().height()) * 0.5))
        self.showup_animation.setCurrent(v)

    def moveFrame(self, v):
        w = self.geometry().width()
        bw = self.body.geometry().width()
        mx = (w - bw) // 2
        self.frame.move(mx, int(v + self.y_interval))

    def resizeEvent(self, event):
        size = event.size() # 这里 size 传入的是主界面的宽和高
        w, h = size.width(), size.height()
        bw = self.body.geometry().width()  # 内容的宽度决定了frame及其子对象的宽度

        mx = (w - bw) // 2
        my = self.y_interval
        mw = bw
        mh = h - my

        oh = 80 # 操作栏的高度
        oi = 48 # 操作栏内容距离两侧的距离

        self.background.resize(w, h)
        self.frame.setGeometry(mx, my, mw, mh)
        self.opreate_frame.setGeometry(0, h - oh - my, mw, oh)
        self.opreate_layout.setGeometry(oi, 0, mw - 2 * oi, oh)
        self.body_frame.setGeometry(0, 0, mw, mh)
        self.body.setGeometry(0, 0, mw, mh - oh)

    def show_animation(self):
        self.showup_animation.setTarget(0)
        self.showup_animation.try_to_start()

    def hide_animation(self):
        self.showup_animation.setTarget(self.geometry().height())
        self.showup_animation.try_to_start()
