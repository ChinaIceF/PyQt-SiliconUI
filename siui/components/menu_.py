from __future__ import annotations

from PyQt5.QtCore import QEvent, QMargins, QObject, QPoint, QRect, QRectF, QSize, Qt, QTimer, pyqtProperty, pyqtSignal
from PyQt5.QtGui import QColor, QIcon, QKeySequence, QPainter, QPainterPath, QTextOption
from PyQt5.QtWidgets import QAction, QActionGroup, QApplication, QHBoxLayout, QLabel, QMenu, QSpacerItem, QWidget

from siui.components.button import SiTransparentButton
from siui.components.container import SiDenseContainer
from siui.components.label import SiRoundPixmapWidget
from siui.components.slider_ import SiScrollAreaRefactor
from siui.core import SiQuickEffect, createPainter
from siui.core.animation import SiExpAnimationRefactor
from siui.core.event_filter import DebugEventFilter, WidgetTooltipAcceptEventFilter
from siui.core.globals import SiGlobal
from siui.gui import SiFont
from siui.typing import T_WidgetParent


class CheckedIndicatorStyleData:
    independent_indicator_color = QColor("#918497")
    exclusive_indicator_color = QColor("#918497")


class ActionItemsWidgetStyleData:
    hover_overlay_color_idle: QColor = QColor("#00EDE1F4")
    hover_overlay_color_hovered: QColor = QColor("#20EDE1F4")
    label_text_color_enabled: QColor = QColor("#D1CBD4")
    label_text_color_disabled: QColor = QColor("#50D1CBD4")
    shortcut_text_color: QColor = QColor("#918497")
    shortcut_background_color: QColor = QColor("#201d23")
    checked_indicator_color_unchecked = QColor("#00D087DF")
    checked_indicator_color_checked = QColor("#D087DF")


class SeperatorItemsWidgetStyleData:
    seperator_color: QColor = QColor("#6a5e73")


class SectionItemsWidgetStyleData:
    seperator_color: QColor = QColor("#6a5e73")
    text_color: QColor = QColor("#918497")


class MenuStyleData:
    background_color: QColor = QColor("#322e37")
    border_color: QColor = QColor("#3c3841")


class ActionItemWidgetCheckedIndicator(QWidget):
    def __init__(self, action: QAction, parent=None):
        super().__init__(parent)

        self._action = action
        self._margins_independent = QMargins(12, 12, 12, 12)
        self._margins_exclusive = QMargins(13, 13, 13, 13)
        self._policy = self._actionExclusivePolicy()
        self._is_checked = self._action.isChecked()

        self.style_data = CheckedIndicatorStyleData()

    def _actionExclusivePolicy(self) -> QActionGroup.ExclusionPolicy:
        action_group = self._action.actionGroup()

        if action_group is not None:
            return action_group.exclusionPolicy()

        return QActionGroup.ExclusionPolicy.None_

    def updateAction(self) -> None:
        self._policy = self._actionExclusivePolicy()
        self._is_checked = self._action.isChecked()
        self.update()

    def _drawIndependentIndicator(self, painter: QPainter, rect: QRect) -> None:
        if not self._is_checked:
            return

        top_left = rect.topLeft()
        point1 = QPoint(0, 4) + top_left
        point2 = QPoint(4, 8) + top_left
        point3 = QPoint(12, 0) + top_left

        painter.setPen(self.style_data.independent_indicator_color)
        painter.setBrush(Qt.NoBrush)
        painter.drawLine(point1, point2)
        painter.drawLine(point2, point3)

    def _drawExclusiveIndicator(self, painter: QPainter, rect: QRect) -> None:
        if not self._is_checked:
            return

        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), 3, 3)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.style_data.exclusive_indicator_color)
        painter.drawPath(path)

    def paintEvent(self, a0):
        rect = self.rect()
        independent_rect = rect.marginsRemoved(self._margins_independent)
        exclusive_rect = rect.marginsRemoved(self._margins_exclusive)

        with createPainter(self) as painter:
            if self._policy == QActionGroup.ExclusionPolicy.None_:
                self._drawIndependentIndicator(painter, independent_rect)

            else:
                self._drawExclusiveIndicator(painter, exclusive_rect)


class SiMenuItem(QObject):
    class Type:
        Action = "Action"
        SubMenu = "SubMenu"
        Separator = "Separator"
        Section = "Section"
        Custom = "Custom"

    def __init__(self, parent, type_, action: QAction, cls=None):
        super().__init__(parent)

        self.type = type_
        self.action = action
        self.cls = cls


class SiMenuItemWidget(QWidget):
    """所有菜单项 widget 的基类"""
    reachedEnd = pyqtSignal()
    peeked = pyqtSignal(QAction)

    def __init__(self, action: QAction | None, parent=None):
        super().__init__(parent)
        self._action = action

    def action(self) -> QAction | None:
        return self._action

    def peek(self) -> None:
        self.peeked.emit(self._action)

    def reachEnd(self) -> None:
        self.reachedEnd.emit()

    def setCheckedIndicatorVisible(self, state: bool) -> None:
        pass

    def setIconVisible(self, state: bool) -> None:
        pass

    def setShortcutVisible(self, state: bool) -> None:
        pass

    def setSubmenuIndicatorVisible(self, state: bool) -> None:
        pass


class ActionItemWidget(SiMenuItemWidget):
    def __init__(self, action: QAction, parent=None):
        super().__init__(action, parent)

        self.setFixedHeight(32)

        self._action = action
        self.style_data = ActionItemsWidgetStyleData()

        self._checked_indicator = ActionItemWidgetCheckedIndicator(action, self)
        self._icon_widget = SiRoundPixmapWidget(self)
        self._name_label = QLabel(self)
        self._shortcut_widget = QLabel(self)
        self._button = SiTransparentButton(self)

        self._applyAction(action)
        self._initWidgets()
        self._initLayout()
        self._initTooltipAcceptFilter()

        self._button.clicked.connect(self._onButtonClicked)

    def _initWidgets(self) -> None:
        sd = self.style_data

        self._checked_indicator.setFixedSize(32, 32)

        self._shortcut_widget.setStyleSheet(
            f"color: {sd.shortcut_text_color.name()};"
            f"background-color: {sd.shortcut_background_color.name()};"
            "padding: 1px 6px 1px 6px;"
            "margin: 1px 8px 0px 8px;"
            "border-radius: 4px;"
        )

        self._icon_widget.setPixmap(self._action.icon().pixmap(64, 64))
        self._icon_widget.setFixedSize(32, 32)
        self._icon_widget.setVisualSize(QSize(18, 18))
        self._icon_widget.setVisualSizeEnabled(True)

        self._name_label.setFont(SiFont.getFont(size=14))
        self._name_label.setText(self._action.text())
        self._name_label.setAlignment(Qt.AlignVCenter)
        self._name_label.setFixedHeight(32)
        self._name_label.setMinimumWidth(32)
        self._name_label.setStyleSheet(f"""
        QLabel {{
            margin: 0px 8px 1px 0px;
            color: {sd.label_text_color_enabled.name(QColor.HexArgb)};
        }}
        QLabel:disabled {{
            margin: 0px 8px 1px 0px;
            color: {sd.label_text_color_disabled.name(QColor.HexArgb)};
        }}
        """)

        self._shortcut_widget.setFont(SiFont.getFont(size=9))
        self._shortcut_widget.setAlignment(Qt.AlignCenter)
        self._shortcut_widget.setFixedHeight(18)

        self._button.setBorderRadius(6)

    def _initLayout(self) -> None:
        layout = QHBoxLayout(self)
        layout.addWidget(self._checked_indicator)
        layout.addSpacerItem(QSpacerItem(4, 32))
        layout.addWidget(self._icon_widget)
        layout.addSpacerItem(QSpacerItem(4, 32))
        layout.addWidget(self._name_label)
        layout.addStretch()
        layout.addWidget(self._shortcut_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setLayout(layout)

    def _initTooltipAcceptFilter(self) -> None:
        self._tooltip_accept_filter = WidgetTooltipAcceptEventFilter(self)
        self.installEventFilter(self._tooltip_accept_filter)

    def _applyAction(self, action: QAction) -> None:
        self.addAction(action)
        self._updateFromAction(action)
        action.changed.connect(lambda: self._updateFromAction(action))

    def _updateFromAction(self, action: QAction) -> None:
        self.setText(action.text())
        self.setIcon(action.icon())
        self.setToolTip(action.toolTip())
        self.setShortcut(action.shortcut())
        self.setEnabled(action.isEnabled())

        self._checked_indicator.updateAction()

    def _onButtonClicked(self) -> None:
        self._action.trigger()
        self._button.leave()
        self.peek()
        self.reachEnd()

    def setText(self, text: str) -> None:
        self._name_label.setText(text)

    def setIcon(self, icon: QIcon) -> None:
        self._icon_widget.setPixmap(icon.pixmap(64, 64))

    def setShortcut(self, shortcut: QKeySequence) -> None:
        string = shortcut.toString()
        self._shortcut_widget.setText(string)

    def setCheckedIndicatorVisible(self, state: bool) -> None:
        self._checked_indicator.setVisible(state)

    def setIconVisible(self, state: bool) -> None:
        self._icon_widget.setVisible(state)

    def setShortcutVisible(self, state: bool) -> None:
        self._shortcut_widget.setVisible(state and not self._action.shortcut().isEmpty())

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self._button.resize(a0.size())

    def enterEvent(self, a0):
        super().enterEvent(a0)
        self._action.hover()


class SubmenuItemWidget(SiMenuItemWidget):
    def __init__(self, action: QAction, parent=None):
        super().__init__(action, parent)

        self.setFixedHeight(32)

        self._action = action
        self.style_data = ActionItemsWidgetStyleData()

        self._peeking_timer = QTimer(self)

        self._checked_indicator = ActionItemWidgetCheckedIndicator(action, self)
        self._icon_widget = SiRoundPixmapWidget(self)
        self._name_label = QLabel(self)
        self._shortcut_widget = QLabel(self)
        self._submenu_indicator = SiRoundPixmapWidget(self)
        self._button = SiTransparentButton(self)

        self._applyAction(action)
        self._initWidgets()
        self._initLayout()
        self._initTimer()
        self._initTooltipAcceptFilter()

        self._button.clicked.connect(self._onButtonClicked)

    def _initWidgets(self) -> None:
        sd = self.style_data

        self._checked_indicator.setFixedSize(32, 32)

        self._shortcut_widget.setStyleSheet(
            f"color: {sd.shortcut_text_color.name()};"
            f"background-color: {sd.shortcut_background_color.name()};"
            "padding: 1px 6px 1px 6px;"
            "margin: 1px 8px 0px 0px;"
            "border-radius: 4px;"
        )

        self._icon_widget.setPixmap(self._action.icon().pixmap(64, 64))
        self._icon_widget.setFixedSize(32, 32)
        self._icon_widget.setVisualSize(QSize(18, 18))
        self._icon_widget.setVisualSizeEnabled(True)

        self._name_label.setFont(SiFont.getFont(size=14))
        self._name_label.setText(self._action.text())
        self._name_label.setAlignment(Qt.AlignVCenter)
        self._name_label.setFixedHeight(32)
        self._name_label.setMinimumWidth(32)
        self._name_label.setStyleSheet(f"""
        QLabel {{
            margin: 0px 8px 1px 0px;
            color: {sd.label_text_color_enabled.name(QColor.HexArgb)};
        }}
        QLabel:disabled {{
            margin: 0px 8px 1px 0px;
            color: {sd.label_text_color_disabled.name(QColor.HexArgb)};
        }}
        """)

        self._shortcut_widget.setFont(SiFont.getFont(size=9))
        self._shortcut_widget.setAlignment(Qt.AlignCenter)
        self._shortcut_widget.setFixedHeight(18)

        self._submenu_indicator.setPixmap(SiGlobal.siui.iconpack.toPixmap("ic_fluent_chevron_right_filled"))
        self._submenu_indicator.setFixedSize(16, 16)
        self._submenu_indicator.setVisualSize(QSize(16, 16))
        self._submenu_indicator.setContentsMargins(16, 8, 16, 8)
        self._submenu_indicator.setVisualSizeEnabled(True)

    def _initLayout(self) -> None:
        layout = QHBoxLayout(self)
        layout.addWidget(self._checked_indicator)
        layout.addWidget(self._icon_widget)
        layout.addSpacerItem(QSpacerItem(4, 32))
        layout.addWidget(self._name_label)
        layout.addStretch()
        layout.addWidget(self._shortcut_widget)
        layout.addWidget(self._submenu_indicator)
        layout.setContentsMargins(4, 0, 8, 0)
        layout.setSpacing(0)

        self.setLayout(layout)

    def _initTimer(self) -> None:
        self._peeking_timer.setSingleShot(True)
        self._peeking_timer.setInterval(400)
        self._peeking_timer.timeout.connect(self._onPeekingTimerTimeout)

    def _initTooltipAcceptFilter(self) -> None:
        self._tooltip_accept_filter = WidgetTooltipAcceptEventFilter(self)
        self.installEventFilter(self._tooltip_accept_filter)

    def _applyAction(self, action: QAction) -> None:
        self.addAction(action)
        self._updateFromAction(action)
        action.changed.connect(lambda: self._updateFromAction(action))

    def _updateFromAction(self, action: QAction) -> None:
        self.setText(action.text())
        self.setIcon(action.icon())
        self.setToolTip(action.toolTip())
        self.setShortcut(action.shortcut())
        self.setEnabled(action.isEnabled())

        self._checked_indicator.updateAction()

    def _showSubmenu(self) -> None:
        pos = self.mapToGlobal(self.geometry().topRight() - self.geometry().topLeft())
        menu = self._action.menu()
        menu.popup(pos)

    def _onButtonClicked(self) -> None:
        self.peek()
        self._peeking_timer.stop()
        self._showSubmenu()
        self._button.leave()

    def _onPeekingTimerTimeout(self) -> None:
        self.peek()
        self._showSubmenu()

    def setText(self, text: str) -> None:
        self._name_label.setText(text)

    def setIcon(self, icon: QIcon) -> None:
        self._icon_widget.setPixmap(icon.pixmap(64, 64))

    def setShortcut(self, shortcut: QKeySequence) -> None:
        string = shortcut.toString()
        self._shortcut_widget.setText(string)

    def setCheckedIndicatorVisible(self, state: bool) -> None:
        self._checked_indicator.setVisible(state)

    def setIconVisible(self, state: bool) -> None:
        self._icon_widget.setVisible(state)

    def setShortcutVisible(self, state: bool) -> None:
        self._shortcut_widget.setVisible(state and not self._action.shortcut().isEmpty())

    def setSubmenuIndicatorVisible(self, state: bool) -> None:
        self._submenu_indicator.setVisible(state)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self._button.resize(a0.size())

    def enterEvent(self, a0):
        super().enterEvent(a0)
        self._action.hover()
        self._peeking_timer.start()

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        self._peeking_timer.stop()


class SeparatorItemWidget(SiMenuItemWidget):
    def __init__(self, action: QAction | None, parent=None):
        super().__init__(action, parent)

        self.setFixedHeight(1)
        self.style_data = SeperatorItemsWidgetStyleData()
        self._margin = QMargins(4, 0, 4, 0)

    def _drawSeparationLine(self, painter: QPainter, rect: QRect) -> None:
        painter.setPen(self.style_data.seperator_color)
        painter.setBrush(Qt.NoBrush)
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())

    def paintEvent(self, a0):
        rect = self.rect()
        shrunk_rect = rect.marginsRemoved(self._margin)

        with createPainter(self) as painter:
            self._drawSeparationLine(painter, shrunk_rect)


class SectionItemWidget(SiMenuItemWidget):
    def __init__(self, action: QAction, parent=None):
        super().__init__(action, parent)

        self.setFixedHeight(32)
        self.setFont(SiFont.getFont(size=12))

        self.style_data = SectionItemsWidgetStyleData()

        self._action = action
        self._margin = QMargins(4, 4, 4, 4)

    def reachEnd(self) -> None:
        pass

    def peek(self) -> None:
        pass

    def _drawSeparationLine(self, painter: QPainter, rect: QRect) -> None:
        painter.setPen(self.style_data.seperator_color)
        painter.setBrush(Qt.NoBrush)
        painter.drawLine(rect.bottomLeft(), rect.bottomRight())

    def _drawSectionText(self, painter: QPainter, rect: QRect) -> None:
        text = self._action.text()
        option = QTextOption()
        option.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        painter.setFont(self.font())
        painter.setPen(self.style_data.text_color)
        painter.drawText(QRectF(rect), text, option)

    def paintEvent(self, a0):
        rect = self.rect()
        shrunk_rect = rect.marginsRemoved(self._margin)

        with createPainter(self) as painter:
            self._drawSectionText(painter, shrunk_rect)
            self._drawSeparationLine(painter, shrunk_rect)


class SiMenuItemWidgetFactory:
    @staticmethod
    def create(item: SiMenuItem, parent=None) -> SiMenuItemWidget:
        if item.type == SiMenuItem.Type.Action:
            return ActionItemWidget(item.action, parent)

        elif item.type == SiMenuItem.Type.Separator:
            return SeparatorItemWidget(item.action, parent)

        elif item.type == SiMenuItem.Type.SubMenu:
            return SubmenuItemWidget(item.action, parent)

        elif item.type == SiMenuItem.Type.Section:
            return SectionItemWidget(item.action, parent)

        elif item.type == SiMenuItem.Type.Custom:
            action, widget_cls = item.action, item.cls
            widget = widget_cls(action, parent)
            widget.setParent(parent)

            if not isinstance(widget, SiMenuItemWidget):
                raise TypeError(f"Custom widgets must inherit from SiMenuItemWidget, encountered {type(widget)}")

            return widget

        else:
            raise ValueError(f"Type {item.type} is not implemented in SiMenuItemWidgetFactory.create")


class SiRoundedMenuActivationFilter(QObject):
    def __init__(self, parent: SiRoundedMenu | None = None):
        super().__init__(parent)
        self.menu = parent

    def eventFilter(self, obj, event):
        event_type = event.type()

        if event_type == QEvent.Show:
            self.menu._clearPeekingAction()  # noqa

        if event_type == QEvent.WindowDeactivate:
            if self.menu.peekingAction() is not None:
                return False
            self.menu._closeMenuTreeUptoActivated()  # noqa

        return False


class SiRoundedMenu(QMenu):
    class Property:
        ViewSize = "viewSize"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.Popup
            | Qt.NoDropShadowWindowHint
            | Qt.Tool
        )

        self._items: list[SiMenuItem] = []
        self._widgets: dict[SiMenuItem, SiMenuItemWidget] = {}
        self._action_to_items: dict[QAction, SiMenuItem] = {}
        self._is_layout_dirty = True
        self._is_mouse_pressed_in_self = False
        self._peeking_action = None

        self.style_data = MenuStyleData()

        self._margins = QMargins(32, 32, 32, 32)
        self._scroll_area_size = QSize(80, 80)

        self._background = QLabel(self)
        self._scroll_area = SiScrollAreaRefactor(self)
        self._container = SiDenseContainer(self._scroll_area, SiDenseContainer.TopToBottom)

        self.ani_scroll_area_size = SiExpAnimationRefactor(self, self.Property.ViewSize)
        self.ani_scroll_area_size.init(1 / 6, 1, self._scroll_area_size, self._scroll_area_size)

        self._initStyle()
        self._initActivationFilter()

    def _initStyle(self) -> None:
        background = self.style_data.background_color.name()
        border = self.style_data.border_color.name()

        self._background.move(self._margins.left(), self._margins.top())
        self._background.setStyleSheet(
            f"background-color: {background};"
            f"border: 1px solid {border};"
            "border-radius: 6px;"
        )

        self._scroll_area.setWidget(self._container)
        self._scroll_area.setViewportMargins(0, 1, -8, 1)
        self._scroll_area.move(self._margins.left(), self._margins.top())
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self._container.layout().setSpacing(4)
        self._container.setContentsMargins(6, 4, 6, 4)
        self._container.layout().removeWidget(self._container.stretchWidget())

    def _initActivationFilter(self) -> None:
        self._activation_filter = SiRoundedMenuActivationFilter(self)
        self.installEventFilter(self._activation_filter)

    def _applyGraphicEffect(self) -> None:
        SiQuickEffect.applyDropShadowOn(self._background, color=(0, 0, 0, 128))

    @pyqtProperty(QSize)
    def viewSize(self):
        return self._scroll_area_size

    @viewSize.setter
    def viewSize(self, value: QSize):
        self._scroll_area_size = value
        self._scroll_area.resize(value)
        self._background.resize(value)

    def _startShowAnimation(self) -> None:
        inner_size = self.size().shrunkBy(self._margins)
        width = inner_size.width()
        height = inner_size.height()

        ani = self.ani_scroll_area_size
        ani.setCurrentValue(QSize(width, int(height * 0.6)))
        ani.setEndValue(QSize(width, height))
        ani.start()

    def _prepareShowAnimation(self) -> None:
        inner_size = self.size().shrunkBy(self._margins)
        width = inner_size.width()
        height = inner_size.height()

        ani = self.ani_scroll_area_size
        ani.stop()
        ani.setCurrentValue(QSize(width, int(height * 0.6)))
        ani.toProperty()

    def _closeMenu(self) -> None:
        self.close()

    def _closeMenuTreeUp(self) -> None:
        widget = self
        while isinstance(widget, SiRoundedMenu):
            widget.close()
            widget = widget.parent()

    def _closeMenuTreeUptoActivated(self) -> None:
        widget = self
        while isinstance(widget, SiRoundedMenu) and not widget.isActiveWindow():
            widget.close()
            widget = widget.parent()

    def _closeMenuTreeDown(self) -> None:
        widget = self
        while isinstance(widget, SiRoundedMenu):
            widget.close()

            action = widget._peeking_action
            if action is None:
                break

            item = widget._action_to_items[action]
            item_widget = widget._widgets[item]
            widget = item_widget.action().menu()

    def _onReachedEnd(self) -> None:
        self._closeMenuTreeUp()

    def _onActionPeeked(self, action: QAction) -> None:
        self.activateWindow()
        self._peeking_action = action

    # region Action related methods

    def _extractActionFromArgs(self, *args) -> QAction | None:
        if len(args) == 1 and isinstance(args[0], QAction):
            return args[0]
        return None

    def _addItem(self, item: SiMenuItem) -> None:
        widget = SiMenuItemWidgetFactory.create(item, self._container)
        widget.reachedEnd.connect(self._closeMenuTreeUp)
        widget.peeked.connect(self._onActionPeeked)

        self._items.append(item)
        self._widgets.update([(item, widget)])
        self._action_to_items.update([(item.action, item)])

        self._is_layout_dirty = True

    def _insertItem(self, before: QAction, item: SiMenuItem) -> None:
        widget = SiMenuItemWidgetFactory.create(item, self._container)
        widget.reachedEnd.connect(self._closeMenuTreeUp)

        before_item = self._action_to_items.get(before)
        before_index = self._items.index(before_item)

        self._items.insert(before_index, item)
        self._widgets.update([(item, widget)])
        self._action_to_items.update([(item.action, item)])

        self._is_layout_dirty = True

    def addAction(self, *args, **kwargs) -> QAction | None:
        new_action = super().addAction(*args, **kwargs)
        action_for_item = new_action if new_action else self._extractActionFromArgs(*args)

        item = SiMenuItem(self, SiMenuItem.Type.Action, action_for_item)
        self._addItem(item)

        return new_action

    def addMenu(self, *args, **kwargs) -> QAction | None:
        new_action = super().addMenu(*args, **kwargs)

        item = SiMenuItem(self, SiMenuItem.Type.SubMenu, new_action)
        self._addItem(item)

        return new_action

    def addSeparator(self) -> QAction | None:
        new_action = super().addSeparator()

        item = SiMenuItem(self, SiMenuItem.Type.Separator, new_action)
        self._addItem(item)

        return new_action

    def addSection(self, *args, **kwargs) -> QAction | None:
        new_action = super().addSection(*args, **kwargs)

        item = SiMenuItem(self, SiMenuItem.Type.Section, new_action)
        self._addItem(item)

        return new_action

    def addCustomWidget(self, action: QAction, widget_cls: type[SiMenuItemWidget]) -> QAction | None:
        new_action = super().addAction(action)

        item = SiMenuItem(self, SiMenuItem.Type.Custom, action, widget_cls)
        self._addItem(item)

        return new_action

    def addActions(self, actions: list[QAction]) -> None:
        for action in actions:
            item = SiMenuItem(self, SiMenuItem.Type.Action, action)
            self._addItem(item)

    def insertAction(self, before: QAction, action: QAction) -> None:
        super().insertAction(before, action)

        item = SiMenuItem(self, SiMenuItem.Type.Action, action)
        self._insertItem(before, item)

        return None

    def insertMenu(self, before: QAction, menu: QMenu) -> QAction:
        new_action = super().insertMenu(before, menu)

        item = SiMenuItem(self, SiMenuItem.Type.SubMenu, new_action)
        self._insertItem(before, item)

        return new_action

    def insertSeparator(self, before: QAction) -> QAction:
        new_action = super().insertSeparator(before)

        item = SiMenuItem(self, SiMenuItem.Type.Separator, new_action)
        self._insertItem(before, item)

        return new_action

    def insertSection(self, before: QAction, text: str) -> QAction:
        new_action = super().insertSection(before, text)

        item = SiMenuItem(self, SiMenuItem.Type.Section, new_action)
        self._insertItem(before, item)

        return new_action

    def insertCustomWidget(self, before: QAction, action: QAction,
                           widget_cls: type[SiMenuItemWidget]) -> QAction | None:
        new_action = super().addAction(action)

        item = SiMenuItem(self, SiMenuItem.Type.Custom, action, widget_cls)
        self._insertItem(before, item)

        return new_action

    def insertActions(self, before: QAction, actions: list[QAction]) -> None:
        super().insertActions(before, actions)

        for action in actions:
            item = SiMenuItem(self, SiMenuItem.Type.Action, action)
            self._insertItem(before, item)
            before = action

    def removeAction(self, action: QAction) -> None:
        super().removeAction(action)
        item = self._action_to_items.get(action)
        widget = self._widgets.get(item)

        self._container.layout().removeWidget(widget)
        widget.reachedEnd.disconnect()
        widget.deleteLater()

        self._items.remove(item)
        self._widgets.pop(item)
        self._action_to_items.pop(action)

        return None

    def clear(self) -> None:
        super().clear()
        for item in self._items:
            widget = self._widgets.get(item)

            self._container.layout().removeWidget(widget)
            widget.reachedEnd.disconnect()
            widget.deleteLater()

        self._widgets.clear()
        self._items.clear()
        self._action_to_items.clear()

    # endregion

    def container(self) -> QWidget:
        return self._container

    def _clearPeekingAction(self) -> None:
        self._peeking_action = None

    def peekingAction(self) -> QAction | None:
        return self._peeking_action

    def isSubmenu(self) -> bool:
        return isinstance(self.parent(), SiRoundedMenu)

    def sizeHint(self):
        screen_rect = QApplication.desktop().availableGeometry()
        container_size = self._container.size()
        expanded_rect = container_size.grownBy(self._margins)

        width = expanded_rect.width()
        height = min(expanded_rect.height() + 2, screen_rect.height(), self.maximumHeight())

        return QSize(width, height)

    def _updateComponentsVisibility(self) -> None:
        item_in_section = []
        has_checkable = False
        has_icon = False
        has_shortcut = False
        has_submenu = False

        for item in self._items:
            if not item_in_section:
                has_checkable = False
                has_icon = False
                has_shortcut = False
                has_submenu = False

            if item.type in [item.Type.Separator, item.Type.Section]:
                for item_ in item_in_section:
                    widget = self._widgets.get(item_)
                    widget.setCheckedIndicatorVisible(has_checkable)
                    widget.setIconVisible(has_icon)
                    widget.setShortcutVisible(has_shortcut)
                    widget.setSubmenuIndicatorVisible(has_submenu)

                item_in_section = []
                continue

            action: QAction = item.action
            has_checkable |= action.isCheckable()
            has_icon |= not action.icon().isNull()
            has_shortcut |= not action.shortcut().isEmpty()
            has_submenu |= action.menu() is not None

            item_in_section.append(item)

        for item_ in item_in_section:
            widget = self._widgets.get(item_)
            widget.setCheckedIndicatorVisible(has_checkable)
            widget.setIconVisible(has_icon)
            widget.setShortcutVisible(has_shortcut)
            widget.setSubmenuIndicatorVisible(has_submenu)

    def _refreshLayoutOrder(self) -> None:
        layout = self._container.layout()
        current_widgets = [layout.itemAt(i).widget() for i in range(layout.count())]
        desired_widgets = [self._widgets[item] for item in self._items if item in self._widgets]

        for i, widget in enumerate(desired_widgets):
            if i >= len(current_widgets) or current_widgets[i] is not widget:
                layout.removeWidget(widget)
                layout.insertWidget(i, widget)

    def _prepareToPopup(self) -> None:
        self._clearPeekingAction()
        self._updateComponentsVisibility()

        if self._is_layout_dirty:
            self._refreshLayoutOrder()
            self._is_layout_dirty = False

        self._container.adjustSize()

    def popup(self, pos: QPoint, action: QAction | None = None) -> None:
        self._prepareToPopup()

        new_pos = pos - self._scroll_area.pos()
        super().popup(new_pos, action)
        self.activateWindow()

    def refreshLayout(self) -> None:
        """立即更新布局"""
        self._refreshLayoutOrder()
        self._container.adjustSize()
        self.adjustSize()

    def paintEvent(self, a0):
        pass

    def showEvent(self, a0):
        super().showEvent(a0)

        self._applyGraphicEffect()
        self._startShowAnimation()

    def hideEvent(self, a0):
        super().hideEvent(a0)
        self._prepareShowAnimation()

    def mouseMoveEvent(self, a0):
        a0.ignore()

    def mousePressEvent(self, a0):
        inner_rect = self.rect().marginsRemoved(self._margins)
        pos = a0.pos()
        self._is_mouse_pressed_in_self = inner_rect.contains(pos)

    def mouseReleaseEvent(self, a0):
        inner_rect = self.rect().marginsRemoved(self._margins)
        pos = a0.pos()
        if not inner_rect.contains(pos) and not self._is_mouse_pressed_in_self:
            self.close()

        self._is_mouse_pressed_in_self = False

    def resizeEvent(self, a0):
        super().resizeEvent(a0)



