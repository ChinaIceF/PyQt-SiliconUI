from __future__ import annotations

from PyQt5.QtCore import QEvent, QObject, QPoint, QRect, QSize, Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QLayout, QLayoutItem, QWidget, QWidgetItem

from siui.core.animation import SiExpAnimationRefactor
from siui.typing import T_WidgetParent


class AnimatedWidgetItem(QWidgetItem):
    class Property:
        Geometry = "geometry"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.ani_geometry = SiExpAnimationRefactor(parent, self.Property.Geometry)
        self.ani_geometry.init(1/4, 0.2, self.geometry(), self.geometry())

    def animation(self, prop_name: str) -> SiExpAnimationRefactor:
        return {
            self.Property.Geometry: self.ani_geometry,
        }.get(prop_name)

    def setGeometry(self, a0):
        self.ani_geometry.setEndValue(a0)
        self.ani_geometry.start()

    def setGeometryDirectly(self, a0):
        self.widget().setGeometry(a0)
        self.ani_geometry.fromProperty()


class DraggingEventFilter(QObject):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._is_dragging = False
        self._drag_start_pos = QPoint()
        self._widget_start_pos = QPoint()
        self._target = parent  # 默认是 parent

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        # 确保事件是来自我们期望的 widget
        if obj != self._target:
            return super().eventFilter(obj, event)

        if event.type() == QEvent.MouseButtonPress:
            mouse_event: QMouseEvent = event
            if mouse_event.button() == Qt.LeftButton:
                self._is_dragging = True
                self._drag_start_pos = mouse_event.globalPos()
                self._widget_start_pos = self._target.pos()
                return False

        elif event.type() == QEvent.MouseMove:
            mouse_event: QMouseEvent = event
            if self._is_dragging and (mouse_event.buttons() & Qt.LeftButton):
                delta = mouse_event.globalPos() - self._drag_start_pos
                new_pos = self._widget_start_pos + delta
                # 直接移动目标 widget
                self._target.move(new_pos)
                return False

        elif event.type() == QEvent.MouseButtonRelease:
            mouse_event: QMouseEvent = event
            if mouse_event.button() == Qt.LeftButton:
                self._is_dragging = False
                # 拖动结束后的逻辑，比如通知 AnimatedWidgetItem 布局更新
                # 但在当前场景，我们让 AnimatedWidgetItem 的 setGeometry 自动适应
                return False

        return super().eventFilter(obj, event)

    def is_dragging(self) -> bool:
        return self._is_dragging


class DraggableWidgetItem(QWidgetItem):
    class Property:
        Geometry = "geometry"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self._trigger = parent

        self.ani_geometry = SiExpAnimationRefactor(parent, self.Property.Geometry)
        self.ani_geometry.init(1/4, 0.2, self.geometry(), self.geometry())
        self.layout()

    def trigger(self) -> QWidget:
        return self._trigger

    def setTrigger(self) -> None:
        self._trigger.removeEventFilter(self)

    def animation(self, prop_name: str) -> SiExpAnimationRefactor:
        return {
            self.Property.Geometry: self.ani_geometry,
        }.get(prop_name)

    def setGeometry(self, a0):
        self.ani_geometry.setEndValue(a0)
        self.ani_geometry.start()

    def setGeometryDirectly(self, a0):
        self.widget().setGeometry(a0)
        self.ani_geometry.fromProperty()


class SiMasonryLayout(QLayout):
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self._column_width = 96
        self._column_spacing = 8
        self._line_spacing = 8
        self._max_column_height_cache = 0
        self._items = []

    def addItem(self, a0: QLayoutItem) -> None:
        self._items.append(a0)
        self.invalidate()

    def count(self) -> int:
        return len(self._items)

    def itemAt(self, index: int) -> QLayoutItem | None:
        if index >= len(self._items) or index < 0:
            return None
        return self._items[index]

    def takeAt(self, index) -> QLayoutItem | None:
        if index >= len(self._items) or index < 0:
            return None
        return self._items.pop(index)

    def sizeHint(self) -> QSize:
        width_unit = self._column_width + self._column_spacing
        column_n = (self.geometry().width() + self._column_spacing) // width_unit
        width = column_n * width_unit - self._column_spacing
        height = self._max_column_height_cache - self._line_spacing
        return QSize(width, height)

    def columnWidth(self) -> int:
        return self._column_width

    def setColumnWidth(self, width: int) -> None:
        self._column_width = width
        self.invalidate()

    def columnSpacing(self) -> int:
        return self._column_spacing

    def setColumnSpacing(self, a0: int) -> None:
        self._column_spacing = a0
        self.invalidate()

    def lineSpacing(self) -> int:
        return self._line_spacing

    def setLineSpacing(self, a0: int) -> None:
        self._line_spacing = a0
        self.invalidate()

    def _getItemSize(self, item: QLayoutItem) -> QSize:
        widget = item.widget()
        if widget is None:
            return item.geometry().size()

        width = self._column_width
        if widget.hasHeightForWidth():
            height = widget.heightForWidth(width)
        else:
            height = widget.height()

        return QSize(width, height)

    def setGeometry(self, geo):
        super().setGeometry(geo)

        margins = self.parentWidget().contentsMargins()
        rect = self.geometry()
        rect_no_margin = rect.marginsAdded(margins)

        width_unit = self._column_width + self._column_spacing
        column_n = (rect.width() + self._column_spacing) // width_unit
        column_height = [0 for _ in range(column_n)]

        for i in range(self.count()):
            item = self.itemAt(i)
            column_index = i % column_n

            pos = QPoint(width_unit * column_index, column_height[column_index]) + rect.topLeft()
            size = self._getItemSize(item)
            new_rect = QRect(pos, size)

            column_height[column_index] += size.height() + self._line_spacing

            if ((not rect_no_margin.intersects(new_rect)) and (not rect_no_margin.intersects(item.geometry()))
                    and isinstance(item, AnimatedWidgetItem)):
                item.setGeometryDirectly(new_rect)  # 初末位置都不可见，并且是 AnimatedWidgetItem，则取消动画以优化性能

            else:
                item.setGeometry(new_rect)

        self._max_column_height_cache = max(column_height)
