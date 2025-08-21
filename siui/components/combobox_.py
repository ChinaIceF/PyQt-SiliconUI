from __future__ import annotations

from PyQt5.QtCore import QEvent, QMargins, QObject, QPoint, QRect, QRectF, QSize, Qt
from PyQt5.QtGui import QColor, QIcon, QKeySequence, QMouseEvent, QPainter, QPainterPath
from PyQt5.QtWidgets import QAction, QActionGroup, QComboBox, QHBoxLayout, QLabel, QSpacerItem, QWidget

from siui.components.button import SiFlatButton, SiTransparentButton
from siui.components.editbox import SiCapsuleLineEdit
from siui.components.label import SiRoundPixmapWidget
from siui.components.menu_ import ActionItemsWidgetStyleData, SiMenuItemWidget, SiRoundedMenu
from siui.core import SiGlobal, createPainter
from siui.core.event_filter import WidgetTooltipAcceptEventFilter
from siui.gui import SiFont
from siui.typing import T_WidgetParent


class CheckedIndicatorStyleData:
    indicator_color = QColor("#D087DF")


class ComboboxItemWidgetCheckedIndicator(QWidget):
    def __init__(self, action: QAction, parent=None):
        super().__init__(parent)

        self._action = action
        self._is_checked = self._action.isChecked()

        self.style_data = CheckedIndicatorStyleData()

    def updateAction(self) -> None:
        self._is_checked = self._action.isChecked()
        self.update()

    def _drawIndicatorRect(self, painter: QPainter, rect: QRect) -> None:
        if self._is_checked is False:
            return
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), 2, 2)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.style_data.indicator_color)
        painter.drawPath(path)

    def paintEvent(self, a0):
        rect = self.rect()

        with createPainter(self) as painter:
            self._drawIndicatorRect(painter, rect)


class ComboboxItemWidget(SiMenuItemWidget):
    def __init__(self, action: QAction, parent=None):
        super().__init__(action, parent)

        self.setFixedHeight(32)

        self._action = action
        self.style_data = ActionItemsWidgetStyleData()

        self._checked_indicator = ComboboxItemWidgetCheckedIndicator(action, self)
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

        self._checked_indicator.setFixedSize(4, 16)

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


class ComboBoxClickEventFilter(QObject):
    def __init__(self, combobox: QComboBox, line_edit: SiCapsuleLineEdit, menu: SiRoundedMenu):
        super().__init__(line_edit)
        self._combobox = combobox
        self._line_edit = line_edit
        self._menu = menu

        self._is_pressed = False

    def eventFilter(self, obj: QWidget, event: QEvent):
        if self._combobox.isEditable():
            return False

        if event.type() == QEvent.Type.MouseButtonPress:
            event: QMouseEvent
            self._is_pressed = event.button() == Qt.LeftButton
            return False

        if event.type() == QEvent.Type.MouseButtonRelease:
            if self._is_pressed:
                self._combobox.showPopup()

            self._is_pressed = False
            return True

        return False


class SiCapsuleComboBox(QComboBox):
    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)

        self._is_menu_dirty = True

        self._menu = SiRoundedMenu(self)
        self._text_to_width_hint: dict[str, int] = {}
        self._max_width_hint = -1
        self._title = "untitled"

        self._line_edit = SiCapsuleLineEdit(self)

        self._initStyleSheet()
        self._initWidget()
        self._initClickEventFilter()
        self._initModelSignals()
        self._initMenuSignals()

    def _initStyleSheet(self) -> None:
        self.setStyleSheet("""
            QComboBox {
                border: none;
            }
            QComboBox::drop-down {
                width: 0px;
                border: 0px;
            }
            QComboBox:editable {
                padding-right: 0px;
            }
        """)

    def _initWidget(self) -> None:
        button = SiFlatButton(self)
        button.setFixedSize(28, 28)
        button.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_chevron_down_regular"))
        button.clicked.connect(self.showPopup)

        super().setLineEdit(self._line_edit)
        self._line_edit.setReadOnly(not self.isEditable())
        self._line_edit.setTitle(self._title)
        self._line_edit.addWidgetToRight(button)
        self._line_edit.setContextMenuPolicy(Qt.CustomContextMenu)

    def _initClickEventFilter(self) -> None:
        self._click_event_filter = ComboBoxClickEventFilter(self, self._line_edit, self._menu)
        self._line_edit.installEventFilter(self._click_event_filter)

    def _initModelSignals(self) -> None:
        model = self.model()
        model.dataChanged.connect(self._onModelChanged)
        model.layoutChanged.connect(self._onModelChanged)
        model.modelReset.connect(self._onModelChanged)
        model.rowsInserted.connect(self._onModelChanged)
        model.rowsRemoved.connect(self._onModelChanged)
        model.columnsInserted.connect(self._onModelChanged)
        model.columnsRemoved.connect(self._onModelChanged)

    def _initMenuSignals(self) -> None:
        self._menu.triggered.connect(self._onMenuActionTriggered)

    def _onMenuActionTriggered(self, action: QAction) -> None:
        self.setCurrentIndex(action.data())

    def _onModelChanged(self) -> None:
        self._is_menu_dirty = True
        self.updateGeometry()

    def _rebuildMenu(self) -> None:
        self._menu.clear()

        action_group = QActionGroup(self)
        action_group.setExclusionPolicy(QActionGroup.ExclusionPolicy.Exclusive)

        for i in range(self.count()):
            text = self.itemText(i)
            action = QAction(text)
            action.setData(i)
            action.setCheckable(True)
            action.setChecked(i == self.currentIndex())

            action_group.addAction(action)
            self._menu.addCustomWidget(action, ComboboxItemWidget)

        self._menu.refreshLayout()

    def _calcSizeHintCache(self) -> None:
        for i in range(self.count()):
            text = self.itemText(i)
            if text in self._text_to_width_hint.keys():
                continue

            width_for_text = self._line_edit.widthForText(text)
            self._text_to_width_hint.update([(text, width_for_text)])

        self._max_width_hint = max(list(self._text_to_width_hint.values()) + [0])

    def sizeHint(self):
        if self._is_menu_dirty:
            self._rebuildMenu()
            self._calcSizeHintCache()
            self._is_menu_dirty = False
        return QSize(self._max_width_hint, super().sizeHint().height())

    def minimumSizeHint(self):
        min_width = self._line_edit.widthForText("") + 48
        min_height = 36
        return QSize(min_width, min_height)

    def setTitle(self, text: str) -> None:
        self._title = text
        self._line_edit.setTitle(text)
        self.updateGeometry()

    def setEditable(self, editable: bool) -> None:
        self._line_edit.setReadOnly(not editable)

    def isEditable(self) -> bool:
        return not self._line_edit.isReadOnly()

    def showPopup(self) -> None:
        if self._is_menu_dirty:
            self._rebuildMenu()
            self._calcSizeHintCache()
            self._is_menu_dirty = False

        title_width = self._line_edit.titleWidth()
        menu_width = self.width() - title_width
        self._menu.container().setFixedWidth(menu_width)

        pos = self.rect().bottomLeft() + QPoint(title_width, 0)
        self._menu.popup(self.mapToGlobal(pos))

    def hidePopup(self) -> None:
        self._menu.close()

    def paintEvent(self, e):
        pass

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._line_edit.resize(e.size())
