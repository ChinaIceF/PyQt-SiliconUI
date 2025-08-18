from __future__ import annotations

import math
import warnings

import numpy
from PyQt5.QtCore import QEvent, QPointF, QRect, QRectF, QSize, Qt, pyqtProperty
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QPaintEvent, QPixmap
from PyQt5.QtWidgets import QLabel, QWidget

from siui.core import SiColor, SiGlobal, createPainter
from siui.core.animation import SiExpAnimationRefactor
from siui.core.painter import getSuperRoundedRectPath
from siui.typing import T_WidgetParent


# @dataclass
class SiLabelStyleData:
    text_color = SiColor.toArray("#00FFFFFF")
    background_color = SiColor.toArray("#00FFFFFF")
    border_bottom_left_radius: int = 4
    border_bottom_right_radius: int = 4
    border_top_left_radius: int = 4
    border_top_right_radius: int = 4


class SiLabelRefactor(QLabel):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.style_data = SiLabelStyleData()

    @property
    def textColor(self) -> numpy.ndarray:
        return self.style_data.text_color

    def backgroundColor(self) -> numpy.ndarray:
        return self.style_data.background_color

    def borderRadius(self) -> tuple:
        return (self.style_data.border_bottom_left_radius, self.style_data.border_bottom_right_radius,
                self.style_data.border_top_left_radius, self.style_data.border_top_right_radius)

    def setTextColor(self, code: str | tuple) -> None:
        self.style_data.text_color = SiColor.toArray(code)
        self.update()

    def setBackgroundColor(self, code: str | tuple) -> None:
        self.style_data.background_color = SiColor.toArray(code)
        self.update()

    def setBorderRadius(self, *radius: int):
        """
        set the border radius of this label.
        accepts 1 or 4 param(s).
        """
        if len(radius) == 1:
            self.style_data.border_bottom_left_radius = radius[0]
            self.style_data.border_bottom_right_radius = radius[0]
            self.style_data.border_top_left_radius = radius[0]
            self.style_data.border_top_right_radius = radius[0]
        elif len(radius) == 4:
            self.style_data.border_bottom_left_radius = radius[0]
            self.style_data.border_bottom_right_radius = radius[1]
            self.style_data.border_top_left_radius = radius[2]
            self.style_data.border_top_right_radius = radius[3]
        else:
            raise ValueError(f"setBorderRadius expects 1 or 4 param, but {len(radius)} are given.")
        self.update()

    def event(self, event):
        if event.type() == QEvent.ToolTip:
            return True  # 忽略工具提示事件
        return super().event(event)

    def _showToolTip(self) -> None:
        tool_tip_window = SiGlobal.siui.windows.get("TOOL_TIP")
        if tool_tip_window is not None and self.toolTip() != "":
            tool_tip_window.setNowInsideOf(self)
            tool_tip_window.show_()

    def _hideToolTip(self) -> None:
        tool_tip_window = SiGlobal.siui.windows.get("TOOL_TIP")
        if tool_tip_window is not None and self.toolTip() != "":
            tool_tip_window.setNowInsideOf(None)
            tool_tip_window.hide_()

    def _updateToolTip(self) -> None:
        tool_tip_window = SiGlobal.siui.windows.get("TOOL_TIP")
        if tool_tip_window is not None and tool_tip_window.nowInsideOf() == self:
            tool_tip_window.setText(self.toolTip())

    def setToolTip(self, tooltip) -> None:
        super().setToolTip(tooltip)
        self._updateToolTip()

    def enterEvent(self, event) -> None:
        super().enterEvent(event)
        self._showToolTip()
        self._updateToolTip()

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)
        self._hideToolTip()


class SiAnimatedColorWidget(QWidget):
    class Property:
        BackgroundColor = "backgroundColor"

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._background_color = QColor("#00000000")
        self._border_radius = 0.0

        self.color_ani = SiExpAnimationRefactor(self, self.Property.BackgroundColor)
        self.color_ani.init(1 / 8, 0.01, self._background_color, self._background_color)

    @pyqtProperty(QColor)
    def backgroundColor(self):
        return self._background_color

    @backgroundColor.setter
    def backgroundColor(self, value: QColor):
        self._background_color = value
        self.update()

    def borderRadius(self) -> float:
        return self._border_radius

    def setBorderRadius(self, value: float) -> None:
        self._border_radius = value
        self.update()

    def animation(self) -> SiExpAnimationRefactor:
        return self.color_ani

    def setAnimation(self, ani) -> None:
        self.color_ani.stop()
        self.color_ani.deleteLater()
        self.color_ani = ani

    def _drawBackgroundPath(self, rect: QRectF) -> QPainterPath:
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, rect.width(), rect.height()), self._border_radius, self._border_radius)
        return path

    def _drawBackgroundRect(self, painter: QPainter, rect: QRectF) -> None:
        painter.setBrush(self._background_color)
        painter.drawPath(self._drawBackgroundPath(rect))

    def paintEvent(self, event: QPaintEvent) -> None:
        rect = self.rect()
        renderHints = (
                QPainter.RenderHint.SmoothPixmapTransform
                | QPainter.RenderHint.TextAntialiasing
                | QPainter.RenderHint.Antialiasing
        )

        with createPainter(self, renderHints) as painter:
            self._drawBackgroundRect(painter, rect)


class SiRoundPixmapWidget(QWidget):
    def __init__(self, parent, pixmap: QPixmap | None = None):
        super().__init__(parent)
        self._pixmap = pixmap
        self._visual_size = QSize(32, 32)
        self._visual_size_enabled = False
        self._border_radius = 0.0

    def setPixmap(self, pixmap: QPixmap) -> None:
        self._pixmap = pixmap
        self.update()

    def setVisualSize(self, size: QSize) -> None:
        self._visual_size = size
        self.update()

    def setVisualSizeEnabled(self, state: bool) -> None:
        self._visual_size_enabled = state
        self.update()

    def setBorderRadius(self, radius: float) -> None:
        self._border_radius = radius
        self.update()

    def pixmap(self) -> QPixmap:
        return self._pixmap

    def visualSize(self) -> QSize:
        return self._visual_size

    def isVisualSizeEnabled(self) -> bool:
        return self._visual_size_enabled

    def borderRadius(self) -> float:
        return self._border_radius

    def _drawPixmap(self, painter: QPainter, rect: QRect) -> None:
        if self._pixmap is None:
            return

        device_pixel_ratio = self.devicePixelRatioF()
        border_radius = self._border_radius

        if self._visual_size_enabled:
            width = self._visual_size.width()
            height = self._visual_size.height()

        else:
            width = rect.width()
            height = rect.height()

        x = (rect.width() - width) // 2
        y = (rect.height() - height) // 2
        target_rect = QRect(x, y, width, height)
        size = QSize(width, height) * device_pixel_ratio

        pixmap = self._pixmap.scaled(size, transformMode=Qt.TransformationMode.SmoothTransformation)

        path = QPainterPath()
        path.addRoundedRect(x, y, width, height, border_radius, border_radius)
        painter.setClipPath(path)
        painter.drawPixmap(target_rect, pixmap)

    def paintEvent(self, event) -> None:
        rect = self.rect()
        device_pixel_ratio = self.devicePixelRatioF()

        buffer = QPixmap(rect.size() * device_pixel_ratio)
        buffer.setDevicePixelRatio(device_pixel_ratio)
        buffer.fill(Qt.transparent)

        renderHints = (
                QPainter.RenderHint.SmoothPixmapTransform
                | QPainter.RenderHint.TextAntialiasing
                | QPainter.RenderHint.Antialiasing
        )

        with createPainter(buffer, renderHints) as buffer_painter:
            self._drawPixmap(buffer_painter, rect)

        with createPainter(self, renderHints) as painter:
            painter.drawPixmap(rect, buffer)


# class SiPainterPath(QPainterPath):
#     class Quality:
#         Low = 16
#         Medium = 24
#         Normal = 32
#         High = 48
#         VeryHigh = 64
#         Extreme = 128
#         Auto = -1
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#     def addSuperRoundedRect(self, rect: QRectF,
#                             radius_x: float,
#                             radius_y: float,
#                             power: int = 5,
#                             quality: int = Quality.Normal) -> None:
#
#         if quality == self.Quality.Auto:
#             quality = max(radius_x, radius_y) // 4 * 4
#
#         points = _getSuperRoundedPoints(radius_x, radius_y, power, quality)
#         inner_rect = QRectF(rect.x() + radius_x, rect.y() + radius_y,
#                             rect.width() - 2 * radius_x, rect.height() - 2 * radius_y)
#
#         q = quality
#
#         self.moveTo(points[q // 4 * 0] + inner_rect.bottomRight())
#         delta = inner_rect.bottomRight()
#         for i in range(q // 4 * 0, q // 4 * 1 + 1):
#             mid_point = (points[i] + points[i + 1]) / 2 + delta
#             point = points[i] + delta
#             self.quadTo(point, mid_point)
#
#         delta = inner_rect.topRight()
#         for i in range(q // 4 * 1, q // 4 * 2 + 1):
#             mid_point = (points[i] + points[i + 1]) / 2 + delta
#             point = points[i] + delta
#             self.quadTo(point, mid_point)
#
#         delta = inner_rect.topLeft()
#         for i in range(q // 4 * 2, q // 4 * 3 + 1):
#             mid_point = (points[i] + points[i + 1]) / 2 + delta
#             point = points[i] + delta
#             self.quadTo(point, mid_point)
#
#         delta = inner_rect.bottomLeft()
#         for i in range(q // 4 * 3, q // 4 * 4):
#             mid_point = (points[i] + points[i + 1]) / 2 + delta
#             point = points[i] + delta
#             self.quadTo(point, mid_point)
#
#         self.lineTo(points[-1] + inner_rect.bottomLeft())  # 连接到最后一个点


class HyperRoundBorderTest(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.quality = 48
        self.points = []

    def sinSuper(self, x: float) -> float:
        return math.copysign(abs(math.sin(x)) ** (2 / 5), math.sin(x))

    def cosSuper(self, x: float) -> float:
        return math.copysign(abs(math.cos(x)) ** (2 / 5), math.cos(x))

    def _drawPath(self, rect: QRect) -> QPainterPath:
        # path = QPainterPath()
        # # path.addRoundedRect()
        # if self.points:
        #     path.moveTo(self.points[0])  # 将路径移动到第一个点
        #
        #     # 使用样条曲线平滑连接所有点
        #     for i in range(1, len(self.points) - 1):
        #         mid_point = (self.points[i] + self.points[i + 1]) / 2
        #         path.quadTo(self.points[i], mid_point)
        #     path.lineTo(self.points[-1])  # 连接到最后一个点
        # return path
        # path = SiPainterPath()
        # path.addSuperRoundedRect(rect, 24, 24, quality=SiPainterPath.Quality.Auto)
        return getSuperRoundedRectPath(rect, 24, 24)

    def _drawTest(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(QColor("#D087DF"))
        painter.drawPath(self._drawPath(rect))

    def paintEvent(self, a0):
        rect = self.rect()

        renderHints = (
                QPainter.RenderHint.SmoothPixmapTransform
                | QPainter.RenderHint.TextAntialiasing
                | QPainter.RenderHint.Antialiasing
        )

        with createPainter(self, renderHints) as painter:
            self._drawTest(painter, rect)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.points = []
        q = self.quality
        for i in range(q // 4 * 1, q // 4 * 2):
            self.points.append(QPointF((self.sinSuper(2 * math.pi * i / q) + 1) * self.width() / 2,
                                       (self.cosSuper(2 * math.pi * i / q) + 1) * self.height() / 2))


class LinearIndicatorStyleData:
    hl_color_inactive = QColor("#00D087DF")
    hl_color_flash = QColor("#F5EBF9")
    hl_color_active = QColor("#D087DF")
    hl_color_warn_flash = QColor("#ed716c")
    track_color = QColor("#4d4753")


class SiLinearIndicator(QWidget):
    class Property:
        Color = "color"
        VisualWidth = "visualWidth"
        VisualHeight = "visualHeight"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.style_data = LinearIndicatorStyleData()
        self._visual_width = 0
        self._visual_height = 0
        self._border_radius = 4.0
        self._color = self.style_data.hl_color_inactive

        self.visual_width_ani = SiExpAnimationRefactor(self, self.Property.VisualWidth)
        self.visual_width_ani.init(1/4, 0.0001, self._visual_width, self._visual_width)

        self.visual_height_ani = SiExpAnimationRefactor(self, self.Property.VisualHeight)
        self.visual_height_ani.init(1/4, 0.0001, self._visual_height, self._visual_height)

        self.color_ani = SiExpAnimationRefactor(self, self.Property.Color)
        self.color_ani.init(1/8, 0.0001, self._color, self._color)

    @pyqtProperty(float)
    def visualWidth(self):
        return self._visual_width

    @visualWidth.setter
    def visualWidth(self, value: float):
        self._visual_width = value
        self.update()

    @pyqtProperty(float)
    def visualHeight(self):
        return self._visual_height

    @visualHeight.setter
    def visualHeight(self, value: float):
        self._visual_height = value
        self.update()

    @pyqtProperty(QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, value: QColor):
        self._color = value
        self.update()

    def setBorderRadius(self, value: float) -> None:
        self._border_radius = value
        self.update()

    def borderRadius(self) -> float:
        return self._border_radius

    def setVisualWidth(self, value: float, ani: bool = False) -> None:
        if ani:
            self.visual_width_ani.setEndValue(value)
            self.visual_width_ani.start()
        else:
            self.visual_width_ani.stop()
            self.visual_width_ani.setCurrentValue(value)
            self.visual_width_ani.toProperty()

    def setVisualHeight(self, value: float, ani: bool = False) -> None:
        if ani:
            self.visual_height_ani.setEndValue(value)
            self.visual_height_ani.start()
        else:
            self.visual_height_ani.stop()
            self.visual_height_ani.setCurrentValue(value)
            self.visual_height_ani.toProperty()

    def setColor(self, value: QColor, ani: bool = False):
        if ani:
            self.color_ani.setEndValue(value)
            self.color_ani.start()
        else:
            self.color_ani.stop()
            self.color_ani.setCurrentValue(value)
            self.color_ani.toProperty()

    def activate(self, flash=True) -> None:
        if flash:
            self.color_ani.setCurrentValue(self.style_data.hl_color_flash)
        self.color_ani.setEndValue(self.style_data.hl_color_active)
        self.color_ani.start()

    def deactivate(self) -> None:
        self.color_ani.setEndValue(self.style_data.hl_color_inactive)
        self.color_ani.start()

    def warn(self):
        self.color_ani.setCurrentValue(self.style_data.hl_color_warn_flash)
        self.color_ani.start()

    def colorAnimation(self) -> SiExpAnimationRefactor:
        return self.color_ani

    def visualWidthAnimation(self) -> SiExpAnimationRefactor:
        return self.visual_width_ani

    def visualHeightAnimation(self) -> SiExpAnimationRefactor:
        return self.visual_height_ani

    def _borderRadiusLegalized(self) -> float:
        min_shape = min(self.width(), self.height())
        legalized = min(self._border_radius, min_shape / 2)
        return legalized

    def _drawTrackRect(self, painter: QPainter, rect: QRectF) -> None:
        path = QPainterPath()
        path.addRoundedRect(rect, self._borderRadiusLegalized(), self._borderRadiusLegalized())

        painter.setPen(Qt.NoPen)
        painter.setBrush(self.style_data.track_color)
        painter.drawPath(path)

    def _drawIndicatorRect(self, painter: QPainter, rect: QRectF) -> None:
        path = QPainterPath()
        path.addRoundedRect(rect, self._borderRadiusLegalized(), self._borderRadiusLegalized())

        painter.setPen(Qt.NoPen)
        painter.setBrush(self._color)
        painter.drawPath(path)

    def paintEvent(self, a0):
        x = (self.width() - self._visual_width) / 2
        y = (self.height() - self._visual_height) / 2
        rect = QRectF(x, y, self._visual_width, self._visual_height)

        with createPainter(self) as painter:
            self._drawTrackRect(painter, rect)
            self._drawIndicatorRect(painter, rect)


class SiLinearPartitionIndicator(SiLinearIndicator):

    class Property:
        Color = "color"
        VisualWidth = "visualWidth"
        VisualHeight = "visualHeight"
        HighlightRect = "highlightRect"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self._orientation = Qt.Horizontal
        self._node_amount = 2
        self._indicator_start_index = 0
        self._indicator_end_index = 1
        self._hl_rect = QRectF()

        self.hl_rect_ani = SiExpAnimationRefactor(self, self.Property.HighlightRect)
        self.hl_rect_ani.init(1/4, 0.0001, self._hl_rect, self._hl_rect)

    @pyqtProperty(QRectF)
    def highlightRect(self):
        return self._hl_rect

    @highlightRect.setter
    def highlightRect(self, value: QRectF):
        self._hl_rect = value
        self.update()

    def setOrientation(self, ori: Qt.Orientation):
        if ori != Qt.Horizontal and ori != Qt.Vertical:
            raise ValueError(f"{ori} is not in Qt.Orientation.")

        self._orientation = ori
        self.update()

    def orientation(self) -> Qt.Orientation:
        return self._orientation

    def updateIndicatorRect(self) -> None:
        x = (self.width() - self._visual_width) / 2
        y = (self.height() - self._visual_height) / 2
        start_i = self._indicator_start_index
        end_i = self._indicator_end_index

        section_amount = self._node_amount - 1

        if section_amount == 0:
            rect = QRectF(x, y, self._visual_width, self._visual_height)
            self.hl_rect_ani.setEndValue(rect)
            self.hl_rect_ani.start()
            return

        if self._orientation == Qt.Horizontal:
            section_span = self._visual_width / section_amount
            rect = QRectF(x + start_i * section_span, y, (end_i - start_i) * section_span, self._visual_height)

        elif self._orientation == Qt.Vertical:
            section_span = self._visual_height / section_amount
            rect = QRectF(x, y + start_i * section_span, self._visual_width, (end_i - start_i) * section_span)

        else:
            raise ValueError(f"Unexpected orientation value: {self._orientation}")

        self.hl_rect_ani.setEndValue(rect)
        self.hl_rect_ani.start()

    def setStartIndex(self, index: int) -> None:
        if index >= self._node_amount or self._node_amount < 0:
            warnings.warn("Start index out of range. "
                          f"(expected {0} to {self._node_amount - 1}, but encountered {index}) "
                          "set to closest legal value instead")

            index = 0 if index < 0 else self._node_amount - 1

        self._indicator_start_index = index
        self.updateIndicatorRect()

    def setEndIndex(self, index: int) -> None:
        if index >= self._node_amount or self._node_amount < 0:
            warnings.warn("End index out of range. "
                          f"(expected {0} to {self._node_amount - 1}, but encountered {index}) "
                          "set to closest legal value instead")

            index = 0 if index < 0 else self._node_amount - 1

        self._indicator_end_index = index
        self.updateIndicatorRect()

    def setNodeAmount(self, a: int) -> None:
        if a <= 0:
            warnings.warn("Node amount must be a positive int value, set to 1 instead.")
            a = 1

        self._node_amount = a
        self.updateIndicatorRect()

    def startIndex(self) -> int:
        return self._indicator_start_index

    def endIndex(self) -> int:
        return self._indicator_end_index

    def nodeAmount(self) -> int:
        return self._node_amount

    def paintEvent(self, a0):
        x = (self.width() - self._visual_width) / 2
        y = (self.height() - self._visual_height) / 2
        track_rect = QRectF(x, y, self._visual_width, self._visual_height)
        indi_rect = self._hl_rect

        with createPainter(self) as painter:
            self._drawTrackRect(painter, track_rect)
            self._drawIndicatorRect(painter, indi_rect)
