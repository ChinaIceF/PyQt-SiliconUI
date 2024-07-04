from PyQt5.QtCore import QPoint, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPainterPath, QPixmap
from PyQt5.QtSvg import QSvgWidget

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


class SiSvgLabel(SiLabel):
    """
    可以显示 Svg 图像的 SiLabel 标签
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 创建 QSvgWidget
        self.svg_widget = QSvgWidget(self)

    def load(self, path_or_data):
        """
        从字符串或者文件加载 svg 数据
        :param path_or_data: 文件路径或是 svg 字符串
        :return:
        """
        self.svg_widget.load(path_or_data)

    def setSvgSize(self, w, h):
        """
        设置 svg 图标的大小
        :param w: 宽度
        :param h: 高度
        """
        self.svg_widget.setFixedSize(w, h)
        self.resize(self.size())    # 保证居中

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        # 保证居中显示
        self.svg_widget.move((w - self.svg_widget.width()) // 2, (h - self.svg_widget.height()) // 2)


class SiIconLabel(SiLabel):
    """
    具图标的标签，即一个图标紧跟一段文字的标签，使用一个 SiSvgLabel 和 SiLabel 组合
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.has_icon_flag = False  # 加载图标后为真
        self.has_text_flag = False  # 设置文本后为真

        # 创建图标标签
        self.icon = SiSvgLabel(self)
        self.icon.resize(16, 16)
        self.icon.setSvgSize(16, 16)

        # 创建文本标签
        self.text_label = SiLabel(self)
        self.text_label.setAutoAdjustSize(True)
        self.text_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

    def setStyleSheet(self, stylesheet: str):
        self.text_label.setStyleSheet(stylesheet)

    def setFixedStyleSheet(self, fixed_stylesheet: str):
        self.text_label.setStyleSheet(fixed_stylesheet)

    def load(self, path_or_data):
        """
        从字符串或者文件加载 svg 数据
        :param path_or_data: 文件路径或是 svg 字符串
        :return:
        """
        self.has_icon_flag = True
        self.icon.load(path_or_data)
        self.adjustSize()    # 保证布局正常

    def setSvgSize(self, w, h):
        """
        设置 svg 图标的大小
        :param w: 宽度
        :param h: 高度
        """
        self.icon.resize(w, h)  # 这里直接设为一样，避免边缘切割
        self.icon.setSvgSize(w, h)
        self.adjustSize()    # 保证布局正常

    def setFont(self, a0):
        self.text_label.setFont(a0)

    def setText(self, text: str):
        self.has_text_flag = True
        self.text_label.setText(text)
        self.adjustSize()    # 保证布局正常

    def text(self):
        return self.text_label.text()

    def adjustSize(self):


        preferred_width = (int(self.has_text_flag) * self.text_label.width() +
                           int(self.has_text_flag and self.has_icon_flag) * 4 +
                           int(self.has_icon_flag) * self.icon.width())

        preferred_height = max(int(self.has_text_flag) * self.text_label.height(),
                               int(self.has_icon_flag) * self.icon.height())

        self.resize(preferred_width, preferred_height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()
        self.icon.move(0, (h - self.icon.height()) // 2)
        self.text_label.move(w - self.text_label.width(), (h - self.text_label.height()) // 2)



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
