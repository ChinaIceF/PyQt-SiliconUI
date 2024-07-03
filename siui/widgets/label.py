from PyQt5.QtCore import QPoint, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPainterPath, QPixmap

from siui.core.animation import SiExpAnimation
from siui.core.color import Color
from siui.widgets.abstracts import ABCAnimatedLabel


class SiLabel(ABCAnimatedLabel):
    def __init__(self, parent=None):
        super().__init__(parent)


class SiColoredLabel(ABCAnimatedLabel):
    """
    面向显示颜色的标签，支持改变颜色动画
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.animation_color = SiExpAnimation(self)
        self.animation_color.setFactor(1/4)
        self.animation_color.setBias(1)
        self.animation_color.ticked.connect(self._set_color_handler)

        self.getAnimationGroup().addMember(self.animation_color, "color")

    def setColorTo(self, color_code):
        """
        设置目标颜色，同时启动动画
        :param color_code: 色号
        :return:
        """
        self.animation_color.setTarget(Color.decodeColor(color_code))
        self.animation_color.try_to_start()

    def setColor(self, color_code):
        """
        设置颜色
        :param color_code: 色号
        :return:
        """
        color_value = Color.decodeColor(color_code)
        self.animation_color.setCurrent(color_value)
        self._set_color_handler(color_value)

    def _set_color_handler(self, color_value):
        self.setStyleSheet(f"background-color: {Color.encodeColor(color_value)}")


class SiPixLabel(SiLabel):
    """
    为显示图片提供支持的标签，支持图片的圆角处理
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parent =  parent

        self.border_radius = 32
        self.blur_radius = 0
        self.path = None

    def setBorderRadius(self, r: int):
        """
        设置图片圆角半径
        :param r: 圆角半径
        :return:
        """
        self.border_radius = r

    def load(self, path: str):
        """
        加载图片
        :param path: 图片路径
        :return:
        """
        self.path = path
        self.draw()

    def draw(self):
        """
        绘制图像，只有在调用 load 方法后才有效
        :return:
        """
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
        path.addRoundedRect(0,                  0,
                            self.width(),       self.height(),
                            self.border_radius, self.border_radius)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, p)
        self.setPixmap(self.target)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.draw()


class SiDraggableLabel(SiLabel):
    """
    为拖动事件提供支持的标签
    """
    dragged = pyqtSignal(object)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setMouseTracking(True)
        self.anchor = QPoint(0, 0)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.anchor = event.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if not (event.buttons() & Qt.LeftButton):
            return
        newpos = event.pos() - self.anchor + self.frameGeometry().topLeft()
        x, y = self._legalizeMovingTarget(newpos.x(), newpos.y())
        self.moveTo(x, y)
        self.dragged.emit([x, y])

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
