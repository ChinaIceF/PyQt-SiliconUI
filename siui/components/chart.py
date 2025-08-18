from dataclasses import dataclass

from PyQt5.QtCore import QEvent, QLineF, QPoint, QPointF, QRect, QRectF, Qt, pyqtProperty
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QPen, QPixmap
from PyQt5.QtWidgets import QWidget

from siui.core import createPainter, hideToolTip, isTooltipShown, showToolTip
from siui.core.animation import SiExpAnimationRefactor
from siui.typing import T_WidgetParent


# @dataclass
class TrendChartStyleData:
    background_color: QColor = QColor("#25222a")
    major_tick_color: QColor = QColor("#433b49")
    minor_tick_color: QColor = QColor("#2e2a34")
    axis_tick_color: QColor = QColor("#6a5e73")

    axis_label_color: QColor = QColor("#918497")
    axis_name_color: QColor = QColor("#DFDFDF")

    line_color: QColor = QColor("#D087DF")
    indicator_idle_color: QColor = QColor("#00DFDFDF")
    indicator_hover_color: QColor = QColor("#FFDFDFDF")
    tick_text_color: QColor = QColor("#918497")

    axis_y_label_width: int = 64
    axis_y_name_width: int = 32
    axis_x_label_height: int = 32
    axis_x_name_height: int = 32

    border_radius: int = 6


class SiTrendChart(QWidget):
    class Property:
        IndicatorPosition = "indicatorPosition"
        IndicatorColor = "indicatorColor"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)
        self.setMouseTracking(True)

        self._point_list = []
        self._shown_point_list = []
        self.style_data = TrendChartStyleData()
        self._shown_point_pixmap = QPixmap()

        self._view_rect = QRectF(0, 0, 100, 100)
        self._x_tick_delta = 10
        self._x_minor_tick_count = 4
        self._y_tick_delta = 10
        self._y_minor_tick_count = 4
        self._quality = 1
        self._indicator_position = QPointF(0, 0)
        self._indicator_color = self.style_data.indicator_idle_color
        self._x_tick_name_func = lambda x: str(round(x, 1))
        self._y_tick_name_func = lambda x: str(round(x, 2))
        self._tool_tip_func = lambda x, y: f"x = {round(x, 4)}\ny = {round(y, 4)}"

        self.indicator_pos_ani = SiExpAnimationRefactor(self, self.Property.IndicatorPosition)
        self.indicator_pos_ani.init(1/3.5, 0.01, self._indicator_position, self._indicator_position)

        self.indicator_color_ani = SiExpAnimationRefactor(self, self.Property.IndicatorColor)
        self.indicator_color_ani.init(1/4, 0.01, self._indicator_color, self._indicator_color)

    @pyqtProperty(QPointF)
    def indicatorPosition(self):
        return self._indicator_position

    @indicatorPosition.setter
    def indicatorPosition(self, value: QPointF):
        self._indicator_position = value
        self.update()

    @pyqtProperty(QColor)
    def indicatorColor(self):
        return self._indicator_color

    @indicatorColor.setter
    def indicatorColor(self, value: QColor):
        self._indicator_color = value
        self.update()

    def setViewRect(self, rect: QRectF) -> None:
        self._view_rect = rect
        self._updateShownPointPixmap()
        self.update()

    def viewRect(self) -> QRectF:
        return self._view_rect

    def pointList(self) -> list:
        return self._point_list

    def setPointList(self, plist: list) -> None:
        self._point_list = plist
        self._updateShownPointList()
        self._updateShownPointPixmap()
        self.update()

    def setXTickNameFunc(self, func) -> None:
        self._x_tick_name_func = func
        self.update()

    def setYTickNameFunc(self, func) -> None:
        self._y_tick_name_func = func
        self.update()

    def setToolTipFunc(self, func) -> None:
        self._tool_tip_func = func

    def setQuality(self, q: float) -> None:
        self._quality = q
        self._updateShownPointList()
        self._updateShownPointPixmap()
        self.update()

    def adjustViewRect(self, policy: Qt.AspectRatioMode = Qt.KeepAspectRatio):
        xs = [point.x() for point in self._point_list]
        ys = [point.y() for point in self._point_list]
        rect = QRectF(min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))

        pixel_rate_x = rect.width() / self._getChartRect().width()
        pixel_rate_y = rect.height() / self._getChartRect().height()

        if policy == Qt.IgnoreAspectRatio:
            self._view_rect = rect
            self.update()

        if policy == Qt.KeepAspectRatio:
            self._y_tick_delta = self._y_tick_delta / (pixel_rate_x / pixel_rate_y)
            self._view_rect = rect
            self.update()

        if policy == Qt.KeepAspectRatioByExpanding:
            rate = (rect.width() / rect.height()) / (pixel_rate_x / pixel_rate_y)
            delta = rect.height() * (rate - 1)
            rect.setHeight(rect.height() * rate)
            rect.setY(rect.y() + delta / 2)
            self._view_rect = rect
            self.update()

    def coordinateToPos(self, coordinate_point: QPointF, chart_rect: QRectF) -> QPointF:
        """ returns displaying position of the given data point """
        px = (coordinate_point.x() - self._view_rect.x()) / self._view_rect.width()
        py = (coordinate_point.y() - self._view_rect.y()) / self._view_rect.height()
        return QPointF(px * chart_rect.width(), (1 - py) * chart_rect.height())

    def posToCoordinate(self, pos: QPointF, chart_rect: QRectF) -> QPointF:
        px = pos.x() / chart_rect.width()
        py = pos.y() / chart_rect.height()
        return QPointF(px * self._view_rect.width() + self._view_rect.x(),
                       (1 - py) * self._view_rect.height() + self._view_rect.y())

    def event(self, event):
        if event.type() == QEvent.ToolTip:
            return True  # 忽略工具提示事件
        return super().event(event)

    def _isMousePosValid(self, pos: QPoint) -> bool:
        rect = self._getChartRect()
        return rect.contains(pos)

    def _findClosestDataPoint(self, cx: float) -> QPointF:
        distances = [(abs(point.x() - cx), point) for point in self._shown_point_list]
        distances.sort(key=lambda x: x[0])
        return distances[0][1]

    def _updateShownPointPixmap(self) -> None:
        chart_rect = self._getChartRect().toRect()
        device_pixel_ratio = self.devicePixelRatioF()

        renderHints = (
            QPainter.RenderHint.SmoothPixmapTransform
            | QPainter.RenderHint.TextAntialiasing
            | QPainter.RenderHint.Antialiasing
        )

        buffer = QPixmap(chart_rect.size() * device_pixel_ratio)
        buffer.setDevicePixelRatio(device_pixel_ratio)
        buffer.fill(Qt.transparent)

        with createPainter(buffer, renderHints) as painter:
            self._drawDataLine(painter, chart_rect)

        self._shown_point_pixmap = buffer
        self.update()

    def _updateShownPointList(self) -> None:
        if self._quality == -1:
            self._shown_point_list = self._point_list
            return

        result = [self._point_list[0]]
        min_step = self._view_rect.width() / self._getChartRect().width() / self._quality

        for point in self._point_list:
            if point.x() - result[-1].x() >= min_step:
                result.append(point)

        self._shown_point_list = result

    def _getBackgroundRect(self) -> QRectF:
        return QRectF(self.style_data.axis_y_name_width + self.style_data.axis_y_label_width,
                      0,
                      self.width() - self.style_data.axis_y_name_width - self.style_data.axis_y_label_width,
                      self.height() - self.style_data.axis_x_name_height - self.style_data.axis_x_label_height)

    def _getChartRect(self) -> QRectF:
        rect = self._getBackgroundRect()
        return QRectF(rect.x() + 24, rect.y() + 24, rect.width() - 48, rect.height() - 48)

    def _getTickLine(self, chart_rect: QRectF) -> list:
        minor_ticks, major_ticks = [], []
        minor_points, major_points = [], []
        x_minor_tick_delta = self._x_tick_delta / (self._x_minor_tick_count + 1)
        y_minor_tick_delta = self._y_tick_delta / (self._y_minor_tick_count + 1)
        start_tick_index_x: int = self._view_rect.x() // x_minor_tick_delta + 1
        start_tick_index_y: int = self._view_rect.y() // y_minor_tick_delta + 1

        now_tick_index = start_tick_index_x - 1

        while (now_tick_index - 1) * x_minor_tick_delta < self._view_rect.x() + self._view_rect.width():  # 垂直
            p1 = QPointF(now_tick_index * x_minor_tick_delta, self._view_rect.y())
            p2 = QPointF(now_tick_index * x_minor_tick_delta, self._view_rect.y() + self._view_rect.height())
            line = QLineF(self.coordinateToPos(p1, chart_rect) + chart_rect.topLeft() + QPointF(0, 12),
                          self.coordinateToPos(p2, chart_rect) + chart_rect.topLeft() + QPointF(0, -12))

            if now_tick_index % (self._x_minor_tick_count + 1) == 0:
                major_ticks.append(line)
                major_points.append(p1)
            else:
                minor_ticks.append(line)
                minor_points.append(p1)
            now_tick_index += 1

        now_tick_index = start_tick_index_y - 1

        while (now_tick_index - 1) * y_minor_tick_delta < self._view_rect.y() + self._view_rect.height():  # 垂直
            p1 = QPointF(self._view_rect.x(),                           now_tick_index * y_minor_tick_delta)
            p2 = QPointF(self._view_rect.x() + self._view_rect.width(), now_tick_index * y_minor_tick_delta)
            line = QLineF(self.coordinateToPos(p1, chart_rect) + chart_rect.topLeft() + QPointF(-12, 0),
                          self.coordinateToPos(p2, chart_rect) + chart_rect.topLeft() + QPointF(12, 0))

            if now_tick_index % (self._y_minor_tick_count + 1) == 0:
                major_ticks.append(line)
                major_points.append(p1)
            else:
                minor_ticks.append(line)
                minor_points.append(p1)
            now_tick_index += 1

        return [minor_ticks, major_ticks, minor_points, major_points]

    def _drawBackgroundPath(self, rect: QRect) -> QPainterPath:
        radius = self.style_data.border_radius
        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)
        return path

    def _drawBackgroundRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(self.style_data.background_color)
        painter.drawPath(self._drawBackgroundPath(rect))

    def _drawTickLine(self, painter: QPainter, rect: QRectF) -> None:
        minor_ticks, major_ticks, _, _ = self._getTickLine(rect)

        pen_minor = QPen(self.style_data.minor_tick_color)
        pen_minor.setWidthF(1)
        pen_minor.setCapStyle(Qt.RoundCap)
        pen_major = QPen(self.style_data.major_tick_color)
        pen_major.setWidthF(1)
        pen_major.setCapStyle(Qt.RoundCap)
        pen_axis = QPen(self.style_data.axis_tick_color)
        pen_axis.setWidthF(1)
        pen_axis.setCapStyle(Qt.RoundCap)

        painter.setPen(pen_minor)
        for line in minor_ticks:
            painter.drawLine(line)

        painter.setPen(pen_major)
        for line in major_ticks:
            painter.drawLine(line)

        # painter.setPen(pen_axis)
        # for line in major_ticks:
        #     cp = self.posToCoordinate(line.p1() - rect.topLeft(), rect)
        #     if cp.x() == 0 or cp.y() == 0:
        #         painter.drawLine(line)

        painter.setPen(Qt.NoPen)

    def _drawTickText(self, painter: QPainter, rect: QRectF) -> None:
        _, major_ticks, _, major_points = self._getTickLine(rect)

        painter.setPen(self.style_data.tick_text_color)
        for line, point in zip(major_ticks, major_points):
            if line.dx() == 0:  # 竖直线
                text = self._x_tick_name_func(point.x())
                painter.drawText(QRectF(line.p1().x() - 32, rect.bottom() + 32, 64, 32), Qt.AlignCenter, text)
            if line.dy() == 0:  # 水平线
                text = self._y_tick_name_func(point.y())
                painter.drawText(QRectF(rect.left() - 64 - 32, line.p1().y() - 16, 64, 32), Qt.AlignCenter, text)

    def _drawDataLine(self, painter: QPainter, rect: QRect) -> None:
        chart_rect = self._getChartRect()
        self._shown_point_pos = [self.coordinateToPos(point, chart_rect) for point in self._shown_point_list]

        points = self._shown_point_pos

        pen = QPen(self.style_data.line_color)
        pen.setWidthF(2)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.drawPolyline(*points)

    def _drawDataLinePixmap(self, painter: QPainter, rect: QRectF) -> None:
        painter.drawPixmap(rect.toRect(), self._shown_point_pixmap)

    def _drawIndicatorRect(self, painter: QPainter, rect: QRectF) -> None:
        pos = self._indicator_position

        path_line = QPainterPath()
        path_line.addRoundedRect(pos.x() + rect.x() - 1, -12 + rect.y(), 2, rect.height() + 24, 1, 1)
        painter.setBrush(self._indicator_color)
        painter.drawPath(path_line)

        path_circle = QPainterPath()
        path_circle.addRoundedRect(pos.x() - 6 + rect.x(), pos.y() - 16 + rect.y(), 12, 32, 6, 6)
        painter.setBrush(self._indicator_color)
        painter.drawPath(path_circle)

    def paintEvent(self, a0):
        bg_rect = self._getBackgroundRect()
        chart_rect = self._getChartRect()

        renderHints = (
            QPainter.RenderHint.SmoothPixmapTransform
            | QPainter.RenderHint.TextAntialiasing
            | QPainter.RenderHint.Antialiasing
        )

        with createPainter(self, renderHints) as painter:
            self._drawBackgroundRect(painter, bg_rect)
            self._drawTickLine(painter, chart_rect)
            self._drawDataLinePixmap(painter, chart_rect)
            self._drawIndicatorRect(painter, chart_rect)
            self._drawTickText(painter, chart_rect)

    def mouseMoveEvent(self, a0):
        super().mouseMoveEvent(a0)

        chart_rect = self._getChartRect()
        pos = a0.pos() - chart_rect.topLeft()
        cpos = self.posToCoordinate(pos, chart_rect)
        closest_point = self._findClosestDataPoint(cpos.x())

        self.indicator_pos_ani.setEndValue(
            QPointF(
                min(max(0, self.coordinateToPos(closest_point, chart_rect).x()), chart_rect.width()),
                self.coordinateToPos(closest_point, chart_rect).y()
            )
        )
        self.indicator_pos_ani.start()
        self.setToolTip(self._tool_tip_func(closest_point.x(), closest_point.y()))

        if self._isMousePosValid(a0.pos()):
            showToolTip(self, flash=not isTooltipShown())
            self.indicator_color_ani.setEndValue(self.style_data.indicator_hover_color)
            self.indicator_color_ani.start()
        else:
            hideToolTip(self)
            self.indicator_color_ani.setEndValue(self.style_data.indicator_idle_color)
            self.indicator_color_ani.start()

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self._updateShownPointList()
        self._updateShownPointPixmap()
        self.update()
