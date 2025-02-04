from __future__ import annotations

from PyQt5.QtCore import QEvent, QPoint, QRect, QSize, Qt, pyqtProperty
from PyQt5.QtGui import QColor, QCursor, QPalette
from PyQt5.QtWidgets import QAction, QBoxLayout, QLabel, QMenu, QSizePolicy, QWidget, QWidgetAction

from siui.components.button import SiFlatButton, SiPushButtonRefactor
from siui.components.container import SiDenseContainer
from siui.components.label import SiAnimatedColorWidget
from siui.components.slider_ import SiScrollAreaRefactor
from siui.core import SiQuickEffect, createPainter, hideToolTip, showToolTip
from siui.core.animation import SiExpAnimationRefactor
from siui.core.globals import raiseToolTipWindow
from siui.gui import SiFont
from siui.typing import T_WidgetParent


class SiRoundMenuWidgetAction(QWidgetAction):
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

    def createWidget(self, parent):
        button = SiPushButtonRefactor(parent)
        button.setText(self.text())
        return button


class SeperatorWidget(QWidget):
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)
        self.setFixedHeight(1)

    def paintEvent(self, a0):
        with createPainter(self) as painter:
            painter.setPen(QColor("#6a5e73"))
            painter.drawLine(QPoint(4, 0), QPoint(self.width() - 4, 0))


class ActionWidget(SiDenseContainer):
    def __init__(self, action: QAction, parent: QWidget) -> None:
        super().__init__(parent, direction=SiDenseContainer.LeftToRight)

        self.setContentsMargins(10, 0, 10, 0)
        self.layout().setSpacing(4)

        self.action = action
        self._pressed_flag = False

        self.color_widget = SiAnimatedColorWidget(self)
        self.icon = QLabel(self)
        self.name = QLabel(self)
        self.shortcut = QLabel(self)
        self.child_icon = QLabel(self)

        self._initContents()
        self.addWidget(self.icon)
        self.addWidget(self.name)
        self.addWidget(self.child_icon, side=Qt.RightEdge)
        self.addWidget(self.shortcut, side=Qt.RightEdge)

        self.action.changed.connect(self._initContents)
        self.action.changed.connect(lambda: self.setEnabled(self.action.isEnabled()))

    def _initContents(self) -> None:
        self.setToolTip(self.action.whatsThis())

        self.color_widget.animation().setCurrentValue(QColor("#00EDE1F4"))
        self.color_widget.animation().setEndValue(QColor("#00EDE1F4"))
        self.color_widget.setBorderRadius(6)

        self.name.setStyleSheet(
            f"color: {'#D1CBD4' if self.action.isEnabled() else '#50D1CBD4'};"
            "padding-right: 4px"
        )
        self.shortcut.setStyleSheet(
            "color: #918497; background-color: #201d23;"
            "padding: 1px 6px 1px 6px;"
            "margin: 1px 0px 0px 0px;"
            "border-radius: 4px;"
        )

        self.icon.setPixmap(self.action.icon().pixmap(16, 16))
        self.icon.setFixedSize(24, 24)
        self.icon.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.icon.setContentsMargins(16, 8, 16, 8)
        self.icon.setVisible(False)

        self.name.setFont(SiFont.getFont(size=14))
        # self.name.setFont(self.action.font())
        self.name.setText(self.action.text())
        self.name.setAlignment(Qt.AlignVCenter)
        self.name.setFixedHeight(32)
        self.name.setMinimumWidth(32)
        self.name.adjustSize()

        self.shortcut.setFont(SiFont.getFont(size=9))
        self.shortcut.setText("+".join([sc.toString() for sc in self.action.shortcuts()]))
        self.shortcut.setAlignment(Qt.AlignCenter)
        self.shortcut.setFixedHeight(18)
        self.shortcut.adjustSize()
        self.shortcut.setVisible(self.shortcut.text() != "")
        # self.shortcut.setVisible(False)

        self.child_icon.setFixedSize(16, 16)
        # self.child_icon.setVisible(False)

    def event(self, event):
        if event.type() == QEvent.ToolTip:
            return True  # 忽略工具提示事件
        return super().event(event)

    def enterEvent(self, a0):
        super().enterEvent(a0)
        self.color_widget.animation().setEndValue(QColor("#20EDE1F4"))
        self.color_widget.animation().start()
        self.action.hover()
        showToolTip(self)
        raiseToolTipWindow()

    def leaveEvent(self, a0):
        super().leaveEvent(a0)
        self.color_widget.animation().setEndValue(QColor("#00EDE1F4"))
        self.color_widget.animation().start()
        hideToolTip(self)

    def paintEvent(self, a0):
        super().paintEvent(a0)
        local_pos = self.mapFromGlobal(QCursor.pos())
        if self.rect().contains(local_pos):
            self.color_widget.animation().setEndValue(QColor("#20EDE1F4"))
            self.color_widget.animation().start()
        else:
            self.color_widget.animation().setEndValue(QColor("#00EDE1F4"))
            self.color_widget.animation().start()

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.color_widget.resize(a0.size())

    def mousePressEvent(self, a0):
        if self.action.isEnabled() is False:
            a0.accept()
            return
        else:
            a0.ignore()
            self._pressed_flag = True

    def mouseReleaseEvent(self, a0):
        if self.action.isEnabled():
            if self._pressed_flag:
                print(self.action.parent())
                if self.action.menu() is not None:
                    menu = self.action.menu()
                    menu.popup(menu.toPopupPos(self.mapToGlobal(self.rect().topRight())))
                    a0.accept()
                else:
                    a0.ignore()
                self.action.trigger()
        else:
            a0.accept()
        self._pressed_flag = False


class MenuActionContainer(SiDenseContainer):
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent, direction=SiDenseContainer.TopToBottom)

        self.layout().setSpacing(4)
        self.setContentsMargins(6, 4, 6, 4)


class SiRoundMenu(QMenu):
    class Property:
        ViewSize = "viewSize"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self.setMaximumHeight(400)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint
                            | Qt.Popup
                            | Qt.NoDropShadowWindowHint)

        self._actions = []
        self._padding = 32
        self._view_size = QSize(0, 0)

        self.background = QLabel(self)
        self.view = SiScrollAreaRefactor(self)
        self.container = MenuActionContainer(self.view)

        self.view_size_ani = SiExpAnimationRefactor(self, self.Property.ViewSize)
        self.view_size_ani.init(1/6, 1, self._view_size, self._view_size)

        self._initStyle()

    def _initStyle(self) -> None:
        self.background.setStyleSheet("background-color: #322e37; border-radius: 6px; border: 1px solid #3c3841")
        self.background.move(self._padding, self._padding)

        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.view.setViewportMargins(0, 1, -8, 1)
        self.view.setWidget(self.container)
        self.view.move(self._padding, self._padding)

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
        new_widget = ActionWidget(action=action, parent=self)
        self.container.addWidget(new_widget)
        self.container.adjustSize()
        self._actions.append(action)

    def addMenu(self, menu: QMenu) -> QAction:
        action = menu.menuAction()
        self.addAction(action)
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

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        width = a0.size().width() - self._padding * 2
        self.container.setFixedWidth(width)

    def showEvent(self, a0):
        super().showEvent(a0)

        self._applyDropShadowEffect()

        width = self.size().width() - self._padding * 2
        height = self.size().height() - self._padding * 2
        self.view_size_ani.setCurrentValue(QSize(width, int(height * 0.6)))
        self.view_size_ani.setEndValue(QSize(width, height))
        self.view_size_ani.start()

    def hideEvent(self, a0):
        super().hideEvent(a0)

        width = self.size().width() - self._padding * 2
        height = self.size().height() - self._padding * 2

        self.view_size_ani.stop()
        self.view_size_ani.setCurrentValue(QSize(width, int(height * 0.6)))
        self.setProperty(self.Property.ViewSize, QSize(width, int(height * 0.6)))
