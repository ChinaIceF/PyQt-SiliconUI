from __future__ import annotations

import math
import random
from dataclasses import dataclass
from functools import lru_cache

import numpy
from PyQt5 import Qt
from PyQt5.QtCore import QEvent, QPointF, QRect, QRectF
from PyQt5.QtGui import QColor, QPainter, QPainterPath
from PyQt5.QtWidgets import QLabel, QWidget

from siui.core import SiColor, SiGlobal, createPainter
from siui.core.painter import getSuperRoundedRectPath


@dataclass
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
        painter.setBrush(QColor("#a681bf"))
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
