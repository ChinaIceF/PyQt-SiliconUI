from dataclasses import dataclass

from PyQt5.QtCore import QEvent, QPoint, QRect, QRectF, pyqtProperty, Qt
from PyQt5.QtGui import QColor, QPainter, QPainterPath
from PyQt5.QtWidgets import QAbstractSlider

from siui.core import SiGlobal, createPainter
from siui.core.animation import SiExpAnimationRefactor
from siui.typing import T_WidgetParent


@dataclass
class SliderStyleData:
    STYLE_TYPES = ["Slider"]

    thumb_idle_color: QColor = QColor("#9F89AA")
    thumb_hover_color: QColor = QColor("#EDE1F4")
    thumb_width: int = 52
    thumb_height: int = 14

    track_color: QColor = QColor("#9F89AA")
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
        self._track_color = self.style_data.track_color
        self._thumb_color = self.style_data.thumb_idle_color
        self._background_color = self.style_data.background_color
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
        self.progress_ani.init(1/4, 0.0001, 0, 0)

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

    def _onValueChanged(self, value):
        self.progress_ani.setEndValue((value - self.minimum()) / (self.maximum() - self.minimum()))
        self.progress_ani.start()
        self.setToolTip(self._value_to_tooltip_func(self.value()))
        self._updateToolTip(flash=False)

    def _onRangeChanged(self, _, __):
        p = (self.value() - self.minimum()) / (self.maximum() - self.minimum())
        self.setProperty(self.Property.TrackProgress, p)
        self.progress_ani.update()
        self.progress_ani.setCurrentValue(p)
        self.progress_ani.setEndValue(p)

    def _drawBackgroundPath(self, rect) -> QPainterPath:
        radius = min(rect.height() / 2, rect.width() / 2)
        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)
        return path

    def _drawTrackPath(self, rect: QRect) -> QPainterPath:
        radius = min(rect.height() / 2, rect.width() / 2)
        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)
        return path

    def _drawThumbPath(self, rect: QRect) -> QPainterPath:
        radius = min(rect.height() / 2, rect.width() / 2)
        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)
        return path

    def _drawBackgroundRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(self._background_color)
        painter.drawPath(self._drawBackgroundPath(rect))

    def _drawTrackRect(self, painter: QPainter, rect: QRect) -> None:
        if self._is_draw_track:
            painter.setBrush(self._track_color)
            painter.drawPath(self._drawTrackPath(rect))

    def _drawThumbRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(self._thumb_color)
        painter.drawPath(self._drawThumbPath(rect))

    def _isMouseInThumbRect(self, pos: QPoint) -> bool:
        p = self._track_progress
        thumb_w = self.style_data.thumb_width
        thumb_h = self.style_data.thumb_height
        thumb_rect = QRectF((self.width() - thumb_w) * p, (self.height() - thumb_h) / 2, thumb_w, thumb_h)
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
        thumb_rect = QRectF((self.width() - thumb_w) * p, (self.height() - thumb_h) / 2, thumb_w, thumb_h)
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
            track_rect = QRectF(0, (self.height() - track_h) / 2, self.width() * p, track_h)
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

