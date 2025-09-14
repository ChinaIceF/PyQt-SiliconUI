from __future__ import annotations

import difflib

from PyQt5.QtCore import QMargins, QObject, QPoint, QPointF, QRect, QRectF, QSize, QSizeF, Qt, pyqtProperty
from PyQt5.QtGui import (
    QColor,
    QDoubleValidator,
    QFont,
    QFontMetrics,
    QIntValidator,
    QPainter,
    QPainterPath,
    QTextOption,
)
from PyQt5.QtWidgets import QAction, QApplication, QLineEdit, QWidget

from siui.components.button import SiFlatButton
from siui.components.container import SiBoxContainer, SiDenseContainer
from siui.components.menu_ import SiRoundedMenu
from siui.core import SiGlobal, createPainter
from siui.core.animation import SiExpAnimationRefactor
from siui.core.event_filter import WidgetToolTipRedirectEventFilter
from siui.gui import SiFont
from siui.typing import T_WidgetParent


# @dataclass
class LineEditStyleData:
    STYLE_TYPES = ["Slider"]

    title_background_color: QColor = QColor("#28252d")
    title_color_idle: QColor = QColor("#918497")
    title_color_focused: QColor = QColor("#D1CBD4")
    title_color_error: QColor = QColor("#b27b84")

    text_background_color: QColor = QColor("#201d23")
    text_color: QColor = QColor("#D1CBD4")

    text_indicator_color_idle: QColor = QColor("#00D087DF")
    text_indicator_color_editing: QColor = QColor("#D087DF")
    text_indicator_color_error: QColor = QColor("#d36764")


class SiCapsuleLineEdit(QLineEdit):
    class TitleWidthMode:
        Preferred = "Preferred"
        Fixed = "Fixed"
        Ratio = "Ratio"

    class Property:
        TitleColor = "titleColor"
        TextIndicatorColor = "textIndicatorColor"
        TextIndicatorWidth = "textIndicatorWidth"

    def __init__(self, parent: T_WidgetParent = None, title: str = "Untitled") -> None:
        super().__init__(parent)

        self.setFont(SiFont.getFont(size=14))

        self.style_data = LineEditStyleData()

        self._left_edge_container = SiBoxContainer(self)
        self._right_edge_container = SiBoxContainer(self)

        self._title_font = SiFont.getFont(size=13)
        self._title_text = title
        self._title_text_margins = QMargins(17, 0, 17, 0)
        self._title_width_mode = self.TitleWidthMode.Preferred
        self._title_fixed_width = 160
        self._title_ratio = 0.25

        self._in_rect_container_margins = QMargins(8, 0, 8, 0)
        self._in_rect_text_margins = QMargins(10, 0, 10, 0)
        self._user_text_margins = QMargins(0, 0, 0, 0)

        self._title_color = self.style_data.title_color_idle
        self._text_indi_color = self.style_data.text_indicator_color_idle
        self._text_indi_width = 0
        self._text_bg_width_progress = 0

        self.title_color_ani = SiExpAnimationRefactor(self, self.Property.TitleColor)
        self.title_color_ani.init(1/6, 0.001, self._title_color, self._title_color)

        self.text_indicator_color_ani = SiExpAnimationRefactor(self, self.Property.TextIndicatorColor)
        self.text_indicator_color_ani.init(1/4, 0.01, self._text_indi_color, self._text_indi_color)

        self.text_indicator_width_ani = SiExpAnimationRefactor(self, self.Property.TextIndicatorWidth)
        self.text_indicator_color_ani.init(1/8, 0.01, 0, 0)

        self._initWidget()
        self._initStyleSheet()
        self._initTooltipRedirectEventFilter()
        self._initSignals()

        self._updateTextMargins()

        self._createCustomMenu()
        self.setContextMenuPolicy(Qt.CustomContextMenu)

    def _initWidget(self) -> None:
        self._left_edge_container.layout().setDirection(SiBoxContainer.LeftToRight)
        self._left_edge_container.layout().setSpacing(6)
        self._right_edge_container.layout().setDirection(SiBoxContainer.RightToLeft)
        self._right_edge_container.layout().setSpacing(6)

    def _initStyleSheet(self) -> None:
        self.setStyleSheet(
            "QLineEdit {"
            "     selection-background-color: #493F4E;"
            "     background-color: transparent;"
            f"    color: {self.style_data.text_color.name()};"
            "     border: 0px;"
            "}"
        )

    def _initTooltipRedirectEventFilter(self):
        self._tooltip_redirect_event_filter = WidgetToolTipRedirectEventFilter()
        self.installEventFilter(self._tooltip_redirect_event_filter)

    def _initSignals(self) -> None:
        self.customContextMenuRequested.connect(self._showCustomMenu)
        self.textChanged.connect(self._onTextEdited)
        self.returnPressed.connect(self._onReturnPressed)

    # region Property

    @pyqtProperty(QColor)
    def titleColor(self):
        return self._title_color

    @titleColor.setter
    def titleColor(self, value: QColor):
        self._title_color = value
        self.update()

    @pyqtProperty(float)
    def textBackgroundWidthProgress(self):
        return self._text_bg_width_progress

    @textBackgroundWidthProgress.setter
    def textBackgroundWidthProgress(self, value: float):
        self._text_bg_width_progress = value
        self.update()

    @pyqtProperty(QColor)
    def textIndicatorColor(self):
        return self._text_indi_color

    @textIndicatorColor.setter
    def textIndicatorColor(self, value: QColor):
        self._text_indi_color = value
        self.update()

    @pyqtProperty(float)
    def textIndicatorWidth(self):
        return self._text_indi_width

    @textIndicatorWidth.setter
    def textIndicatorWidth(self, value: float):
        self._text_indi_width = value
        self.update()

    # endregion

    def _showCustomMenu(self, pos: QPoint):
        print(self.actions())
        self.undo_action.setEnabled(self.isUndoAvailable())
        self.redo_action.setEnabled(self.isRedoAvailable())
        self.cut_action.setEnabled(self.hasSelectedText())
        self.copy_action.setEnabled(self.hasSelectedText())
        self.paste_action.setEnabled(bool(QApplication.clipboard().text()))
        self.select_all_action.setEnabled(len(self.text()) > 0)

        self.menu.popup(self.mapToGlobal(pos))

    def _createCustomMenu(self):
        self.menu = SiRoundedMenu(self)

        self.undo_action = QAction("撤销", self)
        self.undo_action.setShortcut("Ctrl+Z")
        self.undo_action.triggered.connect(self.undo)

        self.redo_action = QAction("重做", self)
        self.redo_action.setShortcut("Ctrl+Shift+Z")
        self.redo_action.triggered.connect(self.redo)

        self.cut_action = QAction("剪切", self)
        self.cut_action.setShortcut("Ctrl+X")
        self.cut_action.triggered.connect(self.cut)

        self.copy_action = QAction("复制", self)
        self.copy_action.setShortcut("Ctrl+C")
        self.copy_action.triggered.connect(self.copy)

        self.paste_action = QAction("粘贴", self)
        self.paste_action.setShortcut("Ctrl+V")
        self.paste_action.triggered.connect(self.paste)

        self.select_all_action = QAction("全选", self)
        self.select_all_action.setShortcut("Ctrl+A")
        self.select_all_action.triggered.connect(self.selectAll)

        self.menu.addAction(self.undo_action)
        self.menu.addAction(self.redo_action)
        self.menu.addSeparator()
        self.menu.addAction(self.cut_action)
        self.menu.addAction(self.copy_action)
        self.menu.addAction(self.paste_action)
        self.menu.addSeparator()
        self.menu.addAction(self.select_all_action)
        self.menu.adjustSize()

    def title(self) -> str:
        return self._title

    def _updateTextMargins(self) -> None:
        user_text_margins = self._user_text_margins
        in_rect_text_margins = self._in_rect_text_margins
        in_rect_container_margins = self._in_rect_container_margins
        container_margins = self._calcContainerMargins()

        title_text_margins = self._title_text_margins
        title_text_width = self._calcTitleTextWidth()

        out_rect_margins = QMargins()
        out_rect_margins.setLeft(title_text_margins.left() + title_text_margins.right() + title_text_width)

        new_margins = user_text_margins + in_rect_text_margins + container_margins + in_rect_container_margins + out_rect_margins
        super().setTextMargins(new_margins)

    def _updateContainerGeometry(self) -> None:
        margins = self._in_rect_container_margins
        text_rect = self._calcTextRect()
        available_rect = text_rect.marginsRemoved(margins)

        left_size = self._left_edge_container.sizeHint()
        x = available_rect.left()
        self._right_edge_container.setGeometry(x, 0, left_size.width(), self.height())

        right_size = self._right_edge_container.sizeHint()
        x = available_rect.right() - right_size.width()
        self._right_edge_container.setGeometry(x, 0, right_size.width(), self.height())

    def setTitle(self, title: str) -> None:
        self._title_text = title
        self._updateTextMargins()
        self._updateContainerGeometry()
        self.update()

    def setTitleWidthMode(self, mode) -> None:
        self._title_width_mode = mode
        self._updateTextMargins()
        self._updateContainerGeometry()
        self.update()

    def setTitleFixedWidth(self, width: int) -> None:
        self._title_fixed_width = width
        self._updateTextMargins()
        self._updateContainerGeometry()
        self.update()

    def setTitleRatio(self, ratio: float) -> None:
        self._title_ratio = ratio
        self._updateTextMargins()
        self._updateContainerGeometry()
        self.update()

    def titleWidth(self) -> int:
        return self._calcTitleRect().width()

    def widthForText(self, text: str) -> int:
        metrics = QFontMetrics(self.font())
        text_size = QSize(metrics.horizontalAdvance(text) + 8, 0)
        grown_size = text_size.grownBy(super().textMargins())
        return grown_size.width()

    def setTextMargins(self, left: int, top: int, right: int, bottom: int) -> None:
        self._user_text_margins = QMargins(left, top, right, bottom)
        self._updateTextMargins()

    def textMargins(self) -> QMargins:
        return self._user_text_margins

    def leftEdgeContainer(self) -> QWidget:
        return self._left_edge_container

    def rightEdgeContainer(self) -> QWidget:
        return self._right_edge_container

    def addWidgetToLeft(self, widget: QWidget) -> None:
        self._left_edge_container.addWidget(widget)
        self._updateTextMargins()
        self._updateContainerGeometry()

    def addWidgetToRight(self, widget: QWidget) -> None:
        self._right_edge_container.layout().addWidget(widget)
        self._updateTextMargins()
        self._updateContainerGeometry()

    def notifyInvalidInput(self):
        self.text_indicator_color_ani.setEndValue(self.style_data.text_indicator_color_error)
        self.text_indicator_color_ani.start()
        self.title_color_ani.setEndValue(self.style_data.title_color_error)
        self.title_color_ani.start()
        self.text_indicator_width_ani.setEndValue(self.width() - self._title_width - 36)
        self.text_indicator_width_ani.start()

    def _onTextEdited(self, text: str):
        margins = self._in_rect_container_margins + self._calcContainerMargins() + self._in_rect_text_margins
        metric = QFontMetrics(self.font())
        text_rect = self._calcTextRect()
        text_bounding_width = metric.boundingRect(text).width()
        available_width = text_rect.marginsRemoved(margins).width()
        width = min(text_bounding_width, available_width)

        self.text_indicator_width_ani.setEndValue(width)
        self.text_indicator_width_ani.start()

    def _onReturnPressed(self):
        # find the nearest edit box and give focus to it.
        target = None
        for widget in self.parent().findChildren(QLineEdit):
            if widget.x() > self.x() or widget.y() > self.y():
                if target is None:
                    target = widget
                    continue
                if widget.x() < target.x() or widget.y() < target.y():
                    target = widget
                    continue

        if target is not None:
            target.setFocus()
        self.clearFocus()

    def _calcTitleTextWidth(self) -> int:
        if self._title_width_mode == self.TitleWidthMode.Preferred:
            metrics = QFontMetrics(self._title_font)
            return metrics.horizontalAdvance(self._title_text)

        elif self._title_width_mode == self.TitleWidthMode.Fixed:
            return self._title_fixed_width

        elif self._title_width_mode == self.TitleWidthMode.Ratio:
            return int(self.width() * self._title_ratio)

        else:
            raise ValueError(f"{self._title_width_mode}")

    def _calcTitleRect(self) -> QRect:
        width = self._calcTitleTextWidth() + self._title_text_margins.left() + self._title_text_margins.right()
        height = self.height() + self._title_text_margins.top() + self._title_text_margins.bottom()
        rect = QRect(0, 0, width, height)
        return rect

    def _calcTextRect(self) -> QRect:
        rect = self.rect()
        shrunk_rect = rect.adjusted(self._calcTitleRect().width(), 0, 0, 0)
        return shrunk_rect

    def _calcContainerMargins(self) -> QMargins:
        container_margins = QMargins()
        container_margins.setLeft(self._left_edge_container.sizeHint().width())
        container_margins.setRight(self._right_edge_container.sizeHint().width())
        return container_margins

    def _drawBodyBackgroundRect(self, painter: QPainter, rect: QRect) -> None:
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), 10, 10)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.style_data.title_background_color)
        painter.drawPath(path)

    def _drawEditBackgroundRect(self, painter: QPainter, rect: QRect) -> None:
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), 10, 10)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.style_data.text_background_color)
        painter.drawPath(path)

    def _drawTitleText(self, painter: QPainter, rect: QRect) -> None:
        shrunk_rect = rect.marginsRemoved(self._title_text_margins)
        option = QTextOption()
        option.setWrapMode(QTextOption.WrapMode.NoWrap)
        option.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        painter.setFont(self._title_font)
        painter.setPen(self._title_color)
        painter.drawText(QRectF(shrunk_rect), self._title_text, option)

    def _drawIndicatorRect(self, painter: QPainter, rect: QRect) -> None:
        container_margins = self._calcContainerMargins()

        shrunk_rect = rect.marginsRemoved(container_margins)
        indi_rect = QRectF(shrunk_rect.topLeft() + QPoint(16, 34), QSizeF(self._text_indi_width + 8, 2))

        path = QPainterPath()
        path.addRoundedRect(indi_rect, 1, 1)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._text_indi_color)
        painter.drawPath(path)

    def paintEvent(self, a0):
        body_rect = self.rect()
        title_rect = self._calcTitleRect()
        text_rect = self._calcTextRect()

        with createPainter(self) as painter:
            self._drawBodyBackgroundRect(painter, body_rect)
            self._drawEditBackgroundRect(painter, text_rect)
            self._drawTitleText(painter, title_rect)
            self._drawIndicatorRect(painter, text_rect)

        super().paintEvent(a0)

    def focusInEvent(self, a0):
        super().focusInEvent(a0)
        self.text_indicator_color_ani.setEndValue(self.style_data.text_indicator_color_editing)
        self.text_indicator_color_ani.start()
        self.title_color_ani.setEndValue(self.style_data.title_color_focused)
        self.title_color_ani.start()

        self._onTextEdited(self.text())

    def focusOutEvent(self, a0):
        super().focusOutEvent(a0)
        self.text_indicator_color_ani.setEndValue(self.style_data.text_indicator_color_idle)
        self.text_indicator_color_ani.start()
        self.title_color_ani.setEndValue(self.style_data.title_color_idle)
        self.title_color_ani.start()

        self._onTextEdited("")

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self._updateContainerGeometry()

class AnimatedCharObject(QObject):

    class Property:
        TextOpacity = "textOpacity"
        TextPosition = "textPosition"

    def __init__(self, parent, text, start_pos: QPointF):
        super().__init__(parent)

        self._text = text
        self._start_pos = start_pos

        self._text_opacity = 1
        self._text_pos_p = 0

        self.opacity_ani = SiExpAnimationRefactor(self, self.Property.TextOpacity)
        self.opacity_ani.init(1/4, 0.0001, 1, 1)

        self.position_ani = SiExpAnimationRefactor(self, self.Property.TextPosition)
        self.position_ani.init(0, 0.05, self._text_pos_p, self._text_pos_p)

    @pyqtProperty(float)
    def textOpacity(self):
        return self._text_opacity

    @textOpacity.setter
    def textOpacity(self, value: float):
        self._text_opacity = value

    @pyqtProperty(float)
    def textPosition(self):
        return self._text_pos_p

    @textPosition.setter
    def textPosition(self, value: float):
        self._text_pos_p = value

    def disappear(self):
        self.position_ani.setEndValue(1)
        self.opacity_ani.setEndValue(0)

        self.position_ani.start()
        self.opacity_ani.start()

    def isDone(self):
        return self.opacity_ani.currentValue() == 0

    def text(self) -> str:
        return self._text

    def opacity(self) -> float:
        return self._text_opacity

    def position(self) -> QPointF:
        p = self._text_pos_p ** 2
        return self._start_pos + QPointF(0, 10) * p


class SiCustomLineEdit(QLineEdit):
    class Property:
        CharProgress = "charProgress"
        CursorX = "cursorX"

    def __init__(self, parent: T_WidgetParent = None) -> None:
        super().__init__(parent)
        self._origin_point = QPointF(0.0, 0.0)
        self._max_supported_length = 1000  # supported maximum length is 1000 chars
        self._char_progress = [0] * 1000
        self._cursor_x = 0
        self._animated_chars = []
        self._prev_text = ""

        self.char_prog_ani = SiExpAnimationRefactor(self, self.Property.CharProgress)
        self.char_prog_ani.init(1/4, 0.001, self._char_progress, self._char_progress)

        self.cursor_x_ani = SiExpAnimationRefactor(self, self.Property.CursorX)
        self.cursor_x_ani.init(1/2, 0.001, self._cursor_x, self._cursor_x)

        font = SiFont.getFont(size=14)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 0)
        self.setFont(font)
        self.setMaxLength(100)

        self.textChanged.connect(self._onTextChanged)
        self.cursorPositionChanged.connect(self._onCursorPositionChanged)

    @pyqtProperty(list)
    def charProgress(self):
        return self._char_progress

    @charProgress.setter
    def charProgress(self, value: list):
        self._char_progress = value
        self.update()

    @pyqtProperty(float)
    def cursorX(self):
        return self._cursor_x

    @cursorX.setter
    def cursorX(self, value: float):
        self._cursor_x = value
        self.update()

    def _getCharColor(self, index: int) -> QColor:
        return QColor(255, 255, 255, int(255 * self._char_progress[index] ** 0.5))

    def _getCharRect(self, x, y, line_rect, index: int) -> QRectF:
        pos = QPointF(x, y) + self._origin_point
        delta_y = 2 ** ((1 - self._char_progress[index]) * 2) - 1
        return QRectF(pos.x(), pos.y() + delta_y, 32, line_rect.height() - 1)

    def _drawTextChar(self, painter: QPainter, rect: QRectF) -> None:
        font = self.font()
        metrics = QFontMetrics(font)

        sum_x, sum_y = 0, 0
        for index, char in enumerate(self.text()):
            char_rect = self._getCharRect(sum_x, sum_y, rect, index)
            char_color = self._getCharColor(index)

            painter.setPen(char_color)
            painter.drawText(char_rect, Qt.AlignVCenter | Qt.AlignLeft, char)
            sum_x += metrics.width(char)

    def _drawCursorRect(self, painter: QPainter, line_rect: QRectF) -> None:
        if self.hasFocus():
            path = QPainterPath()
            path.addRoundedRect(self._cursor_x + 1, (line_rect.height() - 20) / 2, 5, 20, 2.0, 2.0)
            painter.setBrush(QColor("#30EDE1F4"))
            painter.setPen(Qt.NoPen)
            painter.drawPath(path)

    def _drawBackgroundRect(self, painter: QPainter, rect: QRectF) -> None:
        path = QPainterPath()
        path.addRoundedRect(rect, 6.0, 6.0)
        painter.setBrush(QColor("#252229"))
        painter.drawPath(path)

    def _drawAnimatedChar(self, painter: QPainter, rect: QRectF, obj: AnimatedCharObject):
        color = QColor("#EDE1F4")
        color.setAlphaF(obj.opacity())
        painter.setPen(color)
        painter.drawText(obj.position() + QPointF(1, 24), obj.text())

    def paintEvent(self, a0):
        text_rect = self.rect()
        background_rect = QRectF(0, 0, self.rect().width(), self.rect().height())

        with createPainter(self) as painter:
            self._drawBackgroundRect(painter, background_rect)
            self._drawTextChar(painter, text_rect)
            self._drawCursorRect(painter, text_rect)

            new_list = []
            for obj in self._animated_chars:
                if obj.isDone() is False:
                    self._drawAnimatedChar(painter, text_rect, obj)
                    new_list.append(obj)

            self._animated_chars = new_list

    @staticmethod
    def _findDeletedText(old_text, new_text):
        """使用 difflib 计算被删除的文本"""
        deleted = []
        seq = difflib.SequenceMatcher(None, old_text, new_text)

        for tag, i1, i2, j1, j2 in seq.get_opcodes():
            if tag == "delete":  # 标记删除的部分
                deleted.append(old_text[i1:i2])

        return "".join(deleted)

    def _onTextChanged(self, text) -> None:
        m = self._max_supported_length
        self.char_prog_ani.setEndValue([1] * len(text) + [0] * (m - len(text)))
        self.char_prog_ani.start()

        metrics = QFontMetrics(self.font())
        cursor_x = sum([metrics.width(char) for char in self.text()[:self.cursorPosition()]]) + self._origin_point.x() - 1

        deleted_text = self._findDeletedText(self._prev_text, text)
        obj = AnimatedCharObject(self, deleted_text, QPointF(cursor_x, 0))
        obj.disappear()

        self._animated_chars.append(obj)
        self._prev_text = text

    def _onCursorPositionChanged(self, old, new) -> None:
        metrics = QFontMetrics(self.font())
        cursor_x = sum([metrics.width(char) for char in self.text()[:new]]) + self._origin_point.x() - 1

        self.cursor_x_ani.setEndValue(cursor_x)
        self.cursor_x_ani.start()








class SiLabeledLineEdit(QLineEdit):
    class Property:
        TitleColor = "titleColor"
        TextIndicatorColor = "textIndicatorColor"
        TextIndicatorWidth = "textIndicatorWidth"

    def __init__(self, parent: T_WidgetParent = None, title: str = "Untitled Edit Box") -> None:
        super().__init__(parent)

        self.style_data = LineEditStyleData()
        self._title_font = SiFont.getFont(size=10, weight=QFont.Normal)
        self._title = title
        self._title_color = self.style_data.title_color_idle
        self._text_indi_color = self.style_data.text_indicator_color_idle
        self._text_indi_width = 0
        self._text_bg_width_progress = 0

        self.title_color_ani = SiExpAnimationRefactor(self, self.Property.TitleColor)
        self.title_color_ani.init(1/6, 0.001, self._title_color, self._title_color)

        self.text_indicator_color_ani = SiExpAnimationRefactor(self, self.Property.TextIndicatorColor)
        self.text_indicator_color_ani.init(1/4, 0.01, self._text_indi_color, self._text_indi_color)

        self.text_indicator_width_ani = SiExpAnimationRefactor(self, self.Property.TextIndicatorWidth)
        self.text_indicator_color_ani.init(1/8, 0.01, 0, 0)

        self.setFont(SiFont.getFont(size=14))
        self._initStyleSheet()

        self.textChanged.connect(self._onTextEdited)
        self.returnPressed.connect(self._onReturnPressed)

    def _initStyleSheet(self) -> None:
        self.setStyleSheet(
            "QLineEdit {"
            "     selection-background-color: #493F4E;"
            "     background-color: transparent;"
            f"    color: {self.style_data.text_color.name()};"
            "     border: 0px;"
            f"    padding-top: 22px;"
            "     padding-bottom: 1px;"
            "     padding-right: 15px;"
            "     padding-left: 15px;"
            "}"
        )

    @pyqtProperty(QColor)
    def titleColor(self):
        return self._title_color

    @titleColor.setter
    def titleColor(self, value: QColor):
        self._title_color = value
        self.update()

    @pyqtProperty(float)
    def textBackgroundWidthProgress(self):
        return self._text_bg_width_progress

    @textBackgroundWidthProgress.setter
    def textBackgroundWidthProgress(self, value: float):
        self._text_bg_width_progress = value
        self.update()

    @pyqtProperty(QColor)
    def textIndicatorColor(self):
        return self._text_indi_color

    @textIndicatorColor.setter
    def textIndicatorColor(self, value: QColor):
        self._text_indi_color = value
        self.update()

    @pyqtProperty(float)
    def textIndicatorWidth(self):
        return self._text_indi_width

    @textIndicatorWidth.setter
    def textIndicatorWidth(self, value: float):
        self._text_indi_width = value
        self.update()

    def title(self) -> str:
        return self._title

    def setTitle(self, title: str) -> None:
        self._title = title
        self.update()

    def notifyInvalidInput(self):
        self.text_indicator_color_ani.setEndValue(self.style_data.text_indicator_color_error)
        self.text_indicator_color_ani.start()
        self.title_color_ani.setEndValue(self.style_data.title_color_error)
        self.title_color_ani.start()
        self.text_indicator_width_ani.setEndValue(self.width() - 36)
        self.text_indicator_width_ani.start()

    def _onTextEdited(self, text: str):
        metric = QFontMetrics(self.font())
        width = min(metric.boundingRect(text).width(), self.width() - 36)

        self.text_indicator_width_ani.setEndValue(width)
        self.text_indicator_width_ani.start()

    def _onReturnPressed(self):
        # find the nearest edit box and give focus to it.
        target = None
        for widget in self.parent().findChildren(QLineEdit):
            if widget.x() > self.x() or widget.y() > self.y():
                if target is None:
                    target = widget
                    continue
                if widget.x() < target.x() or widget.y() < target.y():
                    target = widget
                    continue

        if target is not None:
            target.setFocus()
        self.clearFocus()

    def _drawTitleBackgroundPath(self, rect: QRectF) -> QPainterPath:
        path = QPainterPath()
        path.addRoundedRect(rect, 6, 6)
        return path

    def _drawTitleRect(self, painter: QPainter, rect: QRectF) -> None:
        sd = self.style_data

        painter.setPen(self._title_color)
        painter.setFont(self._title_font)
        text_rect = QRectF(rect.x() + 11, rect.y(), rect.width(), 22 - 1)
        text_drawing_rect = painter.boundingRect(text_rect, Qt.AlignVCenter | Qt.AlignLeft, self._title)
        background_rect = QRectF(rect.x(), rect.y(), text_drawing_rect.width() + 22, 48)
        painter.setPen(Qt.NoPen)

        painter.setBrush(sd.title_background_color)
        painter.drawPath(self._drawTitleBackgroundPath(background_rect))

        painter.setPen(self._title_color)
        painter.drawText(text_drawing_rect, self._title)

        painter.setPen(Qt.NoPen)

    def _drawTextBackgroundPath(self, rect: QRectF) -> QPainterPath:
        path = QPainterPath()
        path.addRoundedRect(rect, 10, 10)
        return path

    def _drawTextIndicatorPath(self, rect: QRectF) -> QPainterPath:
        indi_rect = QRectF(rect.x() + 14, rect.y() + 34, self._text_indi_width + 8, 2)
        path = QPainterPath()
        path.addRoundedRect(indi_rect, 1, 1)
        return path

    def _drawTextRect(self, painter: QPainter, rect: QRectF) -> None:
        sd = self.style_data
        painter.setBrush(sd.text_background_color)
        painter.drawPath(self._drawTextBackgroundPath(rect))

        painter.setBrush(self._text_indi_color)
        painter.drawPath(self._drawTextIndicatorPath(rect))

    def paintEvent(self, a0):
        title_rect = QRectF(0, 0, self.width(), self.height())
        text_rect = QRectF(0, 22, self.width(), self.height() - 22)

        renderHints = (
                QPainter.RenderHint.SmoothPixmapTransform
                | QPainter.RenderHint.TextAntialiasing
                | QPainter.RenderHint.Antialiasing
        )

        with createPainter(self, renderHints) as painter:
            self._drawTitleRect(painter, title_rect)
            self._drawTextRect(painter, text_rect)

        super().paintEvent(a0)

    def focusInEvent(self, a0):
        super().focusInEvent(a0)
        self.text_indicator_color_ani.setEndValue(self.style_data.text_indicator_color_editing)
        self.text_indicator_color_ani.start()
        self.title_color_ani.setEndValue(self.style_data.title_color_focused)
        self.title_color_ani.start()

        self._onTextEdited(self.text())

    def focusOutEvent(self, a0):
        super().focusOutEvent(a0)
        self.text_indicator_color_ani.setEndValue(self.style_data.text_indicator_color_idle)
        self.text_indicator_color_ani.start()
        self.title_color_ani.setEndValue(self.style_data.title_color_idle)
        self.title_color_ani.start()

        self._onTextEdited("")


class SiSpinBox(SiLabeledLineEdit):
    def __init__(self, parent: T_WidgetParent = None, title: str = "Untitled Edit Box") -> None:
        super().__init__(parent)

        self._single_step = 1
        self._value = 0
        self._minimum = 0
        self._maximum = 99

        self.setValue(0)
        self.setValidator(QIntValidator(self))

        self.button_increase = SiFlatButton(self)
        self.button_increase.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_caret_up_filled", "#F7A7C7"))
        self.button_increase.style_data.button_color = QColor("#42353f")
        self.button_increase.setIconSize(QSize(12, 12))
        self.button_increase.setFixedSize(20, 20)
        self.button_increase.setAutoRepeat(True)
        self.button_increase.clicked.connect(self.stepForth)

        self.button_decrease = SiFlatButton(self)
        self.button_decrease.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_caret_down_filled", "#AEE5E8"))
        self.button_decrease.style_data.button_color = QColor("#3a3f44")
        self.button_decrease.setIconSize(QSize(12, 12))
        self.button_decrease.setFixedSize(20, 20)
        self.button_decrease.setAutoRepeat(True)
        self.button_decrease.clicked.connect(self.stepBack)

        self.button_container = SiDenseContainer(self, SiDenseContainer.LeftToRight)
        self.button_container.setCursor(Qt.CursorShape.ArrowCursor)
        self.button_container.addWidget(self.button_decrease, Qt.RightEdge)
        self.button_container.addWidget(self.button_increase, Qt.RightEdge)
        self.button_container.layout().setContentsMargins(11, 0, 11, 0)
        self.button_container.layout().setSpacing(6)
        self.button_container.setFixedWidth(68)
        self.button_container.stretchWidget().hide()

        self.editingFinished.connect(self._onEditingFinished)

    def _initStyleSheet(self) -> None:
        self.setStyleSheet(
            "QLineEdit {"
            "     selection-background-color: #493F4E;"
            "     background-color: transparent;"
            f"    color: {self.style_data.text_color.name()};"
            "     border: 0px;"
            f"    padding-top: 22px;"
            "     padding-bottom: 1px;"
            "     padding-right: 68px;"
            "     padding-left: 15px;"
            "}"
        )

    def _onEditingFinished(self):
        self.setValue(int(self.text()))

    def singleStep(self):
        return self._single_step

    def setSingleStep(self, step):
        self._single_step = step

    def minimum(self):
        return self._minimum

    def setMinimum(self, minimum):
        self._minimum = minimum

    def maximum(self):
        return self._maximum

    def setMaximum(self, maximum):
        self._maximum = maximum

    def value(self):
        return self._value

    def setValue(self, value):
        self._value = min(self._maximum, max(value, self._minimum))
        self.setText(str(int(self._value)))

    def stepForth(self):
        self.setValue(self._value + self._single_step)

    def stepBack(self):
        self.setValue(self._value - self._single_step)

    def stepBy(self, step):
        self.setValue(self._value + step)

    def resizeEvent(self, a0):
        super().resizeEvent(a0)
        self.button_container.setGeometry(a0.size().width() - self.button_container.width(), 22,
                                          self.button_container.width(), a0.size().height() - 22)

    def wheelEvent(self, a0):
        super().wheelEvent(a0)
        if a0.angleDelta().y() > 0:
            self.stepForth()
            self.button_increase.flash()
        elif a0.angleDelta().y() < 0:
            self.stepBack()
            self.button_decrease.flash()
        a0.accept()

    def keyPressEvent(self, a0):
        super().keyPressEvent(a0)
        if a0.key() == Qt.Key_Up:
            self.stepForth()
            self.button_increase.flash()
        elif a0.key() == Qt.Key_Down:
            self.stepBack()
            self.button_decrease.flash()
        a0.accept()


class SiDoubleSpinBox(SiSpinBox):
    def __init__(self, parent: T_WidgetParent = None, title: str = "Untitled Edit Box") -> None:
        super().__init__(parent)

        self.setValidator(QDoubleValidator(self))

    @staticmethod
    def _double(value) -> float:
        return round(float(value), 10)

    def _onEditingFinished(self):
        self.setValue(float(self.text()))

    def setValue(self, value):
        self._value = min(self._maximum, max(value, self._minimum))
        self.setText(str(self._double(self._value)))
