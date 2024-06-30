from .SiAnimationObject import *
from .SiButton import *
from .SiGlobal import *


class SubInterface(object):
    def __init__(self):
        self.width_ = 700
        self.body = None
        self.operation = None
        self.name = None

    def get(self):
        return self.body, self.operation, self.width_, self.name


class OverlayShowUpAnimation(SiAnimation):
    def __init__(self, parent):
        super().__init__()

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

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        event.ignore()

    def enterEvent(self, event):
        super().enterEvent(event)
        event.ignore()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        event.ignore()


class SiOverlay(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.y_interval = 128  # 中间框架的上留白
        self.width_ = 700

        self.showup_animation = OverlayShowUpAnimation(self)
        self.showup_animation.ticked.connect(self.showup_animation_handler)

        self.background = Background(self)
        self.background.setStyleSheet("background-color:rgba(0, 0, 0, 0)")
        self.background.move(0, 0)
        self.background.clicked.connect(self.hide_animation)

        self.frame = QLabel(self)  # 框架

        self.body_frame = QLabel(self.frame)  # 内容框架
        self.body_frame.setStyleSheet(
            """
            background-color: {};
            border-radius:8px""".format(colorset.BG_GRAD_HEX[1])
        )

        self.operate_frame = QLabel(self.frame)  # 下方按钮框架
        self.operate_frame.setStyleSheet(
            """
            background-color:{};
            border-top-left-radius:8px;
            border-top-right-radius:8px """.format(colorset.BG_GRAD_HEX[3])
        )

        self.operation = QWidget(self.operate_frame)  # 确保 self.operation 被正确初始化
        self.body = QWidget(self.body_frame)  # 确保 self.body 被正确初始化

        self.subinterface = []

    def showup_animation_handler(self, value):
        self.moveFrame(value)

        alpha = (1 - value / self.height()) * 0.5
        if alpha == 0:
            self.hide()
        else:
            self.show()
        self.background.setStyleSheet("background-color:rgba(0, 0, 0, {})".format((1 - value / self.height()) * 0.5))

    def moveFrame(self, v):
        w = self.width()
        bw = self.width_
        mx = (w - bw) // 2
        self.frame.move(mx, int(v + self.y_interval))

    def resizeEvent(self, event):
        size = event.size()  # 这里 size 传入的是主界面的宽和高
        w, h = size.width(), size.height()
        self.refreshSize(w, h)

    def refreshSize(self, w, h):
        bw = self.width_  # 宽度设置决定了frame及其子对象的宽度

        mx = (w - bw) // 2
        my = self.y_interval
        mw = bw
        mh = h - my

        oh = 80  # 操作栏的高度
        oi = 48  # 操作栏内容距离两侧的距离

        self.background.resize(w, h)
        self.frame.setGeometry(mx, my, mw, mh)
        self.operate_frame.setGeometry(0, h - oh - my, mw, oh)
        self.body_frame.setGeometry(0, 0, mw, mh)
        try:
            self.operation.setGeometry(oi, 0, mw - 2 * oi, oh)
            self.body.setGeometry(0, 0, mw, mh - oh)
        except Exception as e:
            print("SiOverlay 重设大小出错", e)

    def show_animation(self):
        self.showup_animation.setTarget(0)
        self.showup_animation.try_to_start()

    def hide_animation(self):
        self.showup_animation.setTarget(self.height())
        self.showup_animation.try_to_start()

    def addInterface(self, interface):
        body, operation, width, name = interface.get()

        body.setParent(self.frame)
        operation.setParent(self.operate_frame)

        body.setVisible(False)
        operation.setVisible(False)

        self.subinterface.append(interface)

    def setInterface(self, name):
        for interface in self.subinterface:
            body, operation, width, name_ = interface.get()
            body.setVisible(False)
            operation.setVisible(False)

        for interface in self.subinterface:
            if interface.name == name:
                body, operation, width, name = interface.get()
                self.body, self.operation, self.width_ = body, operation, width
                self.body.setVisible(True)
                self.operation.setVisible(True)
                self.refreshSize(self.width(), self.height())
                return
