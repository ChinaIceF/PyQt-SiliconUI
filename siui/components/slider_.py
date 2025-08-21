from __future__ import annotations

import math

from PyQt5.QtCore import QEvent, QPoint, QPointF, QRect, QRectF, QSize, Qt, QTimer, pyqtProperty, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QPainter, QPainterPath, QPen, QPixmap, QValidator
from PyQt5.QtWidgets import (
    QAbstractSlider,
    QAbstractSpinBox,
    QBoxLayout,
    QGraphicsScene,
    QGraphicsView,
    QLabel,
    QScrollArea,
    QScrollBar,
    QSpinBox,
    QWidget,
)

from siui.components.container import SiDenseContainer
from siui.components.graphic import SiAnimatedTransformGraphicProxyWidget
from siui.components.label import SiLinearIndicator
from siui.core import SiGlobal, createPainter
from siui.core.animation import SiExpAnimationRefactor
from siui.gui import SiFont
from siui.typing import T_WidgetParent


# @dataclass
class SliderStyleData:
    STYLE_TYPES = ["Slider"]

    thumb_idle_color: QColor = QColor("#D087DF")
    thumb_hover_color: QColor = QColor("#EDE1F4")
    thumb_width: int = 36
    thumb_height: int = 24

    track_color: QColor = QColor("#D087DF") #77568d
    track_height: int = 5

    background_color: QColor = QColor("#1C191F")


class SiSlider(QAbstractSlider):
    class Property:
        ThumbColor = "thumbColor"
        TrackProgress = "trackProgress"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.setMouseTracking(True)

        self.style_data = SliderStyleData()
        self._thumb_color = self.style_data.thumb_idle_color
        self._track_progress = 0
        self._is_dragging = False
        self._is_dragging_thumb = False
        self._dragging_start_pos = QPoint()
        self._dragging_anchor_pos = QPoint()
        self._value_to_tooltip_func = self._defaultValueToToolTip
        self._is_draw_track = True

        self.thumb_color_ani = SiExpAnimationRefactor(self, self.Property.ThumbColor)
        self.thumb_color_ani.init(1/4, 0.01, self._thumb_color, self._thumb_color)

        self.progress_ani = SiExpAnimationRefactor(self, self.Property.TrackProgress)
        self.progress_ani.init(1/3.5, 0.00001, 0, 0)

        self.valueChanged.connect(self._onValueChanged)
        self.rangeChanged.connect(self._onRangeChanged)

    @pyqtProperty(QColor)
    def thumbColor(self):
        return self._thumb_color

    @thumbColor.setter
    def thumbColor(self, value: QColor):
        self._thumb_color = value
        self.update()

    @pyqtProperty(float)
    def trackProgress(self):
        return self._track_progress

    @trackProgress.setter
    def trackProgress(self, value: float):
        self._track_progress = value
        self.update()

    def setDrawTrack(self, state: bool) -> None:
        self._is_draw_track = state
        self.update()

    def isDrawTrack(self) -> bool:
        return self._is_draw_track

    @staticmethod
    def _defaultValueToToolTip(value: int) -> str:
        return str(value)

    def setToolTipConvertionFunc(self, func) -> None:
        self._value_to_tooltip_func = func
        self.setToolTip(func(self.value()))

    def _onValueChanged(self, value):
        self.progress_ani.setEndValue((value - self.minimum()) / (self.maximum() - self.minimum()))
        self.progress_ani.start()
        self._updateToolTip(flash=False)

    def _onRangeChanged(self, _, __):
        p = (self.value() - self.minimum()) / (self.maximum() - self.minimum())
        self.setProperty(self.Property.TrackProgress, p)
        self.progress_ani.fromProperty()
        self.progress_ani.setCurrentValue(p)
        self.progress_ani.setEndValue(p)

    def _drawBackgroundPath(self, rect) -> QPainterPath:
        radius = min(rect.height() / 2, rect.width() / 2)
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        return path

    def _drawTrackPath(self, rect: QRect) -> QPainterPath:
        radius = min(rect.height() / 2, rect.width() / 2)
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        return path

    def _drawThumbPath(self, rect: QRect) -> QPainterPath:
        radius = min(rect.height() / 2, rect.width() / 2)
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        return path

    def _drawBackgroundRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(self.style_data.background_color)
        painter.drawPath(self._drawBackgroundPath(rect))

    def _drawTrackRect(self, painter: QPainter, rect: QRect) -> None:
        if self._is_draw_track:
            painter.setBrush(self.style_data.track_color)
            painter.drawPath(self._drawTrackPath(rect))

    def _drawThumbRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(self._thumb_color)
        painter.drawPath(self._drawThumbPath(rect))

    def _isMouseInThumbRect(self, pos: QPoint) -> bool:
        p = self._track_progress
        thumb_w = self.style_data.thumb_width
        thumb_h = self.style_data.thumb_height
        if self.orientation() == Qt.Orientation.Horizontal:
            thumb_rect = QRectF((self.width() - thumb_w) * p, (self.height() - thumb_h) / 2, thumb_w, thumb_h)
        else:
            thumb_rect = QRectF((self.width() - thumb_h) / 2, (self.height() - thumb_w) * (1 - p), thumb_h, thumb_w)
        return thumb_rect.contains(pos)

    def _setValueToMousePos(self, pos: QPoint) -> None:
        thumb_width = self.style_data.thumb_width
        region = self.maximum() - self.minimum()
        if self.orientation() == Qt.Orientation.Horizontal:
            p = min(1, max((pos.x() - thumb_width / 2) / (self.width() - thumb_width), 0))
        else:
            p = min(1, max(1 - (pos.y() - thumb_width / 2) / (self.height() - thumb_width), 0))
        self.setValue(int(self.minimum() + region * p))

    def _setThumbHovering(self, state: bool) -> None:
        if state:
            self.thumb_color_ani.setEndValue(self.style_data.thumb_hover_color)
            self.thumb_color_ani.start()
        else:
            self.thumb_color_ani.setEndValue(self.style_data.thumb_idle_color)
            self.thumb_color_ani.start()

    def _updateDraggingAnchor(self):
        p = (self.value() - self.minimum()) / (self.maximum() - self.minimum())
        thumb_w = self.style_data.thumb_width
        thumb_h = self.style_data.thumb_height
        if self.orientation() == Qt.Orientation.Horizontal:
            thumb_rect = QRectF((self.width() - thumb_w) * p, (self.height() - thumb_h) / 2, thumb_w, thumb_h)
        else:
            thumb_rect = QRectF((self.width() - thumb_h) / 2, (self.height() - thumb_w) * (1 - p), thumb_h, thumb_w)
        self._dragging_anchor_pos = thumb_rect.center()

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

    def _updateToolTip(self, flash: bool = True) -> None:
        self.setToolTip(self._value_to_tooltip_func(self.value()))
        tool_tip_window = SiGlobal.siui.windows.get("TOOL_TIP")
        if tool_tip_window is not None and tool_tip_window.nowInsideOf() == self:
            tool_tip_window.setText(self.toolTip(), flash=flash)

    def sizeHint(self) -> QSize:
        return QSize(max(self.size().width(), 64), max(self.size().height(), 32))

    def event(self, event):
        if event.type() == QEvent.ToolTip:
            return True  # 忽略工具提示事件
        return super().event(event)

    def enterEvent(self, a0):
        super().enterEvent(a0)
        self._showToolTip()
        self._updateToolTip()

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        self._hideToolTip()

    def mousePressEvent(self, a0):
        super().mousePressEvent(a0)
        self.sliderPressed.emit()
        self._setThumbHovering(True)  # force to change the outfit of thumb
        self._is_dragging = True
        if self._isMouseInThumbRect(a0.pos()):
            self._is_dragging_thumb = True
            self._updateDraggingAnchor()
            self._dragging_start_pos = a0.pos()
        else:
            self._setValueToMousePos(a0.pos())

    def mouseMoveEvent(self, a0):
        super().mouseMoveEvent(a0)
        if self._is_dragging:
            if self._is_dragging_thumb:
                pos = self._dragging_anchor_pos + (a0.pos() - self._dragging_start_pos)
                self._setValueToMousePos(pos)
            else:
                self._setValueToMousePos(a0.pos())

        else:
            self._setThumbHovering(state=self._isMouseInThumbRect(a0.pos()))

    def mouseReleaseEvent(self, a0):
        super().mouseReleaseEvent(a0)
        self.sliderReleased.emit()

        self._setThumbHovering(False)
        self._is_dragging_thumb = False
        self._is_dragging = False

    def paintEvent(self, event):
        p = self._track_progress
        thumb_w = self.style_data.thumb_width
        thumb_h = self.style_data.thumb_height
        track_w = self.style_data.track_height
        track_h = self.style_data.track_height

        if self.orientation() == Qt.Orientation.Horizontal:
            background_rect = QRectF(0, (self.height() - track_h) / 2, self.width(), track_h)
            track_rect = QRectF(0, (self.height() - track_h) / 2, thumb_w / 2 + (self.width() - thumb_w) * p, track_h)
            thumb_rect = QRectF((self.width() - thumb_w) * p, (self.height() - thumb_h) / 2, thumb_w, thumb_h)
        else:
            background_rect = QRectF((self.width() - track_w) / 2, 0, track_w, self.height())
            track_rect = QRectF((self.width() - track_w) / 2, self.height() * (1-p), track_w, self.height() * p)
            thumb_rect = QRectF((self.width() - thumb_h) / 2, (self.height() - thumb_w) * (1-p), thumb_h, thumb_w)

        renderHints = (
                QPainter.RenderHint.SmoothPixmapTransform
                | QPainter.RenderHint.TextAntialiasing
                | QPainter.RenderHint.Antialiasing
        )

        with createPainter(self, renderHints) as painter:
            self._drawBackgroundRect(painter, background_rect)
            self._drawTrackRect(painter, track_rect)
            self._drawThumbRect(painter, thumb_rect)


# @dataclass
class CoordinatePickerStyleData:
    STYLE_TYPES = ["Slider"]

    slider_x_height: int = 64
    slider_y_width: int = 64

    indicator_size: int = 26
    indicator_idle_color: QColor = QColor("#D087DF")
    indicator_hover_color: QColor = QColor("#EDE1F4")
    indicator_outline_weight: int = 10
    indicator_stroke_weight: int = 6
    indicator_background_color: QColor = QColor("#25222a")
    indicator_stroke_color: QColor = QColor("#D087DF")

    base_line_weight: int = 2
    base_line_color: QColor = QColor("#3b3143")

    xoy_plate_background_color: QColor = QColor("#571c191f")
    deepest_background_color: QColor = QColor("#1c191f")

    background_color: QColor = QColor("#25222a")
    background_border_radius: int = 6


class SiCoordinatePicker2D(QWidget):
    class Property:
        ProgressX = "progressX"
        ProgressY = "progressY"
        IndicatorRect = "indicatorRect"
        ThumbColor = "thumbColor"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.setMouseTracking(True)

        self.style_data = CoordinatePickerStyleData()
        self._dragging_anchor_pos = QPoint()
        self._dragging_start_pos = QPoint()
        self._is_dragging_thumb = False
        self._is_dragging = False
        self._value_to_tooltip_func = self._defaultValueToToolTip

        self._progress_x = 0
        self._progress_y = 0
        self._thumb_color = self.style_data.indicator_idle_color
        self._indicator_rect = QRectF()

        self.slider_x = SiSlider(self)
        self.slider_y = SiSlider(self)

        self.thumb_color_ani = SiExpAnimationRefactor(self, self.Property.ThumbColor)
        self.thumb_color_ani.init(1/4, 0.01, self._thumb_color, self._thumb_color)

        self.progress_x_ani = SiExpAnimationRefactor(self, self.Property.ProgressX)
        self.progress_x_ani.init(1/3.5, 0.00001, 0, 0)

        self.progress_y_ani = SiExpAnimationRefactor(self, self.Property.ProgressY)
        self.progress_y_ani.init(1/3.5, 0.00001, 0, 0)

        self._initStyle()

        self.slider_x.valueChanged.connect(self._onSliderXValueChanged)
        self.slider_y.valueChanged.connect(self._onSliderYValueChanged)

    def _initStyle(self) -> None:
        self.slider_x.setOrientation(Qt.Orientation.Horizontal)
        self.slider_x.setFixedHeight(self.style_data.slider_x_height)
        self.slider_y.setFixedWidth(self.style_data.slider_y_width)
        self.slider_y.setOrientation(Qt.Orientation.Vertical)
        self.slider_x.setDrawTrack(False)
        self.slider_y.setDrawTrack(False)
        self.slider_x.leaveEvent = self.enterEvent
        self.slider_y.leaveEvent = self.enterEvent

        # self.slider_x.style_data.thumb_idle_color = QColor("#b9e2e6")
        # self.slider_x.style_data.track_color = QColor("#83b4b9")
        #
        # self.slider_y.style_data.thumb_idle_color = QColor("#eaa9c4")
        # self.slider_y.style_data.track_color = QColor("#b96f98")

    @pyqtProperty(QColor)
    def thumbColor(self):
        return self._thumb_color

    @thumbColor.setter
    def thumbColor(self, value: QColor):
        self._thumb_color = value
        self.update()

    @pyqtProperty(float)
    def progressX(self):
        return self._progress_x

    @progressX.setter
    def progressX(self, value: float):
        self._progress_x = value
        self.update()

    @pyqtProperty(float)
    def progressY(self):
        return self._progress_y

    @progressY.setter
    def progressY(self, value: float):
        self._progress_y = value
        self.update()

    @pyqtProperty(QRectF)
    def indicatorRect(self):
        return self._indicator_rect

    @indicatorRect.setter
    def indicatorRect(self, value: QRectF):
        self._indicator_rect = value

    @staticmethod
    def _defaultValueToToolTip(*args):
        return f"x = {args[0]}\ny = {args[1]}"

    def setToolTipConvertionFunc(self, func) -> None:
        self._value_to_tooltip_func = func
        self.setToolTip(func(self.value()))

    def _isMouseInThumbRect(self, pos: QPoint) -> bool:
        rect: QRect = self.property(self.Property.IndicatorRect)
        return rect.contains(pos)

    def _isMousePosValid(self, pos: QPoint) -> bool:
        slider_x_height = self.style_data.slider_y_width
        slider_y_width = self.style_data.slider_x_height
        background_rect = QRectF(slider_y_width, 0, self.width() - slider_y_width, self.height() - slider_x_height)
        return background_rect.contains(pos)

    def _setThumbHovering(self, state: bool) -> None:
        if state:
            self.thumb_color_ani.setEndValue(self.style_data.indicator_hover_color)
            self.thumb_color_ani.start()
        else:
            self.thumb_color_ani.setEndValue(self.style_data.indicator_idle_color)
            self.thumb_color_ani.start()

    def _updateDraggingAnchor(self) -> None:
        indicator_outline_rect = self.property(self.Property.IndicatorRect)
        self._dragging_anchor_pos = indicator_outline_rect.center()

    def _setValueToMousePos(self, pos: QPoint) -> None:
        margin = self.slider_x.style_data.thumb_width / 2
        slider_y_width = self.style_data.slider_y_width
        slider_x_height = self.style_data.slider_x_height
        progress_x = (pos.x() - slider_y_width - margin) / (self.width() - slider_y_width - margin * 2)
        progress_y = 1 - (pos.y() - margin) / (self.height() - margin * 2 - slider_x_height)

        self.slider_x.setValue(int(self.slider_x.minimum() +
                                   (self.slider_x.maximum() - self.slider_x.minimum()) * progress_x))
        self.slider_y.setValue(int(self.slider_y.minimum() +
                                   (self.slider_y.maximum() - self.slider_y.minimum()) * progress_y))

    def _onSliderXValueChanged(self, _) -> None:
        self.progress_x_ani.setEndValue(self._progressSliderX())
        self.progress_x_ani.start()
        self._updateToolTip(flash=False)

    def _onSliderYValueChanged(self, _) -> None:
        self.progress_y_ani.setEndValue(self._progressSliderY())
        self.progress_y_ani.start()
        self._updateToolTip(flash=False)

    def _progressSliderX(self) -> float:
        return (self.slider_x.value() - self.slider_x.minimum()) / (self.slider_x.maximum() - self.slider_x.minimum())

    def _progressSliderY(self) -> float:
        return (self.slider_y.value() - self.slider_y.minimum()) / (self.slider_y.maximum() - self.slider_y.minimum())

    def _drawBackgroundPath(self, rect: QRect) -> QPainterPath:
        radius = self.style_data.background_border_radius
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        return path

    def _drawIndicatorPath(self, rect: QRect) -> QPainterPath:
        indicator_size = self.style_data.indicator_size
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), indicator_size / 2, indicator_size / 2)
        return path

    def _drawBackgroundRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(self.style_data.background_color)
        painter.drawPath(self._drawBackgroundPath(rect))

    def _drawIndicatorRect(self, painter: QPainter, rect: QRect) -> None:  # the rect should be the rect of background.
        margin = self.slider_x.style_data.thumb_width / 2
        indicator_size = self.style_data.indicator_size - self.style_data.indicator_stroke_weight
        available_w = rect.width() - margin * 2
        available_h = rect.height() - margin * 2

        x = margin + available_w * self._progress_x - indicator_size / 2 + self.style_data.slider_y_width
        y = margin + available_h * (1 - self._progress_y) - indicator_size / 2
        d = self.style_data.indicator_outline_weight
        indicator_rect = QRectF(x, y, indicator_size, indicator_size)
        indicator_outline_rect = QRectF(x - d, y - d, indicator_size + d * 2, indicator_size + d * 2)
        self.setProperty(self.Property.IndicatorRect, indicator_outline_rect)

        painter.setBrush(self.style_data.background_color)
        painter.drawPath(self._drawIndicatorPath(indicator_outline_rect))

        painter.setBrush(self.style_data.indicator_background_color)
        painter.setPen(QPen(self._thumb_color, self.style_data.indicator_stroke_weight))
        painter.drawPath(self._drawIndicatorPath(indicator_rect))
        painter.setPen(Qt.NoPen)

    def _drawBaseLine(self, painter: QPainter, rect: QRect) -> None:  # the rect should be the rect of background.
        margin = self.slider_x.style_data.thumb_width / 2
        available_w = rect.width() - margin * 2
        available_h = rect.height() - margin * 2

        x = margin + available_w * self._progress_x + self.style_data.slider_y_width
        y = margin + available_h * (1 - self._progress_y)
        d = 12

        painter.setPen(QPen(self.style_data.base_line_color, self.style_data.base_line_weight))
        painter.drawLine(QPointF(x, margin - d), QPointF(x, margin + d + available_h))
        painter.drawLine(QPointF(margin + rect.x() - d, y), QPointF(margin + available_w + rect.x() + d, y))
        painter.setPen(Qt.NoPen)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.slider_y.setGeometry(0, 0, self.slider_y.width(), self.height() - self.slider_x.height())
        self.slider_x.setGeometry(self.slider_y.width(), self.height() - self.slider_x.height(),
                                  self.width() - self.slider_y.width(), self.slider_x.height())

    def mousePressEvent(self, a0):
        super().mousePressEvent(a0)
        if self._isMousePosValid(a0.pos()):
            self._setThumbHovering(True)  # force to change the outfit of thumb
            self._is_dragging = True
            if self._isMouseInThumbRect(a0.pos()):
                self._is_dragging_thumb = True
                self._updateDraggingAnchor()
                self._dragging_start_pos = a0.pos()
            else:
                self._setValueToMousePos(a0.pos())

    def mouseMoveEvent(self, a0):
        super().mouseMoveEvent(a0)
        if self._is_dragging:
            if self._is_dragging_thumb:
                pos = self._dragging_anchor_pos + (a0.pos() - self._dragging_start_pos)
                self._setValueToMousePos(pos)
            else:
                self._setValueToMousePos(a0.pos())

        else:
            self._setThumbHovering(state=self._isMouseInThumbRect(a0.pos()))

    def mouseReleaseEvent(self, a0):
        super().mouseReleaseEvent(a0)

        self._setThumbHovering(False)
        self._is_dragging_thumb = False
        self._is_dragging = False

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

    def _updateToolTip(self, flash: bool = True) -> None:
        self.setToolTip(self._value_to_tooltip_func(self.slider_x.value(), self.slider_y.value()))
        tool_tip_window = SiGlobal.siui.windows.get("TOOL_TIP")
        if tool_tip_window is not None and tool_tip_window.nowInsideOf() == self:
            tool_tip_window.setText(self.toolTip(), flash=flash)

    def event(self, event):
        if event.type() == QEvent.ToolTip:
            return True  # 忽略工具提示事件
        return super().event(event)

    def enterEvent(self, a0):
        super().enterEvent(a0)
        self._showToolTip()
        self._updateToolTip()

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        self._hideToolTip()

    def paintEvent(self, a0):
        slider_x_height = self.style_data.slider_y_width
        slider_y_width = self.style_data.slider_x_height
        background_rect = QRectF(slider_y_width, 0, self.width() - slider_y_width, self.height() - slider_x_height)

        renderHints = (
                QPainter.RenderHint.SmoothPixmapTransform
                | QPainter.RenderHint.TextAntialiasing
                | QPainter.RenderHint.Antialiasing
        )

        with createPainter(self, renderHints) as painter:
            self._drawBackgroundRect(painter, background_rect)
            self._drawBaseLine(painter, background_rect)
            self._drawIndicatorRect(painter, background_rect)


class SiCoordinatePicker3D(SiCoordinatePicker2D):
    class Property:
        ProgressX = "progressX"
        ProgressY = "progressY"
        ProgressZ = "progressZ"
        IndicatorRect = "indicatorRect"
        ThumbColor = "thumbColor"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)
        self._value_to_tooltip_func = lambda *args: f"x = {args[0]}\ny = {args[1]}\nz = {args[2]}"
        self._progress_z = 0
        self._min_scale_factor = 0.75

        self.slider_z = SiSlider(self)
        self.slider_z.setVisible(False)

        self.progress_z_ani = SiExpAnimationRefactor(self, self.Property.ProgressZ)
        self.progress_z_ani.init(1/4, 0.00001, 0, 0)

        self.slider_z.valueChanged.connect(self._onSliderZValueChanged)

    @pyqtProperty(float)
    def progressZ(self):
        return self._progress_z

    @progressZ.setter
    def progressZ(self, value: float):
        self._progress_z = value
        self.update()

    def _updateToolTip(self, flash: bool = True) -> None:
        self.setToolTip(
            self._value_to_tooltip_func(self.slider_x.value(), self.slider_y.value(), self.slider_z.value()))

        tool_tip_window = SiGlobal.siui.windows.get("TOOL_TIP")
        if tool_tip_window is not None and tool_tip_window.nowInsideOf() == self:
            tool_tip_window.setText(self.toolTip(), flash=flash)

    def _progressSliderZ(self) -> float:
        return (self.slider_z.value() - self.slider_z.minimum()) / (self.slider_z.maximum() - self.slider_z.minimum())

    def _onSliderZValueChanged(self, _) -> None:
        self.progress_z_ani.setEndValue(self._progressSliderZ())
        self.progress_z_ani.start()

    def _drawXOYPlatePath(self, rect: QRect) -> QPainterPath:
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), 8, 8)
        return path

    def _drawXOYPlateRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(self.style_data.xoy_plate_background_color)
        painter.drawPath(self._drawXOYPlatePath(rect))

    def _drawBackgroundRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(self.style_data.background_color)
        painter.drawPath(self._drawBackgroundPath(rect))

    def _drawDeepestBackgroundRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(self.style_data.deepest_background_color)
        painter.drawPath(self._drawBackgroundPath(rect))

    def _drawBaseLine(self, painter: QPainter, rect: QRect) -> None:  # the rect should be the rect of background.
        margin = self.slider_x.style_data.thumb_width / 2
        available_w = rect.width() - margin * 2
        available_h = rect.height() - margin * 2

        x = margin + available_w * self._progress_x
        y = margin + available_h * (1 - self._progress_y)
        d = 12

        painter.setPen(QPen(self.style_data.base_line_color, self.style_data.base_line_weight))
        painter.drawLine(QPointF(x, margin - d), QPointF(x, margin + d + available_h))
        painter.drawLine(QPointF(margin + rect.x() - d, y), QPointF(margin + available_w + rect.x() + d, y))
        painter.setPen(Qt.NoPen)

    def _drawIndicatorRect(self, painter: QPainter, rect: QRect) -> None:  # the rect should be the rect of background.
        margin = self.slider_x.style_data.thumb_width / 2
        indicator_size = self.style_data.indicator_size - self.style_data.indicator_stroke_weight
        available_w = rect.width() - margin * 2
        available_h = rect.height() - margin * 2

        x = margin + available_w * self._progress_x - indicator_size / 2
        y = margin + available_h * (1 - self._progress_y) - indicator_size / 2
        d = self.style_data.indicator_outline_weight
        indicator_rect = QRectF(x, y, indicator_size, indicator_size)
        indicator_outline_rect = QRectF(x - d, y - d, indicator_size + d * 2, indicator_size + d * 2)
        self.setProperty(self.Property.IndicatorRect, indicator_outline_rect)

        # painter.setBrush(self.style_data.background_color)
        # painter.drawPath(self._drawIndicatorPath(indicator_outline_rect))

        painter.setBrush(self.style_data.indicator_background_color)
        painter.setPen(QPen(self._thumb_color, self.style_data.indicator_stroke_weight))
        painter.drawPath(self._drawIndicatorPath(indicator_rect))
        painter.setPen(Qt.NoPen)

    def wheelEvent(self, a0):
        super().wheelEvent(a0)
        direction = 1 if a0.angleDelta().y() > 0 else -1
        self.slider_z.setValue(self.slider_z.value() + self.slider_z.singleStep() * direction)  # noqa: E501
        self._updateToolTip(flash=False)
        a0.accept()

    def paintEvent(self, a0):
        slider_x_height = self.style_data.slider_y_width
        slider_y_width = self.style_data.slider_x_height
        background_rect = QRect(slider_y_width, 0, self.width() - slider_y_width, self.height() - slider_x_height)
        buffer_rect = QRect(0, 0, self.width() - slider_y_width, self.height() - slider_x_height)

        device_pixel_ratio = self.devicePixelRatioF()
        min_scale_factor = self._min_scale_factor

        buffer = QPixmap(background_rect.size() * device_pixel_ratio)
        buffer.setDevicePixelRatio(device_pixel_ratio)
        buffer.fill(Qt.transparent)

        renderHints = (
                QPainter.RenderHint.SmoothPixmapTransform
                | QPainter.RenderHint.TextAntialiasing
                | QPainter.RenderHint.Antialiasing
        )

        with createPainter(buffer, renderHints) as painter:
            self._drawXOYPlateRect(painter, buffer_rect)
            self._drawBaseLine(painter, buffer_rect)
            self._drawIndicatorRect(painter, buffer_rect)

        a = self._progress_z * (1 - min_scale_factor) + min_scale_factor
        b = min_scale_factor
        with createPainter(self, renderHints) as painter:
            self._drawBackgroundRect(painter, background_rect)

            painter.save()
            painter.translate(QPointF(background_rect.width() * (1 - b) / 2 + self.style_data.slider_y_width,
                                      background_rect.height() * (1 - b) / 2))
            painter.scale(b, b)
            self._drawDeepestBackgroundRect(painter, buffer_rect)

            painter.restore()
            painter.translate(QPointF(background_rect.width() * (1 - a) / 2 + self.style_data.slider_y_width,
                                      background_rect.height() * (1 - a) / 2))
            painter.scale(a, a)
            painter.drawPixmap(0, 0, buffer)


class SiWheelSpinBox(QSpinBox):
    limitReached = pyqtSignal(float)
    carried = pyqtSignal(int)
    increased = pyqtSignal()
    decreased = pyqtSignal()

    def wheelEvent(self, e):
        super().wheelEvent(e)

        delta_y = e.angleDelta().y()
        if delta_y > 0:
            if self.value() == self.maximum():
                self.limitReached.emit(self.value())
            self.stepUp()
            self.increased.emit()

        if delta_y < 0:
            if self.value() == self.minimum():
                self.limitReached.emit(self.value())
            self.stepDown()
            self.decreased.emit()

    def stepBy(self, steps: int) -> None:
        val = self.value()
        min_val = self.minimum()
        max_val = self.maximum()
        range_size = max_val - min_val + 1

        new_val = (val - min_val + steps) % range_size + min_val
        self.setValue(new_val)

        if val + steps > max_val:
            self.carried.emit(1)

        if val + steps < min_val:
            self.carried.emit(-1)


class SiWeekdaySpinBox(QSpinBox):
    WEEKDAYS = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    limitReached = pyqtSignal(float)
    increased = pyqtSignal()
    decreased = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRange(0, 6)  # 索引范围对应一周七天
        self.setWrapping(True)  # 支持循环滚动
        self.setValue(0)

    def textFromValue(self, value):
        if 0 <= value < len(self.WEEKDAYS):
            return self.WEEKDAYS[value]
        return "?"

    def valueFromText(self, text):
        if text in self.WEEKDAYS:
            return self.WEEKDAYS.index(text)
        return 0  # 默认返回星期一

    def validate(self, text, pos):
        if text in self.WEEKDAYS:
            return QValidator.Acceptable, text, pos
        return QValidator.Invalid, text, pos

    def wheelEvent(self, e):
        super().wheelEvent(e)

        delta_y = e.angleDelta().y()
        if delta_y > 0:
            if self.value() == self.maximum():
                self.limitReached.emit(self.value())
            self.stepUp()
            self.increased.emit()

        if delta_y < 0:
            if self.value() == self.minimum():
                self.limitReached.emit(self.value())
            self.stepDown()
            self.decreased.emit()


class WheelPickerStyleData:
    indicator_hover = QColor("#D087DF")
    indicator_idle = QColor("#4C4554")
    indicator_flash = QColor("#F5EBF9")


class SiWheelPickerVertical(SiDenseContainer):
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.style_data = WheelPickerStyleData()
        self._mouse_in = False

        self._indicator = SiLinearIndicator(self)
        self._title_label = QLabel(self)
        self._spinbox = SiWheelSpinBox(self)

        self._container = SiDenseContainer(self, self.TopToBottom)
        self._container.addWidget(self._title_label)
        self._container.addWidget(self._spinbox)
        self._container.layout().setStretchFactor(self._container.stretchWidget(), 0)

        self.layout().setDirection(self.LeftToRight)
        self.addWidget(self._indicator)
        self.addWidget(self._container)

        self._initStyle()

        self._spinbox.valueChanged.connect(self._onValueChanged)
        self._spinbox.limitReached.connect(self._onLimitReached)

    def _initStyle(self):
        self.setFixedHeight(45)
        self.layout().setSpacing(8)
        self._container.layout().setSpacing(0)
        self._container.setContentsMargins(0, 2, 0, 2)

        self._indicator.setVisualWidth(2)
        self._indicator.setVisualHeight(45)
        self._indicator.setFixedSize(4, 45)
        self._indicator.setColor(self.style_data.indicator_idle)

        self._title_label.setFixedHeight(11)
        self._title_label.setAlignment(Qt.AlignTop)
        self._title_label.setFont(SiFont.getFont(size=11, weight=QFont.Bold))
        self._title_label.setStyleSheet(
            "color: #918497;"
            # "background-color: red;"
        )

        self._spinbox.setFixedHeight(33)
        font = SiFont.getFont(size=32, weight=QFont.Bold)
        self._spinbox.setFont(font)
        self._spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self._spinbox.setReadOnly(True)
        self._spinbox.setStyleSheet(
            # "background-color: blue;"
            "color: #D1CBD4;"
            "border: none;"
            "padding: -4px -4px 0px -2px;"
            "selection-color: #D1CBD4;"
            "selection-background-color: transparent;"
        )

    def spinBox(self) -> QSpinBox:
        return self._spinbox

    def setSpinBox(self, spinbox: QSpinBox) -> None:
        self._spinbox.deleteLater()

        self._spinbox = spinbox
        self._spinbox.setParent(self)

        self._initStyle()

        self._spinbox.valueChanged.connect(self._onValueChanged)
        self._spinbox.limitReached.connect(self._onLimitReached)

    def setDirection(self, direction: QBoxLayout.Direction):
        if direction == QBoxLayout.LeftToRight:
            self.layout().setDirection(self.LeftToRight)
            self._title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self._spinbox.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        if direction == QBoxLayout.RightToLeft:
            self.layout().setDirection(self.RightToLeft)
            self._title_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self._spinbox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

    def setTitle(self, value: str) -> None:
        self._title_label.setText(value)

    def _onValueChanged(self, _) -> None:
        end_value = self.style_data.indicator_hover if self._mouse_in else self.style_data.indicator_idle

        self._indicator.colorAnimation().setCurrentValue(self.style_data.indicator_flash)
        self._indicator.colorAnimation().setEndValue(end_value)
        self._indicator.colorAnimation().start()

    def _onLimitReached(self, _) -> None:
        self._indicator.warn()

    def indicatorFlash(self) -> None:
        self._indicator.colorAnimation().setCurrentValue(self.style_data.indicator_flash)
        self._indicator.colorAnimation().start()

    def enterEvent(self, a0):
        super().enterEvent(a0)
        self._mouse_in = True

        self._indicator.colorAnimation().setEndValue(self.style_data.indicator_hover)
        self._indicator.colorAnimation().start()
        self._indicator.visualWidthAnimation().setEndValue(4)
        self._indicator.visualWidthAnimation().start()

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        self._mouse_in = False

        self._indicator.colorAnimation().setEndValue(self.style_data.indicator_idle)
        self._indicator.colorAnimation().start()
        self._indicator.visualWidthAnimation().setEndValue(2)
        self._indicator.visualWidthAnimation().start()


class SiWheelPickerHorizontal(SiDenseContainer):
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.style_data = WheelPickerStyleData()
        self._mouse_in = False

        self._indicator = SiLinearIndicator(self)
        self._title_label = QLabel(self)
        self._spinbox = SiWheelSpinBox(self)

        self.layout().setDirection(self.TopToBottom)
        self.addWidget(self._title_label)
        self.addWidget(self._spinbox)
        self.addWidget(self._indicator)

        self._initStyle()

        self._spinbox.valueChanged.connect(self._onValueChanged)
        self._spinbox.limitReached.connect(self._onLimitReached)

    def _initStyle(self):
        self.setFixedHeight(64)
        self.layout().setSpacing(0)

        self._indicator.setVisualWidth(45)
        self._indicator.setVisualHeight(2)
        self._indicator.setFixedSize(45, 4)
        self._indicator.setColor(self.style_data.indicator_idle)

        # self._title_label.setFixedHeight(12)
        self._title_label.setFont(SiFont.getFont(size=11, weight=QFont.Bold))
        self._title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self._title_label.setStyleSheet(
            # "background-color: red;"
            "color: #918497;"
            "padding-bottom: 3px;"
        )

        self._spinbox.setFixedHeight(40)
        self._spinbox.setFont(SiFont.getFont(size=32, weight=QFont.Bold))
        self._spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self._spinbox.setReadOnly(True)
        self._spinbox.setStyleSheet(
            # "background-color: blue;"
            "color: #D1CBD4;"
            "border: none;"
            "padding: -4px -4px 0px 0px;"
            "selection-color: #D1CBD4;"
            "selection-background-color: transparent;"
            "padding-bottom: 8px;"
        )

    def spinBox(self) -> QSpinBox:
        return self._spinbox

    def setSpinBox(self, spinbox: QSpinBox) -> None:
        self._spinbox.deleteLater()

        self._spinbox = spinbox
        self._spinbox.setParent(self)

        self._initStyle()
        self.layout().insertWidget(1, self._spinbox)

        self._spinbox.valueChanged.connect(self._onValueChanged)
        self._spinbox.limitReached.connect(self._onLimitReached)

    def setTitle(self, value: str) -> None:
        self._title_label.setText(value)

    def _onValueChanged(self, _) -> None:
        end_value = self.style_data.indicator_hover if self._mouse_in else self.style_data.indicator_idle

        self._indicator.colorAnimation().setCurrentValue(self.style_data.indicator_flash)
        self._indicator.colorAnimation().setEndValue(end_value)
        self._indicator.colorAnimation().start()

    def _onLimitReached(self, _) -> None:
        self._indicator.warn()

    def indicatorFlash(self) -> None:
        self._indicator.colorAnimation().setCurrentValue(self.style_data.indicator_flash)
        self._indicator.colorAnimation().start()

    def resizeEvent(self, a0):
        self._indicator.setVisualWidth(self.width())
        self._indicator.setFixedSize(self.width(), 4)

    def enterEvent(self, a0):
        super().enterEvent(a0)
        self._mouse_in = True

        self._indicator.colorAnimation().setEndValue(self.style_data.indicator_hover)
        self._indicator.colorAnimation().start()
        self._indicator.visualHeightAnimation().setEndValue(4)
        self._indicator.visualHeightAnimation().start()

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        self._mouse_in = False

        self._indicator.colorAnimation().setEndValue(self.style_data.indicator_idle)
        self._indicator.colorAnimation().start()
        self._indicator.visualHeightAnimation().setEndValue(2)
        self._indicator.visualHeightAnimation().start()


class ScrollBarStyleData:
    STYLE_TYPES = ["Slider"]

    thumb_idle_color: QColor = QColor("#70EDE1F4")
    thumb_hover_color: QColor = QColor("#EDE1F4")
    thumb_width: int = 52
    thumb_height: int = 8

    track_color: QColor = QColor("#0077568d")
    track_height: int = 5

    background_color: QColor = QColor("#001C191F")


class SiScrollBar(QScrollBar):

    class Property:
        ThumbColor = "thumbColor"
        TrackProgress = "trackProgress"
        ColorOpacity = "colorOpacity"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.setMouseTracking(True)

        self.style_data = ScrollBarStyleData()
        self._thumb_color = self.style_data.thumb_idle_color
        self._track_progress = 0
        self._color_opacity = 1
        self._is_dragging = False
        self._is_dragging_thumb = False
        self._dragging_start_pos = QPoint()
        self._dragging_anchor_pos = QPoint()
        self._value_to_tooltip_func = self._defaultValueToToolTip
        self._is_draw_track = True

        self.thumb_color_ani = SiExpAnimationRefactor(self, self.Property.ThumbColor)
        self.thumb_color_ani.init(1/4, 0.01, self._thumb_color, self._thumb_color)

        self.progress_ani = SiExpAnimationRefactor(self, self.Property.TrackProgress)
        self.progress_ani.init(1/3.5, 0.00001, 0, 0)

        self.color_opacity_ani = SiExpAnimationRefactor(self, self.Property.ColorOpacity)
        self.color_opacity_ani.init(1/6, 0.00001, 1, 1)

        self.valueChanged.connect(self._onValueChanged)
        self.rangeChanged.connect(self._onRangeChanged)

    @pyqtProperty(QColor)
    def thumbColor(self):
        return self._thumb_color

    @thumbColor.setter
    def thumbColor(self, value: QColor):
        self._thumb_color = value
        self.update()

    @pyqtProperty(float)
    def trackProgress(self):
        return self._track_progress

    @trackProgress.setter
    def trackProgress(self, value: float):
        self._track_progress = value
        self.update()

    @pyqtProperty(float)
    def colorOpacity(self):
        return self._color_opacity

    @colorOpacity.setter
    def colorOpacity(self, value: float):
        self._color_opacity = value
        self.update()

    def setPageStep(self, a0):
        super().setPageStep(a0)
        self.update()

    def setDrawTrack(self, state: bool) -> None:
        self._is_draw_track = state
        self.update()

    def isDrawTrack(self) -> bool:
        return self._is_draw_track

    @staticmethod
    def _defaultValueToToolTip(value: int) -> str:
        return str(value)

    def setToolTipConvertionFunc(self, func) -> None:
        self._value_to_tooltip_func = func
        self.setToolTip(func(self.value()))

    def _onValueChanged(self, value):
        if self.maximum() - self.minimum() != 0:
            self.progress_ani.setEndValue((value - self.minimum()) / (self.maximum() - self.minimum()))
            self.progress_ani.start()

    def _onRangeChanged(self, _, __):
        if self.maximum() - self.minimum() != 0:
            self.color_opacity_ani.setEndValue(1)
            self.color_opacity_ani.start()

            p = (self.value() - self.minimum()) / (self.maximum() - self.minimum())
            self.setProperty(self.Property.TrackProgress, p)
            self.progress_ani.fromProperty()
            self.progress_ani.setCurrentValue(p)
            self.progress_ani.setEndValue(p)

        else:
            self.color_opacity_ani.setEndValue(0)
            self.color_opacity_ani.start()

    def _drawBackgroundPath(self, rect) -> QPainterPath:
        radius = min(rect.height() / 2, rect.width() / 2)
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        return path

    def _drawTrackPath(self, rect: QRect) -> QPainterPath:
        radius = min(rect.height() / 2, rect.width() / 2)
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        return path

    def _drawThumbPath(self, rect: QRect) -> QPainterPath:
        radius = min(rect.height() / 2, rect.width() / 2)
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)
        return path

    def _drawBackgroundRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(self.style_data.background_color)
        painter.drawPath(self._drawBackgroundPath(rect))

    def _drawTrackRect(self, painter: QPainter, rect: QRect) -> None:
        if self._is_draw_track:
            painter.setBrush(self.style_data.track_color)
            painter.drawPath(self._drawTrackPath(rect))

    def _drawThumbRect(self, painter: QPainter, rect: QRect) -> None:
        color = QColor(self._thumb_color)
        color.setAlphaF(color.alphaF() * self._color_opacity)
        painter.setBrush(color)
        painter.drawPath(self._drawThumbPath(rect))

    def _isMouseInThumbRect(self, pos: QPoint) -> bool:
        p = self._track_progress
        thumb_w = self.style_data.thumb_width
        thumb_h = self.style_data.thumb_height
        if self.orientation() == Qt.Orientation.Horizontal:
            thumb_rect = QRectF((self.width() - thumb_w) * p, (self.height() - thumb_h) / 2, thumb_w, thumb_h)
        else:
            thumb_rect = QRectF((self.width() - thumb_h) / 2, (self.height() - thumb_w) * p, thumb_h, thumb_w)
        return thumb_rect.contains(pos)

    def _setValueToMousePos(self, pos: QPoint) -> None:
        thumb_width = self.style_data.thumb_width
        region = self.maximum() - self.minimum()
        if self.orientation() == Qt.Orientation.Horizontal:
            p = min(1, max((pos.x() - thumb_width / 2) / (self.width() - thumb_width), 0))
        else:
            p = min(1, max((pos.y() - thumb_width / 2) / (self.height() - thumb_width), 0))
        self.setValue(int(self.minimum() + region * p))

    def _setThumbHovering(self, state: bool) -> None:
        if state:
            self.thumb_color_ani.setEndValue(self.style_data.thumb_hover_color)
            self.thumb_color_ani.start()
        else:
            self.thumb_color_ani.setEndValue(self.style_data.thumb_idle_color)
            self.thumb_color_ani.start()

    def _updateDraggingAnchor(self):
        p = (self.value() - self.minimum()) / (self.maximum() - self.minimum())
        thumb_w = self.style_data.thumb_width
        thumb_h = self.style_data.thumb_height
        if self.orientation() == Qt.Orientation.Horizontal:
            thumb_rect = QRectF((self.width() - thumb_w) * p, (self.height() - thumb_h) / 2, thumb_w, thumb_h)
        else:
            thumb_rect = QRectF((self.width() - thumb_h) / 2, (self.height() - thumb_w) * p, thumb_h, thumb_w)
        self._dragging_anchor_pos = thumb_rect.center()

    def event(self, event):
        if event.type() == QEvent.ToolTip:
            return True  # 忽略工具提示事件
        return super().event(event)

    def enterEvent(self, a0):
        super().enterEvent(a0)
        self._setThumbHovering(True)

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        self._setThumbHovering(False)

    def mousePressEvent(self, a0):
        super().mousePressEvent(a0)
        self.sliderPressed.emit()

        if self.maximum() == self.minimum():
            return

        self._is_dragging = True
        if self._isMouseInThumbRect(a0.pos()):
            self._is_dragging_thumb = True
            self._updateDraggingAnchor()
            self._dragging_start_pos = a0.pos()
        else:
            self._setValueToMousePos(a0.pos())

    def mouseMoveEvent(self, a0):
        super().mouseMoveEvent(a0)
        if self._is_dragging:
            if self._is_dragging_thumb:
                pos = self._dragging_anchor_pos + (a0.pos() - self._dragging_start_pos)
                self._setValueToMousePos(pos)
            else:
                self._setValueToMousePos(a0.pos())

        else:
            self._setThumbHovering(state=self._isMouseInThumbRect(a0.pos()))

    def mouseReleaseEvent(self, a0):
        super().mouseReleaseEvent(a0)
        self.sliderReleased.emit()

        self._setThumbHovering(False)
        self._is_dragging_thumb = False
        self._is_dragging = False

    def paintEvent(self, event):
        p = self._track_progress
        thumb_w = self.style_data.thumb_width
        thumb_h = self.style_data.thumb_height
        track_w = self.style_data.track_height
        track_h = self.style_data.track_height

        if self.orientation() == Qt.Orientation.Horizontal:
            background_rect = QRectF(0, (self.height() - track_h) / 2, self.width(), track_h)
            track_rect = QRectF(0, (self.height() - track_h) / 2, thumb_w / 2 + (self.width() - thumb_w) * p, track_h)
            thumb_rect = QRectF((self.width() - thumb_w) * p, (self.height() - thumb_h) / 2, thumb_w, thumb_h)
        else:
            background_rect = QRectF((self.width() - track_w) / 2, 0, track_w, self.height())
            track_rect = QRectF((self.width() - track_w) / 2, self.height() * (1-p), track_w, self.height() * p)
            thumb_rect = QRectF((self.width() - thumb_h) / 2, (self.height() - thumb_w) * p, thumb_h, thumb_w)

        renderHints = (
                QPainter.RenderHint.SmoothPixmapTransform
                | QPainter.RenderHint.TextAntialiasing
                | QPainter.RenderHint.Antialiasing
        )

        with createPainter(self, renderHints) as painter:
            self._drawBackgroundRect(painter, background_rect)
            self._drawTrackRect(painter, track_rect)
            self._drawThumbRect(painter, thumb_rect)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        page_step = self.pageStep()
        length = self.width() if self.orientation() == Qt.Horizontal else self.height()
        space = (page_step + self.maximum() - self.minimum())

        if space == 0:
            self.style_data.thumb_width = 0
        else:
            self.style_data.thumb_width = page_step / space * length


class SiScrollAreaRefactor(QScrollArea):
    class Property:
        ContentsPos = "contentsPos"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self._over_scroll = False

        self._contents_visual_pos = QPointF(0.0, 0.0)
        self._contents_anchor_pos = QPointF(0.0, 0.0)
        self.contents_pos_ani = SiExpAnimationRefactor(self, self.Property.ContentsPos)
        self.contents_pos_ani.init(1/6, 2, self._contents_visual_pos, self._contents_visual_pos)

        self._initScrollBar()
        self.setStyleSheet("background-color: transparent; border: none; border-radius: 6px")

        self.pileScrollTimer = QTimer(self)
        self.pileScrollTimer.setSingleShot(True)
        self.pileScrollTimer.timeout.connect(self._onPileScrollTriggered)

    @pyqtProperty(QPointF)
    def contentsPos(self):
        return self._contents_visual_pos

    @contentsPos.setter
    def contentsPos(self, value: QPointF):
        self._contents_visual_pos = value
        self.widget().move(int(value.x()), int(value.y()))

    def isOverScrollEnabled(self) -> bool:
        return self._over_scroll

    def setOverScrollEnabled(self, state: bool) -> None:
        self._over_scroll = state

    def _initScrollBar(self) -> None:
        self.scrollbar_v = SiScrollBar(self)
        self.scrollbar_v.setOrientation(Qt.Vertical)
        self.scrollbar_v.setFixedWidth(8)
        self.scrollbar_v.setStyleSheet(
            "QScrollBar:vertical {"
            "    border: none;"
            "    width: 8px;"
            "    margin: 0px 0px 0px 0px;"
            "}"
        )

        self.scrollbar_h = SiScrollBar(self)
        self.scrollbar_h.setOrientation(Qt.Horizontal)
        self.scrollbar_h.setFixedHeight(8)
        self.scrollbar_h.setStyleSheet(
            "QScrollBar:horizontal {"
            "    border: none;"
            "    height: 8px;"
            "    margin: 0px 0px 0px 0px;"
            "}"
        )

        self.setVerticalScrollBar(self.scrollbar_v)
        self.setHorizontalScrollBar(self.scrollbar_h)

    def _onPileScrollTriggered(self) -> None:
        self.contents_pos_ani.setEndValue(self._contents_anchor_pos)
        self.contents_pos_ani.start()

    def _createPileScroll(self) -> None:
        self.pileScrollTimer.start(80)

    def _cancelPileScroll(self) -> None:
        self.pileScrollTimer.stop()

    def _overScrollStepLength(self) -> float:
        anchor = self._contents_anchor_pos
        visual = self.contents_pos_ani.endValue()
        dis = max(0, abs(anchor.y() - visual.y()))

        k, init_step = 0.05, 10
        return math.exp(-dis * k) * init_step

    def wheelEvent(self, a0):
        anchor = self._contents_anchor_pos
        visual = self._contents_visual_pos

        scroll_length = self.scrollbar_v.maximum() - self.scrollbar_v.minimum()
        wheel_delta_y = a0.angleDelta().y()
        end_y = anchor.y()
        k = min(1, abs(wheel_delta_y) / 120)

        if scroll_length != 0 and self._over_scroll:

            if end_y == 0 and wheel_delta_y > 0:
                new_pos = QPointF(visual)  # 拿视觉位置处理
                new_pos.setY(max(new_pos.y(), anchor.y()) + self._overScrollStepLength() * k)

                self.contents_pos_ani.setEndValue(new_pos)
                self.contents_pos_ani.start()

                self._cancelPileScroll()
                self._createPileScroll()  # 创建计划滚动

            if end_y == -scroll_length and wheel_delta_y < 0:
                new_pos = QPointF(visual)  # 拿视觉位置处理
                new_pos.setY(min(new_pos.y(), anchor.y()) - self._overScrollStepLength() * k)

                self.contents_pos_ani.setEndValue(new_pos)
                self.contents_pos_ani.start()

                self._cancelPileScroll()
                self._createPileScroll()  # 创建计划滚动

            if 0 > end_y > -scroll_length:
                self._cancelPileScroll()

        super().wheelEvent(a0)

    def scrollContentsBy(self, dx, dy):
        anchor = self._contents_anchor_pos
        self._contents_anchor_pos.setX(anchor.x() + dx)
        self._contents_anchor_pos.setY(anchor.y() + dy)

        self.contents_pos_ani.setEndValue(self._contents_anchor_pos)
        self.contents_pos_ani.start()

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.contents_pos_ani.stop()


class SiScrollAreaGraphicWidget(QWidget):
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self._proxy_widget = SiAnimatedTransformGraphicProxyWidget()
        self._scene = QGraphicsScene()
        self._view = QGraphicsView(self._scene, self)
        self._scroll_area = SiScrollAreaRefactor()

        self._proxy_widget.setWidget(self._scroll_area)
        self._scene.addItem(self._proxy_widget)

        self._initStyle()

    def _initStyle(self) -> None:
        self._view.setStyleSheet("background-color: transparent; border: none")
        self._view.setRenderHints(
            QPainter.Antialiasing
            | QPainter.SmoothPixmapTransform
            | QPainter.TextAntialiasing
        )

    def scrollArea(self) -> SiScrollAreaRefactor:
        return self._scroll_area

    def fadeIn(self) -> None:
        translate_ani = self._proxy_widget.animation(self._proxy_widget.Property.Translate)
        opacity_ani = self._proxy_widget.animation(self._proxy_widget.Property.Opacity)

        translate_ani.setCurrentValue(QPointF(0, 50))
        translate_ani.setEndValue(QPointF(0, 0))
        translate_ani.start()

        opacity_ani.setCurrentValue(0.0)
        opacity_ani.setEndValue(1.0)
        opacity_ani.start()

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self._view.setGeometry(0, 0, self.width(), self.height())
        self._scene.setSceneRect(QRectF(0, 0, self.width(), self.height()))
        self._scroll_area.resize(self.size())

        self._proxy_widget.setProperty(self._proxy_widget.Property.Center, QPointF(self.width() / 2, self.height() / 2))
