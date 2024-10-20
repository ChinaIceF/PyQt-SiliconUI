from PyQt5.QtCore import QPoint, Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPainterPath, QPixmap
from PyQt5.QtSvg import QSvgWidget

from siui.components.widgets.abstracts.label import ABCAnimatedLabel
from siui.core import GlobalFont, Si, SiColor, SiQuickAlignmentManager
from siui.gui import SiFont


class SiLabel(ABCAnimatedLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().setFont(SiFont.tokenized(GlobalFont.S_NORMAL))


class SiFlashLabel(SiLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.flash_color = self.getColor(SiColor.BUTTON_FLASH)
        self.flash_layer = SiLabel(self)
        self.flash_layer.animationGroup().fromToken("color").setFactor(1/16)

    def setFlashColor(self, code):
        self.flash_color = code

    def flash(self):
        self.flash_layer.setColor(SiColor.trans(self.flash_color, 1.0))
        self.flash_layer.setColorTo(SiColor.trans(self.flash_color, 0))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.flash_layer.resize(event.size())


class SiPixLabel(SiLabel):
    def __init__(self, parent):
        super().__init__(parent)

        self.border_radius = 32
        self.blur_radius = 0
        self.path_ = None
        self.offset = QPoint(0, 0)

    def setOffset(self, x: int, y: int):
        self.offset.setX(x)
        self.offset.setY(y)

    def setBorderRadius(self, r: int):
        """ set the border radius of the shown image """
        self.border_radius = r

    def path(self):
        return self.path_

    def load(self, path: str):
        """ load the image, `draw()` will be Implicitly called. """
        self.path_ = path
        self.draw()

    def draw(self):
        """ Draw the image，you can only call it after run `load(path)` """
        if self.path_ is None:
            return

        w, h = self.width(), self.height()

        target = QPixmap(self.size())
        target.fill(Qt.transparent)

        p = QPixmap(self.path_).scaled(w, h, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        painter = QPainter(target)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        path = QPainterPath()
        path.addRoundedRect(0,                  0,
                            self.width(),       self.height(),
                            self.border_radius, self.border_radius)

        painter.setClipPath(path)
        pos = SiQuickAlignmentManager.toPos(self.size(), p.size(), self.alignment())
        painter.drawPixmap(pos.x() + self.offset.x(), pos.y() + self.offset.y(), p)
        painter.end()

        self.setPixmap(target)

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
        self.setSvgSize(20, 20)
        self.resize(24, 24)

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
        self.icon_ = SiSvgLabel(self)
        self.icon_.resize(24, 24)
        self.icon_.setSvgSize(20, 20)

        # 创建文本标签
        self.text_label = SiLabel(self)
        self.text_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.text_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.text_label.setFixedHeight(20)  # 固定高度

    def setStyleSheet(self, stylesheet: str):
        self.text_label.setStyleSheet(stylesheet)

    def setFixedStyleSheet(self, fixed_stylesheet: str):
        self.text_label.setStyleSheet(fixed_stylesheet)

    def icon(self):
        return self.icon_

    def label(self):
        return self.text_label

    def load(self, path_or_data):
        """
        从字符串或者文件加载 svg 数据
        :param path_or_data: 文件路径或是 svg 字符串
        :return:
        """
        self.has_icon_flag = True
        self.icon_.load(path_or_data)
        self.adjustSize()    # 保证布局正常

    def setSvgSize(self, w, h):
        """
        设置 svg 图标的大小
        :param w: 宽度
        :param h: 高度
        """
        self.icon_.resize(w, h)  # 这里直接设为一样，避免边缘切割
        self.icon_.setSvgSize(w, h)
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
                           int(self.has_icon_flag) * self.icon_.width())

        preferred_height = max(int(self.has_text_flag) * self.text_label.height(),
                               int(self.has_icon_flag) * self.icon_.height())

        self.resize(preferred_width, preferred_height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.icon_.move(0, (h - self.icon_.height()) // 2)
        self.text_label.move(w - self.text_label.width(), (h - self.text_label.height()) // 2 - 1)  # 减一调整显示位置归正


class SiDraggableLabel(SiLabel):
    """
    为拖动事件提供支持的标签
    """
    dragged = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.anchor = QPoint(0, 0)

        self.track = True  # 是否跟随鼠标

    def setTrack(self, b: bool):
        """
        设置是否每次鼠标移动时调用 moveTo 移动到鼠标位置
        :param b: 是否跟踪
        :return:
        """
        self.track = b

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.anchor = event.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if not (event.buttons() & Qt.LeftButton):
            return
        new_pos = event.pos() - self.anchor + self.frameGeometry().topLeft()
        x, y = self._legalize_moving_target(new_pos.x(), new_pos.y())
        self.dragged.emit([x, y])

        if self.track is True:
            self.moveTo(x, y)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
