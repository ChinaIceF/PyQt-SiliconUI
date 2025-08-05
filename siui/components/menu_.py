from __future__ import annotations

from PyQt5.QtCore import QEvent, QMargins, QObject, QPoint, QRect, QRectF, QSize, Qt, pyqtProperty, pyqtSignal
from PyQt5.QtGui import QColor, QCursor, QIcon, QKeySequence, QPainter, QTextOption
from PyQt5.QtWidgets import QAction, QHBoxLayout, QLabel, QMenu, QWidget

from siui.components.button import SiTransparentButton
from siui.components.container import SiDenseContainer
from siui.components.label import SiAnimatedColorWidget, SiRoundPixmapWidget
from siui.components.slider_ import SiScrollAreaRefactor
from siui.core import SiQuickEffect, createPainter, hideToolTip, showToolTip
from siui.core.animation import SiExpAnimationRefactor
from siui.core.event_filter import TooltipManager
from siui.core.globals import SiGlobal, raiseToolTipWindow, toolTipWindow
from siui.gui import SiFont
from siui.typing import T_WidgetParent


class ActionItemsWidgetStyleData:
    hover_overlay_color_idle: QColor = QColor("#00EDE1F4")
    hover_overlay_color_hovered: QColor = QColor("#20EDE1F4")
    label_text_color_enabled: QColor = QColor("#D1CBD4")
    label_text_color_disabled: QColor = QColor("#50D1CBD4")
    shortcut_text_color: QColor = QColor("#918497")
    shortcut_background_color: QColor = QColor("#201d23")
    checked_indicator_color_unchecked = QColor("#00C88CD4")
    checked_indicator_color_checked = QColor("#C88CD4")


class SeperatorItemsWidgetStyleData:
    seperator_color: QColor = QColor("#6a5e73")


class SectionItemsWidgetStyleData:
    seperator_color: QColor = QColor("#6a5e73")
    text_color: QColor = QColor("#918497")


class MenuStyleData:
    background_color: QColor = QColor("#322e37")
    border_color: QColor = QColor("#3c3841")


class SiMenuItem(QObject):
    class Type:
        Action = "Action"
        SubMenu = "SubMenu"
        Separator = "Separator"
        Section = "Section"
        Custom = "Custom"

    def __init__(self, parent, type_, data):
        super().__init__(parent)

        self.type = type_
        self.data = data


class SiMenuItemWidget(QWidget):
    """所有菜单项 widget 的基类"""
    reachedEnd = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def _emitReachedEnd(self):
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
        super().__init__(parent)

        self.setFixedHeight(32)

        self._action = action
        self.style_data = ActionItemsWidgetStyleData()

        self._checked_indicator = QLabel(self)
        self._icon_widget = SiRoundPixmapWidget(self)
        self._name_label = QLabel(self)
        self._shortcut_widget = QLabel(self)
        self._button = SiTransparentButton(self)

        self._applyAction(action)
        self._initWidgets()
        self._initLayout()
        self._initToolTipManager()

        self._button.clicked.connect(self._onButtonClicked)

    def _initWidgets(self) -> None:
        sd = self.style_data

        self._checked_indicator.setFixedSize(5, 5)

        self._shortcut_widget.setStyleSheet(
            f"color: {sd.shortcut_text_color.name()};"
            f"background-color: {sd.shortcut_background_color.name()};"
            "padding: 1px 6px 1px 6px;"
            "margin: 1px 8px 0px 0px;"
            "border-radius: 4px;"
        )

        self._icon_widget.setPixmap(self._action.icon().pixmap(64, 64))
        self._icon_widget.setFixedSize(20, 20)
        self._icon_widget.setVisualSize(QSize(18, 18))
        self._icon_widget.setVisualSizeEnabled(True)
        self._icon_widget.setStyleSheet(
            "margin: 0px 0px 0px 6px"
        )

        self._name_label.setFont(SiFont.getFont(size=14))
        self._name_label.setText(self._action.text())
        self._name_label.setAlignment(Qt.AlignVCenter)
        self._name_label.setFixedHeight(32)
        self._name_label.setMinimumWidth(32)
        self._name_label.setStyleSheet(f"""
        QLabel {{
            padding: 0px 2px 0px 2px;
            margin: 0px 8px 0px 6px;
            color: {sd.label_text_color_enabled.name(QColor.HexArgb)};
        }}
        QLabel:disabled {{
            padding: 0px 2px 0px 2px;
            margin: 0px 8px 0px 6px;
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
        layout.addWidget(self._icon_widget)
        layout.addWidget(self._name_label)
        layout.addStretch()
        layout.addWidget(self._shortcut_widget)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(0)

        self.setLayout(layout)

    def _initToolTipManager(self) -> None:
        self._tooltip_manager = TooltipManager(toolTipWindow())
        self.installEventFilter(self._tooltip_manager)

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
        self.setChecked(action.isChecked())

    def _onButtonClicked(self) -> None:
        self._action.trigger()
        self._action.menuRole()
        self._emitReachedEnd()

    def setText(self, text: str) -> None:
        self._name_label.setText(text)

    def setIcon(self, icon: QIcon) -> None:
        self._icon_widget.setPixmap(icon.pixmap(64, 64))

    def setChecked(self, state: bool) -> None:
        if state:
            self._checked_indicator.setStyleSheet(
                "border-radius: 2px;"
                f"background-color: {self.style_data.checked_indicator_color_checked.name(QColor.HexArgb)}"
            )
        else:
            self._checked_indicator.setStyleSheet(
                "border-radius: 2px;"
                f"background-color: {self.style_data.checked_indicator_color_unchecked.name(QColor.HexArgb)}"
            )

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
        super().__init__(parent)

        self.setFixedHeight(32)

        self._action = action
        self.style_data = ActionItemsWidgetStyleData()

        self._checked_indicator = QLabel(self)
        self._icon_widget = SiRoundPixmapWidget(self)
        self._name_label = QLabel(self)
        self._shortcut_widget = QLabel(self)
        self._submenu_indicator = SiRoundPixmapWidget(self)
        self._button = SiTransparentButton(self)

        self._applyAction(action)
        self._initWidgets()
        self._initLayout()
        self._initToolTipManager()

        self._button.clicked.connect(self._onButtonClicked)

    def _initWidgets(self) -> None:
        sd = self.style_data

        self._checked_indicator.setFixedSize(5, 5)

        self._shortcut_widget.setStyleSheet(
            f"color: {sd.shortcut_text_color.name()};"
            f"background-color: {sd.shortcut_background_color.name()};"
            "padding: 1px 6px 1px 6px;"
            "margin: 1px 8px 0px 0px;"
            "border-radius: 4px;"
        )

        self._icon_widget.setPixmap(self._action.icon().pixmap(64, 64))
        self._icon_widget.setFixedSize(20, 20)
        self._icon_widget.setVisualSize(QSize(18, 18))
        self._icon_widget.setVisualSizeEnabled(True)
        self._icon_widget.setStyleSheet(
            "margin: 0px 0px 0px 6px"
        )

        self._name_label.setFont(SiFont.getFont(size=14))
        self._name_label.setText(self._action.text())
        self._name_label.setAlignment(Qt.AlignVCenter)
        self._name_label.setFixedHeight(32)
        self._name_label.setMinimumWidth(32)
        self._name_label.setStyleSheet(f"""
        QLabel {{
            padding: 0px 2px 0px 2px;
            margin: 0px 8px 0px 6px;
            color: {sd.label_text_color_enabled.name(QColor.HexArgb)};
        }}
        QLabel:disabled {{
            padding: 0px 2px 0px 2px;
            margin: 0px 8px 0px 6px;
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
        layout.addWidget(self._name_label)
        layout.addStretch()
        layout.addWidget(self._shortcut_widget)
        layout.addWidget(self._submenu_indicator)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(0)

        self.setLayout(layout)

    def _initToolTipManager(self) -> None:
        self._tooltip_manager = TooltipManager(toolTipWindow())
        self.installEventFilter(self._tooltip_manager)

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
        self.setChecked(action.isChecked())

    def _showSubmenu(self) -> None:
        pos = self.mapToGlobal(self.geometry().topRight() - self.geometry().topLeft())
        menu = self._action.menu()
        menu.popup(pos)

    def _onButtonClicked(self) -> None:
        self._action.trigger()
        self._action.menuRole()
        self._showSubmenu()

    def setText(self, text: str) -> None:
        self._name_label.setText(text)

    def setIcon(self, icon: QIcon) -> None:
        self._icon_widget.setPixmap(icon.pixmap(64, 64))

    def setChecked(self, state: bool) -> None:
        if state:
            self._checked_indicator.setStyleSheet(
                "border-radius: 2px;"
                f"background-color: {self.style_data.checked_indicator_color_checked.name(QColor.HexArgb)}"
            )
        else:
            self._checked_indicator.setStyleSheet(
                "border-radius: 2px;"
                f"background-color: {self.style_data.checked_indicator_color_unchecked.name(QColor.HexArgb)}"
            )

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


class SeparatorItemWidget(SiMenuItemWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

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
        super().__init__(parent)

        self.setFixedHeight(32)
        self.setFont(SiFont.getFont(size=12))

        self.style_data = SectionItemsWidgetStyleData()

        self._action = action
        self._margin = QMargins(4, 4, 4, 4)

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
            return ActionItemWidget(item.data, parent)

        elif item.type == SiMenuItem.Type.Separator:
            return SeparatorItemWidget(parent)

        elif item.type == SiMenuItem.Type.SubMenu:
            return SubmenuItemWidget(item.data, parent)

        elif item.type == SiMenuItem.Type.Section:
            return SectionItemWidget(item.data, parent)

        elif item.type == SiMenuItem.Type.Custom:
            widget = item.data.parentWidget()
            if not isinstance(widget, SiMenuItemWidget):
                raise TypeError(f"Custom widgets must inherit from SiMenuItemWidget, encountered {type(widget)}")

            widget.setParent(parent)
            return widget

        else:
            raise ValueError(f"Type {item.type} is not implemented in SiMenuItemWidgetFactory.create")


class SiMenu(QMenu):
    class Property:
        ViewSize = "viewSize"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.setMouseTracking(True)

        self._items: list[SiMenuItem] = []
        self._widgets: dict[SiMenuItem, QWidget] = {}
        self._action_to_items: dict[QAction, SiMenuItem] = {}
        self._is_layout_dirty = True
        self._is_mouse_pressed_in_self = False

        self.style_data = MenuStyleData()

        self.setMaximumHeight(400)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.Popup
            | Qt.NoDropShadowWindowHint
        )

        self._margins = QMargins(32, 32, 32, 32)
        self._scroll_area_size = QSize(80, 80)

        self._background = QLabel(self)
        self._scroll_area = SiScrollAreaRefactor(self)
        self._container = SiDenseContainer(self._scroll_area, SiDenseContainer.TopToBottom)

        self.ani_scroll_area_size = SiExpAnimationRefactor(self, self.Property.ViewSize)
        self.ani_scroll_area_size.init(1 / 6, 1, self._scroll_area_size, self._scroll_area_size)

        self._initStyle()
        self._applyGraphicEffect()

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

    def _applyGraphicEffect(self) -> None:
        SiQuickEffect.applyDropShadowOn(self._background, color=(0, 0, 0, 128))

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

            action: QAction = item.data
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

    @pyqtProperty(QSize)
    def viewSize(self):
        return self._scroll_area_size

    @viewSize.setter
    def viewSize(self, value: QSize):
        self._scroll_area_size = value
        self._scroll_area.resize(value)
        self._background.resize(value)

    # region Action related methods

    def _extractActionFromArgs(self, *args) -> QAction | None:
        if len(args) == 1 and isinstance(args[0], QAction):
            return args[0]
        return None

    def _addItem(self, item: SiMenuItem) -> None:
        widget = SiMenuItemWidgetFactory.create(item, self._container)
        widget.reachedEnd.connect(self._closeMenuTree)

        self._items.append(item)
        self._widgets.update([(item, widget)])
        self._action_to_items.update([(item.data, item)])

        self._is_layout_dirty = True

    def _insertItem(self, before: QAction, item: SiMenuItem) -> None:
        widget = SiMenuItemWidgetFactory.create(item, self._container)
        widget.reachedEnd.connect(self._closeMenuTree)

        before_item = self._action_to_items.get(before)
        before_index = self._items.index(before_item)

        self._items.insert(before_index, item)
        self._widgets.update([(item, widget)])
        self._action_to_items.update([(item.data, item)])

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

    def addCustomWidget(self, widget: SiMenuItemWidget) -> QAction:
        new_action = QAction(widget)

        item = SiMenuItem(self, SiMenuItem.Type.Custom, new_action)
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

    def insertCustomWidget(self, before: QAction, widget: SiMenuItemWidget) -> QAction:
        new_action = QAction(widget)

        item = SiMenuItem(self, SiMenuItem.Type.Custom, new_action)
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
        widget.reachedEnd.disconnect()
        widget.deleteLater()

        self._items.remove(item)
        self._widgets.pop(item)
        self._action_to_items.pop(action)

        return None

    # endregion

    def _refreshLayoutOrder(self) -> None:
        layout = self._container.layout()
        current_widgets = [layout.itemAt(i).widget() for i in range(layout.count())]
        desired_widgets = [self._widgets[item] for item in self._items if item in self._widgets]

        for i, widget in enumerate(desired_widgets):
            if i >= len(current_widgets) or current_widgets[i] is not widget:
                layout.removeWidget(widget)
                layout.insertWidget(i, widget)

    def _closeMenu(self) -> None:
        self.close()

    def _closeMenuTree(self) -> None:
        widget = self
        while isinstance(widget, SiMenu):
            widget.close()
            widget = widget.parent()

    def isSubmenu(self) -> bool:
        return isinstance(self.parent(), SiMenu)

    def refreshLayout(self) -> None:
        """立即更新布局"""
        self._refreshLayoutOrder()
        self._container.adjustSize()
        self.adjustSize()

    def sizeHint(self):
        container_size = self._container.sizeHint()
        expanded_rect = container_size.grownBy(self._margins)

        width = expanded_rect.width()
        height = min(expanded_rect.height() + 2, self.maximumHeight())

        return QSize(width, height)

    def popup(self, pos: QPoint, action: QAction | None = None) -> None:
        new_pos = pos - self._scroll_area.pos()
        super().popup(new_pos, action)

    def paintEvent(self, a0):
        pass

    def showEvent(self, a0):
        super().showEvent(a0)

        self._applyGraphicEffect()
        self._updateComponentsVisibility()

        if self._is_layout_dirty:
            self._refreshLayoutOrder()
            self._is_layout_dirty = False

        self._container.adjustSize()
        self.adjustSize()

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


class MenuItemsWidgetStyleData:
    seperator_color: QColor = QColor("#6a5e73")
    seperator_padding: int = 4

    action_idle: QColor = QColor("#00EDE1F4")
    action_hover: QColor = QColor("#20EDE1F4")
    action_name_enabled: QColor = QColor("#D1CBD4")
    action_name_disabled: QColor = QColor("#50D1CBD4")
    action_shortcut_name: QColor = QColor("#918497")
    action_shortcut_background: QColor = QColor("#201d23")


class SeperatorWidget(QWidget):
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)
        self.style_data = MenuItemsWidgetStyleData()
        self.setFixedHeight(1)

    def paintEvent(self, a0):
        padding = self.style_data.seperator_padding
        color = self.style_data.seperator_color
        with createPainter(self) as painter:
            painter.setPen(color)
            painter.drawLine(QPoint(padding, 0), QPoint(self.width() - padding, 0))


class ActionButton(SiDenseContainer):
    def __init__(self, action: QAction, parent_menu: QMenu, parent: QWidget) -> None:
        super().__init__(parent, direction=SiDenseContainer.LeftToRight)

        self.setContentsMargins(8, 0, 10, 0)
        self.layout().setSpacing(4)

        self.style_data = MenuItemsWidgetStyleData()

        self._action = action
        self._parent_menu = parent_menu
        self._pressed_flag = False
        self._has_child_menu = action.menu() is not None

        self._name_label = QLabel(self)
        self._shortcut_widget = QLabel(self)
        self._icon_widget = SiRoundPixmapWidget(self)
        self._submenu_indicator = SiRoundPixmapWidget(self)
        self._color_widget = SiAnimatedColorWidget(self)

        self._initContents()
        self.addWidget(self._icon_widget)
        self.addWidget(self._name_label)
        self.addWidget(self._submenu_indicator, side=Qt.RightEdge)
        self.addWidget(self._shortcut_widget, side=Qt.RightEdge)

        self._action.changed.connect(self._initContents)
        self._action.changed.connect(lambda: self.setEnabled(self._action.isEnabled()))

        self.addAction(action)

    def _initContents(self) -> None:
        self.setToolTip(self._action.whatsThis())

        sd = self.style_data
        ani = self._color_widget.animation()

        ani.setEndValue(self.style_data.action_idle)
        ani.setCurrentValue(self.style_data.action_idle)

        name_color = sd.action_name_enabled if self._action.isEnabled() else sd.action_name_disabled
        shortcut_text = sd.action_shortcut_name.name()
        shortcut_background = sd.action_shortcut_background.name()

        self._name_label.setStyleSheet(
            f"color: {name_color.name(QColor.HexArgb)};"
            "padding: 0px 4px 0px 4px;"
        )
        self._shortcut_widget.setStyleSheet(
            f"color: {shortcut_text};"
            f"background-color: {shortcut_background};"
            "padding: 1px 6px 1px 6px;"
            "margin: 1px 0px 0px 0px;"
            "border-radius: 4px;"
        )

        self._icon_widget.setPixmap(self._action.icon().pixmap(64, 64))
        self._icon_widget.setFixedSize(20, 20)
        self._icon_widget.setVisualSize(QSize(18, 18))
        self._icon_widget.setVisualSizeEnabled(True)
        self._icon_widget.setVisible(False)

        self._name_label.setFont(SiFont.getFont(size=14))
        self._name_label.setText(self._action.text())
        self._name_label.setAlignment(Qt.AlignVCenter)
        self._name_label.setFixedHeight(32)
        self._name_label.setMinimumWidth(32)
        self._name_label.adjustSize()

        self._shortcut_widget.setFont(SiFont.getFont(size=9))
        self._shortcut_widget.setText(self._action.shortcut().toString())
        self._shortcut_widget.setAlignment(Qt.AlignCenter)
        self._shortcut_widget.setFixedHeight(18)
        self._shortcut_widget.adjustSize()
        self._shortcut_widget.setVisible(self._shortcut_widget.text() != "")

        if self._has_child_menu:
            self._submenu_indicator.setPixmap(SiGlobal.siui.iconpack.toPixmap("ic_fluent_chevron_right_filled"))
        self._submenu_indicator.setFixedSize(16, 16)
        self._submenu_indicator.setVisualSize(QSize(16, 16))
        self._submenu_indicator.setContentsMargins(16, 8, 16, 8)
        self._submenu_indicator.setVisualSizeEnabled(True)
        self._submenu_indicator.setVisible(False)

        self._action.shortcut().toString()

        self._color_widget.setBorderRadius(6)

    def setHover(self, state: bool) -> None:
        ani = self._color_widget.animation()
        if state:
            ani.setEndValue(self.style_data.action_hover)
            ani.start()
        else:
            ani.setEndValue(self.style_data.action_idle)
            ani.start()

        if state:
            self._action.hover()

    def setIconVisible(self, state: bool) -> None:
        self._icon_widget.setVisible(state)

    def setSubmenuIndicatorVisible(self, state: bool) -> None:
        self._submenu_indicator.setVisible(state)

    def setShortCutVisible(self, state: bool) -> None:
        self._shortcut_widget.setVisible(state)

    def updateShortCutVisibility(self) -> None:
        text = self._action.shortcut().toString()
        self._shortcut_widget.setText(text)
        self._shortcut_widget.setVisible(text != "")

    def event(self, event):
        if event.type() == QEvent.ToolTip:
            return True  # 忽略工具提示事件
        return super().event(event)

    def enterEvent(self, a0):
        super().enterEvent(a0)
        showToolTip(self)
        raiseToolTipWindow()
        self.setHover(True)

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        hideToolTip(self)
        self.setHover(False)

    def paintEvent(self, a0):
        super().paintEvent(a0)
        local_pos = self.mapFromGlobal(QCursor.pos())
        is_hover = self.rect().contains(local_pos)
        self.setHover(is_hover)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self._color_widget.resize(a0.size())

    def mousePressEvent(self, a0):
        state = self._action.isEnabled()
        self._pressed_flag = state

        if state:
            a0.ignore()
        else:
            a0.accept()

    def mouseReleaseEvent(self, a0):
        menu = self._action.menu()
        has_child_menu = self._action.menu() is not None

        if self._action.isEnabled() and self._pressed_flag:
            self._action.trigger()

            if has_child_menu:
                menu.popup(menu.toPopupPos(self.mapToGlobal(self.rect().topRight())))
                a0.accept()

            else:
                widget = self._parent_menu
                while isinstance(widget, SiRoundMenu):
                    widget.close()
                    widget = widget.parent()

                a0.ignore()
        else:
            a0.accept()
        self._pressed_flag = False

    def focusOutEvent(self, a0):
        super().focusOutEvent(a0)
        self.setHover(False)


class RoundMenuStyleData:
    background: QColor = QColor("#322e37")
    border: QColor = QColor("#3c3841")


class SiRoundMenu(QMenu):
    class Property:
        ViewSize = "viewSize"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.style_data = RoundMenuStyleData()

        self.setMaximumHeight(400)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.Popup
            | Qt.NoDropShadowWindowHint
        )

        self._padding = 32
        self._view_size = QSize(0, 0)
        self._actions_has_icon = False  # unused
        self._actions_has_child_menu = False  # unused
        self._is_mouse_pressed_in_self = False

        self.background = QLabel(self)
        self.view = SiScrollAreaRefactor(self)
        self.container = SiDenseContainer(self.view, SiDenseContainer.TopToBottom)

        self.view_size_ani = SiExpAnimationRefactor(self, self.Property.ViewSize)
        self.view_size_ani.init(1/6, 1, self._view_size, self._view_size)

        self._initStyle()

    def _initStyle(self) -> None:
        background = self.style_data.background.name()
        border = self.style_data.border.name()

        self.background.move(self._padding, self._padding)
        self.background.setStyleSheet(
            f"background-color: {background};"
            f"border: 1px solid {border};"
            "border-radius: 6px;"
        )

        self.view.setWidget(self.container)
        self.view.setViewportMargins(0, 1, -8, 1)
        self.view.move(self._padding, self._padding)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.container.layout().setSpacing(4)
        self.container.setContentsMargins(6, 4, 6, 4)

    def _applyDropShadowEffect(self):
        SiQuickEffect.applyDropShadowOn(self.background, color=(0, 0, 0, 128))

    def _updateComponentsVisibility(self) -> None:
        has_icon = False
        has_submenu = False
        for action in self.actions():
            if action.icon().isNull() is False:
                has_icon = True
            if action.menu() is not None:
                has_submenu = True

        layout = self.container.layout()
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, ActionButton) is False:
                continue
            widget.setIconVisible(has_icon)
            widget.setSubmenuIndicatorVisible(has_submenu)
            widget.updateShortCutVisibility()

        self.container.adjustSize()
        self.adjustSize()

    @pyqtProperty(QSize)
    def viewSize(self):
        return self._view_size

    @viewSize.setter
    def viewSize(self, value: QSize):
        self._view_size = value
        self.view.resize(value)
        self.background.resize(value)

    def toPopupPos(self, pos: QPoint) -> QPoint:
        return QPoint(pos.x() - self._padding, pos.y() - self._padding)

    def addAction(self, action: QAction) -> None:
        new_widget = ActionButton(action=action, parent_menu=self, parent=self)
        self.container.addWidget(new_widget)
        self.container.adjustSize()

        super().addAction(action)

    def addMenu(self, menu: QMenu) -> QAction:
        action = menu.menuAction()
        new_widget = ActionButton(action=action, parent_menu=self, parent=self)
        self.container.addWidget(new_widget)
        self.container.adjustSize()

        super().addAction(action)
        return action

    def addSeparator(self) -> QAction | None:
        new_widget = SeperatorWidget(self)
        self.container.addWidget(new_widget)
        self.container.adjustSize()
        return super().addSeparator()

    def paintEvent(self, a0):
        pass

    def sizeHint(self):
        p = self._padding
        return QSize(self.container.width() + p * 2,
                     min(self.container.height() + p * 2 + 2, self.maximumHeight()))

    def mouseMoveEvent(self, a0):
        a0.ignore()

    def mousePressEvent(self, a0):
        s = self.rect().adjusted(self._padding, self._padding, -self._padding, -self._padding).contains(a0.pos())
        self._is_mouse_pressed_in_self = s

    def mouseReleaseEvent(self, a0):
        s = self.rect().adjusted(self._padding, self._padding, -self._padding, -self._padding).contains(a0.pos())
        if not s and not self._is_mouse_pressed_in_self:
            self.close()
        self._is_mouse_pressed_in_self = False

    def showEvent(self, a0):
        super().showEvent(a0)
        self._applyDropShadowEffect()
        self._updateComponentsVisibility()

        width = self.size().width() - self._padding * 2
        height = self.size().height() - self._padding * 2

        ani = self.view_size_ani
        ani.setCurrentValue(QSize(width, int(height * 0.6)))
        ani.setEndValue(QSize(width, height))
        ani.start()

    def hideEvent(self, a0):
        super().hideEvent(a0)

        width = self.size().width() - self._padding * 2
        height = self.size().height() - self._padding * 2

        ani = self.view_size_ani
        ani.stop()
        ani.setCurrentValue(QSize(width, int(height * 0.6)))
        ani.toProperty()

