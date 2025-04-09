from __future__ import annotations

from PyQt5.QtCore import QEvent, QPoint, QSize, Qt, pyqtProperty
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtWidgets import QAction, QLabel, QMenu, QWidget, QWidgetAction

from siui.components.button import SiPushButtonRefactor
from siui.components.container import SiDenseContainer
from siui.components.label import SiAnimatedColorWidget, SiRoundPixmapWidget
from siui.components.slider_ import SiScrollAreaRefactor
from siui.core import SiQuickEffect, createPainter, hideToolTip, showToolTip
from siui.core.animation import SiExpAnimationRefactor
from siui.core.globals import SiGlobal, raiseToolTipWindow
from siui.gui import SiFont
from siui.typing import T_WidgetParent


class SiRoundMenuWidgetAction(QWidgetAction):
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

    def createWidget(self, parent):
        button = SiPushButtonRefactor(parent)
        button.setText(self.text())
        return button


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

        self.setContentsMargins(10, 0, 10, 0)
        self.layout().setSpacing(4)

        self.style_data = MenuItemsWidgetStyleData()

        self._action = action
        self._parent_menu = parent_menu
        self._pressed_flag = False
        self._has_child_menu = action.menu() is not None

        self.name = QLabel(self)
        self.shortcut = QLabel(self)
        self.icon = SiRoundPixmapWidget(self)
        self.child_icon = SiRoundPixmapWidget(self)
        self.color_widget = SiAnimatedColorWidget(self)

        self._initContents()
        self.addWidget(self.icon)
        self.addWidget(self.name)
        self.addWidget(self.child_icon, side=Qt.RightEdge)
        self.addWidget(self.shortcut, side=Qt.RightEdge)

        self._action.changed.connect(self._initContents)
        self._action.changed.connect(lambda: self.setEnabled(self._action.isEnabled()))

        self.addAction(action)

    def _initContents(self) -> None:
        self.setToolTip(self._action.whatsThis())

        sd = self.style_data
        ani = self.color_widget.animation()

        ani.setEndValue(self.style_data.action_idle)
        ani.setCurrentValue(self.style_data.action_idle)

        name_color = sd.action_name_enabled if self._action.isEnabled() else sd.action_name_disabled
        shortcut_text = sd.action_shortcut_name.name()
        shortcut_background = sd.action_shortcut_background.name()

        self.name.setStyleSheet(
            f"color: {name_color.name(QColor.HexArgb)};"
            "padding: 0px 4px 0px 4px;"
        )
        self.shortcut.setStyleSheet(
            f"color: {shortcut_text};"
            f"background-color: {shortcut_background};"
            "padding: 1px 6px 1px 6px;"
            "margin: 1px 0px 0px 0px;"
            "border-radius: 4px;"
        )

        self.icon.setPixmap(self._action.icon().pixmap(64, 64))
        self.icon.setFixedSize(20, 20)
        self.icon.setVisualSize(QSize(18, 18))
        self.icon.setContentsMargins(16, 8, 16, 8)
        self.icon.setVisualSizeEnabled(True)
        self.icon.setVisible(False)

        self.name.setFont(SiFont.getFont(size=14))
        # self.name.setFont(self.action.font())
        self.name.setText(self._action.text())
        self.name.setAlignment(Qt.AlignVCenter)
        self.name.setFixedHeight(32)
        self.name.setMinimumWidth(32)
        self.name.adjustSize()

        self.shortcut.setFont(SiFont.getFont(size=9))
        self.shortcut.setText("+".join([sc.toString() for sc in self._action.shortcuts()]))
        self.shortcut.setAlignment(Qt.AlignCenter)
        self.shortcut.setFixedHeight(18)
        self.shortcut.adjustSize()
        self.shortcut.setVisible(self.shortcut.text() != "")
        #
        if self._has_child_menu:
            self.child_icon.setPixmap(SiGlobal.siui.iconpack.toPixmap("ic_fluent_caret_right_filled"))
        self.child_icon.setFixedSize(16, 16)
        self.child_icon.setVisualSize(QSize(16, 16))
        self.child_icon.setContentsMargins(16, 8, 16, 8)
        self.child_icon.setVisualSizeEnabled(True)
        self.child_icon.setVisible(False)

        self.color_widget.setBorderRadius(6)

    def setHover(self, state: bool) -> None:
        ani = self.color_widget.animation()
        if state:
            ani.setEndValue(self.style_data.action_hover)
            ani.start()
        else:
            ani.setEndValue(self.style_data.action_idle)
            ani.start()

        if state:
            self._action.hover()

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
        self.color_widget.resize(a0.size())

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


class MenuActionContainer(SiDenseContainer):
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent, direction=SiDenseContainer.TopToBottom)

        self.layout().setSpacing(4)
        self.setContentsMargins(6, 4, 6, 4)


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
        self.container = MenuActionContainer(self.view)

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

    def _applyDropShadowEffect(self):
        SiQuickEffect.applyDropShadowOn(self.background, color=(0, 0, 0, 128))

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

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        width = a0.size().width() - self._padding * 2
        self.container.setFixedWidth(width)

    def showEvent(self, a0):
        super().showEvent(a0)
        self._applyDropShadowEffect()

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
