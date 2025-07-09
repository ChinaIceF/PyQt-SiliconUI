from __future__ import annotations

from PyQt5.QtCore import QEvent, QObject, QPoint, QRect, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QLayout, QLayoutItem, QWidget, QWidgetItem

from siui.core import SiQuickEffect
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
    dropped = pyqtSignal()
    dragged = pyqtSignal(QPoint)
    pressed = pyqtSignal()

    def __init__(self, item: QLayoutItem, target: QWidget, trigger: QWidget):
        super().__init__()
        # parent 是 LayoutItem, target 是 item 的 widget, trigger 是 widget 或者其子控件
        self._is_dragging = False
        self._drag_start_pos = QPoint()
        self._widget_start_pos = QPoint()
        self._item = item           # LayoutItem
        self._target = target       # move 的作用对象
        self._trigger = trigger     # 谁触发拖动

        self.dropped.connect(self._onDropped)
        self.dragged.connect(self._onDragged)

    def _onDropped(self) -> None:
        layout = self._target.parentWidget().layout()
        layout.invalidate()

    def _onDragged(self, _) -> None:
        center = self._target.geometry().center()
        layout = self._target.parentWidget().layout()

        insert_at_index = None
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item is self._item:
                continue
            if item.animation("geometry").state() == SiExpAnimationRefactor.State.Running:
                continue
            if item.geometry().contains(center):
                insert_at_index = i
                break

        if insert_at_index is None:
            return

        layout.removeItem(self._item)
        layout.insertItem(self._item, insert_at_index)
        layout.invalidate()

    def target(self) -> QWidget:
        return self._target

    def setTarget(self, w: QWidget) -> None:
        self._target = w

    def trigger(self) -> QWidget:
        return self._trigger

    def setTrigger(self, w: QWidget) -> None:
        self._trigger = w

    def _onTriggerPressed(self, event: QMouseEvent) -> None:
        self.pressed.emit()
        self._is_dragging = True
        self._drag_start_pos = event.globalPos()
        self._widget_start_pos = self._target.pos()
        self._target.raise_()
        SiQuickEffect.applyDropShadowOn(self._target, (0, 0, 0, 127), blur_radius=32)

    def _onTriggerMouseMoved(self, event: QMouseEvent) -> None:
        delta = event.globalPos() - self._drag_start_pos
        new_pos = self._widget_start_pos + delta
        self.dragged.emit(new_pos)
        ani: SiExpAnimationRefactor = self._item.animation("geometry")
        ani.setEndValue(QRect(new_pos, self._target.size()))
        ani.start()

    def _onTriggerReleased(self, _) -> None:
        self.dropped.emit()
        self._is_dragging = False
        self._target.setGraphicsEffect(None)
        self._target.updateGeometry()

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if obj != self._trigger:
            return super().eventFilter(obj, event)

        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                self._onTriggerPressed(event)
                return False

        elif event.type() == QEvent.MouseMove:
            if self._is_dragging and (event.buttons() & Qt.LeftButton):
                self._onTriggerMouseMoved(event)
                return False

        elif event.type() == QEvent.MouseButtonRelease:
            if event.button() == Qt.LeftButton:
                self._onTriggerReleased(event)
                return False

        return super().eventFilter(obj, event)

    def isDragging(self) -> bool:
        return self._is_dragging


class DraggableWidgetItem(QWidgetItem):

    class Property:
        Geometry = "geometry"

    def __init__(self, parent: T_WidgetParent, trigger: T_WidgetParent) -> None:
        super().__init__(parent)

        self._event_filter = DraggingEventFilter(self, parent, trigger)
        self._trigger = trigger
        self._trigger.installEventFilter(self._event_filter)

        self.ani_geometry = SiExpAnimationRefactor(parent, self.Property.Geometry)
        self.ani_geometry.init(1/4, 0.2, self.geometry(), self.geometry())

    def trigger(self) -> QWidget:
        return self._trigger

    def setTrigger(self, w: QWidget) -> None:
        self._trigger.removeEventFilter(self._event_filter)
        self._event_filter.setTrigger(w)
        self._trigger = w
        self._trigger.installEventFilter(self._event_filter)

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

    def isDragging(self) -> bool:
        return self._event_filter.isDragging()


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

    def insertItem(self, a0: QLayoutItem, index: int) -> None:
        self._items.insert(index, a0)
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
        column_n = max((self.geometry().width() + self._column_spacing) // width_unit, 1)
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

        rect = self.geometry()

        width_unit = self._column_width + self._column_spacing
        column_n = max((rect.width() + self._column_spacing) // width_unit, 1)
        column_height = [0 for _ in range(column_n)]

        for i in range(self.count()):
            item = self.itemAt(i)
            column_index = i % column_n

            pos = QPoint(width_unit * column_index, column_height[column_index]) + rect.topLeft()
            size = self._getItemSize(item)
            new_rect = QRect(pos, size)

            column_height[column_index] += size.height() + self._line_spacing
            self._max_column_height_cache = max(column_height)

            if isinstance(item, DraggableWidgetItem) and item.isDragging():
                continue

            item.setGeometry(new_rect)


class SiFlowLayout(QLayout):
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self._column_spacing = 8
        self._line_spacing = 8

        self._cache_max_line_width = 0
        self._cache_height = 0
        self._items = []

    def addItem(self, a0: QLayoutItem) -> None:
        self._items.append(a0)
        self.invalidate()

    def insertItem(self, a0: QLayoutItem, index: int) -> None:
        self._items.insert(index, a0)
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
        width = self._cache_max_line_width - self._column_spacing
        height = self._cache_height - self._line_spacing
        return QSize(width, height)

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

    def setGeometry(self, geo):
        super().setGeometry(geo)

        rect = self.geometry()

        max_line_width = 0
        max_height_in_line = 0
        current_line_width = 0
        current_height = 0

        for i in range(self.count()):
            item = self.itemAt(i)
            size = item.geometry().size()

            if isinstance(item, (AnimatedWidgetItem, DraggableWidgetItem)):
                ani = item.animation(item.Property.Geometry)
                if ani.state() == ani.State.Running and ani.currentValue().size() == size:
                    size = ani.endValue().size()

            if current_line_width + size.width() > rect.width():
                current_height += max_height_in_line + self._line_spacing
                current_line_width = 0
                max_height_in_line = 0

            max_height_in_line = max(max_height_in_line, size.height())
            pos = QPoint(current_line_width, current_height) + rect.topLeft()
            new_rect = QRect(pos, size)

            current_line_width += size.width() + self._column_spacing
            max_line_width = max(max_line_width, current_line_width)

            if isinstance(item, DraggableWidgetItem) and item.isDragging():
                continue

            item.setGeometry(new_rect)

        self._cache_max_line_width = max_line_width
        self._cache_height = current_height + max_height_in_line + self._line_spacing
