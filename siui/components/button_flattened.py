# NOTE This is the refactor of button component. It's working in progress. It will
# replace button once it's done. Now it's draft, code may be ugly and verbose temporarily.
from __future__ import annotations

import random
from dataclasses import dataclass

from PyQt5.QtCore import QEvent, QRect, QRectF, QSize, Qt, QTimer, pyqtSignal, pyqtProperty, QObject
from PyQt5.QtGui import QColor, QFontMetrics, QIcon, QLinearGradient, QPainter, QPainterPath, QPaintEvent, QPixmap
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QPushButton, QWidget

from siui.core import GlobalFont, SiColor, SiExpAnimation, SiGlobal
from siui.core.animation import SiExpAnimationRefactor
from siui.gui import SiFont


@dataclass
class ButtonStyleData:
    idle_color = SiColor.toArray("#00baadc7")
    hover_color = SiColor.toArray("#1abaadc7")
    click_color = SiColor.toArray("#50baadc7")
    button_color = SiColor.toArray("#4C4554", "rgba")
    border_radius: int = 7
    icon_text_gap: int = 4


@dataclass
class FlatButtonStyleData(ButtonStyleData):
    pass


@dataclass
class PushButtonStyleData(ButtonStyleData):
    background_color = SiColor.toArray("#2d2932", "rgba")
    border_inner_radius: int = 4
    border_height: int = 3


@dataclass
class ProgressPushButtonStyleData(PushButtonStyleData):
    progress_color = SiColor.toArray("#806799", "rgba")
    complete_color = SiColor.toArray("#519868", "rgba")


@dataclass
class LongPressButtonStyleData(PushButtonStyleData):
    progress_color = SiColor.toArray("#DA3462", "rgba")
    button_color = SiColor.toArray("#932a48", "rgba")
    background_color = SiColor.toArray("#642d41", "rgba")
    click_color = SiColor.toArray("#40FFFFFF")


@dataclass
class ToggleButtonStyleData(ButtonStyleData):
    toggled_text_color = SiColor.toArray("#DFDFDF", "rgba")
    toggled_button_color = SiColor.toArray("#519868", "rgba")


class ABCButton(QPushButton):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.style_data = None

        self.highlight_ani = SiExpAnimation(self)
        self.highlight_ani.init(1/8, 0.2, SiColor.toArray("#00FFFFFF"), SiColor.toArray("#00FFFFFF"))
        self.highlight_ani.ticked.connect(self._onAnimationTicked)

        self.clicked.connect(self._onButtonClicked)

    def flash(self) -> None:
        self.highlight_ani.setCurrent(self.style_data.click_color)
        self.highlight_ani.try_to_start()

    def setToolTip(self, tooltip: str) -> None:
        super().setToolTip(tooltip)
        self._updateToolTip()

    def setIconTextGap(self, gap: int) -> None:
        self.style_data.icon_text_gap = gap
        self.update()

    def setBorderRadius(self, r: int) -> None:
        self.style_data.border_radius = r
        self.update()

    def setButtonColor(self, code: str) -> None:
        self.style_data.button_color = SiColor.toArray(code, "rgba")
        self.update()

    def setSvgIcon(self, svg_data: bytes) -> None:
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        svg_renderer = QSvgRenderer(svg_data)
        svg_renderer.render(painter)
        painter.end()
        self.setIcon(QIcon(pixmap))
        self.update()

    def sizeHint(self) -> QSize:
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(self.text())
        text_height = font_metrics.height()
        icon_width = self.iconSize().width() if not self.icon().isNull() else 0
        icon_height = self.iconSize().height() if not self.icon().isNull() else 0
        gap = self.style_data.icon_text_gap if text_width > 0 and icon_width > 0 else 0

        preferred_width = text_width + icon_width + gap + 32
        preferred_height = max(32, text_height, icon_height)
        return QSize(preferred_width, preferred_height)

    @property
    def styleData(self) -> PushButtonStyleData:
        return self.style_data

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

    def _updateToolTip(self) -> None:
        tool_tip_window = SiGlobal.siui.windows.get("TOOL_TIP")
        if tool_tip_window is not None and tool_tip_window.nowInsideOf() == self:
            tool_tip_window.setText(self.toolTip())

    def _onAnimationTicked(self, _) -> None:
        raise NotImplementedError()

    def _onButtonClicked(self) -> None:
        raise NotImplementedError()

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


class SiButtonStyleBase(QObject):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        print(123)


class SiPushButtonRefactor(QPushButton, SiButtonStyleBase):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._my_color = QColor(255, 255, 255, 0)

        self.style_data = PushButtonStyleData()
        self.style_data.idle_color = SiColor.toArray("#00baadc7", "rgba")
        self.style_data.hover_color = SiColor.toArray("#1abaadc7", "rgba")
        self.style_data.click_color = SiColor.toArray("#50baadc7", "rgba")

        self.highlight_ani = SiExpAnimationRefactor(self, "my_color")
        self.highlight_ani.init(1/8, 0.2, SiColor.toArray("#FFFFFF00"), SiColor.toArray("#FFFFFF00"))

        self._initStyle()
        self.clicked.connect(self._onButtonClicked)

    @pyqtProperty(QColor)
    def my_color(self):
        return self._my_color

    @my_color.setter
    def my_color(self, value: QColor):
        self._my_color = value
        self._onAnimationTicked(value)

    def flash(self) -> None:
        self.highlight_ani.setCurrentValue(self.style_data.click_color)
        self.highlight_ani.start()

    def setToolTip(self, tooltip: str) -> None:
        super().setToolTip(tooltip)
        self._updateToolTip()

    def setIconTextGap(self, gap: int) -> None:
        self.style_data.icon_text_gap = gap
        self.update()

    def setBorderRadius(self, r: int) -> None:
        self.style_data.border_radius = r
        self.update()

    def setButtonColor(self, code: str) -> None:
        self.style_data.button_color = SiColor.toArray(code, "rgba")
        self.update()

    def setSvgIcon(self, svg_data: bytes) -> None:
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        svg_renderer = QSvgRenderer(svg_data)
        svg_renderer.render(painter)
        painter.end()
        self.setIcon(QIcon(pixmap))
        self.update()

    def sizeHint(self) -> QSize:
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(self.text())
        text_height = font_metrics.height()
        icon_width = self.iconSize().width() if not self.icon().isNull() else 0
        icon_height = self.iconSize().height() if not self.icon().isNull() else 0
        gap = self.style_data.icon_text_gap if text_width > 0 and icon_width > 0 else 0

        preferred_width = text_width + icon_width + gap + 32
        preferred_height = max(32, text_height, icon_height)
        return QSize(preferred_width, preferred_height)

    @property
    def styleData(self) -> PushButtonStyleData:
        return self.style_data

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

    def _updateToolTip(self) -> None:
        tool_tip_window = SiGlobal.siui.windows.get("TOOL_TIP")
        if tool_tip_window is not None and tool_tip_window.nowInsideOf() == self:
            tool_tip_window.setText(self.toolTip())

    def event(self, event):
        if event.type() == QEvent.ToolTip:
            return True  # 忽略工具提示事件
        return super().event(event)

    def _initStyle(self):
        self.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
        self.setStyleSheet("color: #DFDFDF;")
        self.setIconSize(QSize(20, 20))

    @classmethod
    def withText(cls, text: str, parent: QWidget | None = None) -> "SiPushButton":
        obj = cls(parent)
        obj.setText(text)
        return obj

    @classmethod
    def withIcon(cls, icon: QIcon, parent: QWidget | None = None) -> "SiPushButton":
        obj = cls(parent)
        obj.setIcon(icon)
        return obj

    @classmethod
    def withTextAndIcon(cls, text: str, icon: str, parent: QWidget | None = None) -> "SiPushButton":
        obj = cls(parent)
        obj.setText(text)
        obj.setIcon(QIcon(icon))
        return obj

    @property
    def bottomBorderHeight(self) -> int:
        return self.style_data.border_height

    def setBackgroundColor(self, code: str) -> None:
        self.style_data.background_color = SiColor.toArray(code, "rgba")
        self.update()

    def setBorderInnerRadius(self, r: int) -> None:
        self.style_data.border_inner_radius = r
        self.update()

    def setBorderHeight(self, h: int) -> None:
        self.style_data.border_height = h
        self.update()

    def _drawBackgroundPath(self, rect: QRect) -> QPainterPath:
        radius = self.style_data.border_radius
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, rect.width(), rect.height()), radius, radius)
        return path

    def _drawBackgroundRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(QColor(*self.style_data.background_color))
        painter.drawPath(self._drawBackgroundPath(rect))

    def _drawButtonPath(self, rect: QRect) -> QPainterPath:
        radius = self.style_data.border_inner_radius
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, rect.width(), rect.height() - self.bottomBorderHeight), radius, radius)
        return path

    def _drawButtonRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(QColor(*self.style_data.button_color))
        painter.drawPath(self._drawButtonPath(rect))

    def _drawHighLightRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(self.property("my_color"))
        painter.drawPath(self._drawButtonPath(rect))

    def _drawTextRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setPen(self.palette().text().color())
        painter.setFont(self.font())
        painter.drawText(rect, Qt.AlignCenter, self.text())

    def _drawPixmapRect(self, painter: QPainter, rect: QRectF) -> None:
        painter.drawPixmap(rect, self.icon().pixmap(64, 64))

    def _onAnimationTicked(self, _) -> None:
        self.update()

    def _onButtonClicked(self) -> None:
        self.flash()

    def textRectAndIconRect(self) -> (QRectF, QRect):
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(self.text())
        icon_width = self.iconSize().width() if not self.icon().isNull() else 0
        icon_height = self.iconSize().height() if not self.icon().isNull() else 0
        gap = self.style_data.icon_text_gap if text_width > 0 and icon_width > 0 else 0

        text_rect = QRectF((self.width() - icon_width - text_width - gap) / 2 + icon_width + gap,
                           0,
                           text_width,
                           self.height() - self.style_data.border_height - 1)
        pixmap_rect = QRect((self.width() - icon_width - text_width - gap) // 2,
                            ((self.height() - self.style_data.border_height) - icon_height) // 2,
                            icon_width,
                            icon_height)

        return text_rect, pixmap_rect

    def enterEvent(self, event) -> None:
        super().enterEvent(event)
        self.highlight_ani.setEndValue(self.style_data.hover_color)
        self.highlight_ani.start()
        self._showToolTip()
        self._updateToolTip()

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)
        self.highlight_ani.setEndValue(self.style_data.idle_color)
        self.highlight_ani.start()
        self._hideToolTip()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        rect = self.rect()
        text_rect, icon_rect = self.textRectAndIconRect()
        self._drawBackgroundRect(painter, rect)
        self._drawButtonRect(painter, rect)
        self._drawHighLightRect(painter, rect)
        self._drawTextRect(painter, text_rect)
        self._drawPixmapRect(painter, icon_rect)


class SiProgressPushButton(QPushButton):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.style_data = ProgressPushButtonStyleData()
        self.progress_ = 0

        self.progress_ani = SiExpAnimation(self)
        self.progress_ani.init(1/6, 0.005, 0, 0)
        self.progress_ani.ticked.connect(lambda _: self.update())

        self.progress_color_ani = SiExpAnimation(self)
        self.progress_color_ani.init(1/8, 0.01, self.style_data.progress_color, self.style_data.progress_color)
        self.progress_color_ani.ticked.connect(lambda _: self.update())

        self.highlight_ani = SiExpAnimation(self)
        self.highlight_ani.init(1/8, 0.2, SiColor.toArray("#00FFFFFF"), SiColor.toArray("#00FFFFFF"))
        self.highlight_ani.ticked.connect(self._onAnimationTicked)

        self.clicked.connect(self._onButtonClicked)

        self._initStyle()

    def flash(self) -> None:
        self.highlight_ani.setCurrent(self.style_data.click_color)
        self.highlight_ani.try_to_start()

    def setToolTip(self, tooltip: str) -> None:
        super().setToolTip(tooltip)
        self._updateToolTip()

    def setIconTextGap(self, gap: int) -> None:
        self.style_data.icon_text_gap = gap
        self.update()

    def setBorderRadius(self, r: int) -> None:
        self.style_data.border_radius = r
        self.update()

    def setButtonColor(self, code: str) -> None:
        self.style_data.button_color = SiColor.toArray(code, "rgba")
        self.update()

    def setSvgIcon(self, svg_data: bytes) -> None:
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        svg_renderer = QSvgRenderer(svg_data)
        svg_renderer.render(painter)
        painter.end()
        self.setIcon(QIcon(pixmap))
        self.update()

    def sizeHint(self) -> QSize:
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(self.text())
        text_height = font_metrics.height()
        icon_width = self.iconSize().width() if not self.icon().isNull() else 0
        icon_height = self.iconSize().height() if not self.icon().isNull() else 0
        gap = self.style_data.icon_text_gap if text_width > 0 and icon_width > 0 else 0

        preferred_width = text_width + icon_width + gap + 32
        preferred_height = max(32, text_height, icon_height)
        return QSize(preferred_width, preferred_height)

    @property
    def styleData(self) -> PushButtonStyleData:
        return self.style_data

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

    def _updateToolTip(self) -> None:
        tool_tip_window = SiGlobal.siui.windows.get("TOOL_TIP")
        if tool_tip_window is not None and tool_tip_window.nowInsideOf() == self:
            tool_tip_window.setText(self.toolTip())

    def event(self, event):
        if event.type() == QEvent.ToolTip:
            return True  # 忽略工具提示事件
        return super().event(event)

    def _initStyle(self):
        self.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
        self.setStyleSheet("color: #DFDFDF;")
        self.setIconSize(QSize(20, 20))

    @classmethod
    def withText(cls, text: str, parent: QWidget | None = None) -> "SiPushButton":
        obj = cls(parent)
        obj.setText(text)
        return obj

    @classmethod
    def withIcon(cls, icon: QIcon, parent: QWidget | None = None) -> "SiPushButton":
        obj = cls(parent)
        obj.setIcon(icon)
        return obj

    @classmethod
    def withTextAndIcon(cls, text: str, icon: str, parent: QWidget | None = None) -> "SiPushButton":
        obj = cls(parent)
        obj.setText(text)
        obj.setIcon(QIcon(icon))
        return obj

    @property
    def bottomBorderHeight(self) -> int:
        return self.style_data.border_height

    def setBackgroundColor(self, code: str) -> None:
        self.style_data.background_color = SiColor.toArray(code, "rgba")
        self.update()

    def setBorderInnerRadius(self, r: int) -> None:
        self.style_data.border_inner_radius = r
        self.update()

    def setBorderHeight(self, h: int) -> None:
        self.style_data.border_height = h
        self.update()

    def _drawBackgroundPath(self, rect: QRect) -> QPainterPath:
        radius = self.style_data.border_radius
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, rect.width(), rect.height()), radius, radius)
        return path

    def _drawBackgroundRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(QColor(*self.style_data.background_color))
        painter.drawPath(self._drawBackgroundPath(rect))

    def _drawButtonPath(self, rect: QRect) -> QPainterPath:
        radius = self.style_data.border_inner_radius
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, rect.width(), rect.height() - self.bottomBorderHeight), radius, radius)
        return path

    def _drawHighLightRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(QColor(SiColor.toCode(self.highlight_ani.current_)))
        painter.drawPath(self._drawButtonPath(rect))

    def _drawTextRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setPen(self.palette().text().color())
        painter.setFont(self.font())
        painter.drawText(rect, Qt.AlignCenter, self.text())

    def _drawPixmapRect(self, painter: QPainter, rect: QRectF) -> None:
        painter.drawPixmap(rect, self.icon().pixmap(64, 64))

    def _onAnimationTicked(self, _) -> None:
        self.update()

    def _onButtonClicked(self) -> None:
        self.flash()

    def textRectAndIconRect(self) -> (QRectF, QRect):
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(self.text())
        icon_width = self.iconSize().width() if not self.icon().isNull() else 0
        icon_height = self.iconSize().height() if not self.icon().isNull() else 0
        gap = self.style_data.icon_text_gap if text_width > 0 and icon_width > 0 else 0

        text_rect = QRectF((self.width() - icon_width - text_width - gap) / 2 + icon_width + gap,
                           0,
                           text_width,
                           self.height() - self.style_data.border_height - 1)
        pixmap_rect = QRect((self.width() - icon_width - text_width - gap) // 2,
                            ((self.height() - self.style_data.border_height) - icon_height) // 2,
                            icon_width,
                            icon_height)

        return text_rect, pixmap_rect

    def enterEvent(self, event) -> None:
        super().enterEvent(event)
        self.highlight_ani.setTarget(self.style_data.hover_color)
        self.highlight_ani.start()
        self._showToolTip()
        self._updateToolTip()

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)
        self.highlight_ani.setTarget(self.style_data.idle_color)
        self.highlight_ani.start()
        self._hideToolTip()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        rect = self.rect()
        text_rect, icon_rect = self.textRectAndIconRect()
        self._drawBackgroundRect(painter, rect)
        self._drawButtonRect(painter, rect)
        self._drawHighLightRect(painter, rect)
        self._drawTextRect(painter, text_rect)
        self._drawPixmapRect(painter, icon_rect)

    @property
    def progress(self) -> float:
        return self.progress_

    def setProgress(self, p: float, ani: bool = True) -> None:
        self.progress_ = max(0.0, min(p, 1.0))
        self._updateProgress(ani)
        self._updateCompleteState()
        self.update()

    def _updateProgress(self, ani: bool) -> None:
        if ani is True:
            self.progress_ani.setTarget(self.progress_)
            self.progress_ani.start()
        else:
            self.progress_ani.setTarget(self.progress_)
            self.progress_ani.setCurrent(self.progress_)
            self.progress_ani.stop()

    def _updateCompleteState(self) -> None:
        if self.progress_ == 1.0:
            self.progress_color_ani.setTarget(self.style_data.complete_color)
            self.progress_color_ani.start()
        else:
            self.progress_color_ani.setTarget(self.style_data.progress_color)
            self.progress_color_ani.start()

    def setProgressColor(self, code: str) -> None:
        self.style_data.progress_color = SiColor.toArray(code, "rgba")
        self.update()

    def _drawButtonRect(self, painter: QPainter, rect: QRect) -> None:
        p = min(self.progress_ani.current_, 1)  # prevent progress exceeding caused by using animation.
        gradient = QLinearGradient(rect.left(), rect.top(), rect.right(), rect.top())
        gradient.setColorAt(p - 0.0001, QColor(*self.progress_color_ani.current_))
        gradient.setColorAt(p,          QColor(*self.style_data.button_color))
        painter.setBrush(gradient)
        painter.drawPath(self._drawButtonPath(rect))


class SiLongPressButtonRefactor(QPushButton):
    longPressed = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.style_data = LongPressButtonStyleData()
        self.progress_ = 0

        self.progress_ani = SiExpAnimation(self)
        self.progress_ani.init(-1/16, 0.12, 0, 0)
        self.progress_ani.ticked.connect(lambda _: self.update())

        self.go_backwards_timer = QTimer(self)
        self.go_backwards_timer.setSingleShot(True)
        self.go_backwards_timer.setInterval(500)
        self.go_backwards_timer.timeout.connect(self._goBackwards)

        self.mouse_pressed_timer = QTimer(self)
        self.mouse_pressed_timer.setInterval(1000//60)
        self.mouse_pressed_timer.timeout.connect(self._onMousePressed)

        self.highlight_ani = SiExpAnimation(self)
        self.highlight_ani.init(1/8, 0.2, SiColor.toArray("#00FFFFFF"), SiColor.toArray("#00FFFFFF"))
        self.highlight_ani.ticked.connect(self._onAnimationTicked)

        self._initStyle()
        self.clicked.connect(self._onButtonClicked)

    def flash(self) -> None:
        self.highlight_ani.setCurrent(self.style_data.click_color)
        self.highlight_ani.try_to_start()

    def setToolTip(self, tooltip: str) -> None:
        super().setToolTip(tooltip)
        self._updateToolTip()

    def setIconTextGap(self, gap: int) -> None:
        self.style_data.icon_text_gap = gap
        self.update()

    def setBorderRadius(self, r: int) -> None:
        self.style_data.border_radius = r
        self.update()

    def setButtonColor(self, code: str) -> None:
        self.style_data.button_color = SiColor.toArray(code, "rgba")
        self.update()

    def setSvgIcon(self, svg_data: bytes) -> None:
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        svg_renderer = QSvgRenderer(svg_data)
        svg_renderer.render(painter)
        painter.end()
        self.setIcon(QIcon(pixmap))
        self.update()

    def sizeHint(self) -> QSize:
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(self.text())
        text_height = font_metrics.height()
        icon_width = self.iconSize().width() if not self.icon().isNull() else 0
        icon_height = self.iconSize().height() if not self.icon().isNull() else 0
        gap = self.style_data.icon_text_gap if text_width > 0 and icon_width > 0 else 0

        preferred_width = text_width + icon_width + gap + 32
        preferred_height = max(32, text_height, icon_height)
        return QSize(preferred_width, preferred_height)

    @property
    def styleData(self) -> PushButtonStyleData:
        return self.style_data

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

    def _updateToolTip(self) -> None:
        tool_tip_window = SiGlobal.siui.windows.get("TOOL_TIP")
        if tool_tip_window is not None and tool_tip_window.nowInsideOf() == self:
            tool_tip_window.setText(self.toolTip())

    def event(self, event):
        if event.type() == QEvent.ToolTip:
            return True  # 忽略工具提示事件
        return super().event(event)

    def _initStyle(self):
        self.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
        self.setStyleSheet("color: #DFDFDF;")
        self.setIconSize(QSize(20, 20))

    @classmethod
    def withText(cls, text: str, parent: QWidget | None = None) -> "SiPushButton":
        obj = cls(parent)
        obj.setText(text)
        return obj

    @classmethod
    def withIcon(cls, icon: QIcon, parent: QWidget | None = None) -> "SiPushButton":
        obj = cls(parent)
        obj.setIcon(icon)
        return obj

    @classmethod
    def withTextAndIcon(cls, text: str, icon: str, parent: QWidget | None = None) -> "SiPushButton":
        obj = cls(parent)
        obj.setText(text)
        obj.setIcon(QIcon(icon))
        return obj

    @property
    def bottomBorderHeight(self) -> int:
        return self.style_data.border_height

    def setBackgroundColor(self, code: str) -> None:
        self.style_data.background_color = SiColor.toArray(code, "rgba")
        self.update()

    def setBorderInnerRadius(self, r: int) -> None:
        self.style_data.border_inner_radius = r
        self.update()

    def setBorderHeight(self, h: int) -> None:
        self.style_data.border_height = h
        self.update()

    def _drawBackgroundPath(self, rect: QRect) -> QPainterPath:
        radius = self.style_data.border_radius
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, rect.width(), rect.height()), radius, radius)
        return path

    def _drawBackgroundRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(QColor(*self.style_data.background_color))
        painter.drawPath(self._drawBackgroundPath(rect))

    def _drawButtonPath(self, rect: QRect) -> QPainterPath:
        radius = self.style_data.border_inner_radius
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, rect.width(), rect.height() - self.bottomBorderHeight), radius, radius)
        return path

    def _drawButtonRect(self, painter: QPainter, rect: QRect) -> None:
        p = min(self.progress_ani.current_, 1)  # prevent progress exceeding caused by using animation.
        gradient = QLinearGradient(rect.left(), rect.top(), rect.right(), rect.top())
        gradient.setColorAt(p - 0.0001, QColor(*self.style_data.progress_color))
        gradient.setColorAt(p,          QColor(*self.style_data.button_color))
        painter.setBrush(gradient)
        painter.drawPath(self._drawButtonPath(rect))

    def _drawHighLightRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(QColor(SiColor.toCode(self.highlight_ani.current_)))
        painter.drawPath(self._drawButtonPath(rect))

    def _drawTextRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setPen(self.palette().text().color())
        painter.setFont(self.font())
        painter.drawText(rect, Qt.AlignCenter, self.text())

    def _drawPixmapRect(self, painter: QPainter, rect: QRectF) -> None:
        painter.drawPixmap(rect, self.icon().pixmap(64, 64))

    def _onAnimationTicked(self, _) -> None:
        self.update()

    def _onButtonClicked(self) -> None:
        pass  # disable flashes on mouse click

    def textRectAndIconRect(self) -> (QRectF, QRect):
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(self.text())
        icon_width = self.iconSize().width() if not self.icon().isNull() else 0
        icon_height = self.iconSize().height() if not self.icon().isNull() else 0
        gap = self.style_data.icon_text_gap if text_width > 0 and icon_width > 0 else 0

        text_rect = QRectF((self.width() - icon_width - text_width - gap) / 2 + icon_width + gap,
                           0,
                           text_width,
                           self.height() - self.style_data.border_height - 1)
        pixmap_rect = QRect((self.width() - icon_width - text_width - gap) // 2,
                            ((self.height() - self.style_data.border_height) - icon_height) // 2,
                            icon_width,
                            icon_height)

        return text_rect, pixmap_rect

    def enterEvent(self, event) -> None:
        super().enterEvent(event)
        self.highlight_ani.setTarget(self.style_data.hover_color)
        self.highlight_ani.start()
        self._showToolTip()
        self._updateToolTip()

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)
        self.highlight_ani.setTarget(self.style_data.idle_color)
        self.highlight_ani.start()
        self._hideToolTip()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        rect = self.rect()
        text_rect, icon_rect = self.textRectAndIconRect()
        self._drawBackgroundRect(painter, rect)
        self._drawButtonRect(painter, rect)
        self._drawHighLightRect(painter, rect)
        self._drawTextRect(painter, text_rect)
        self._drawPixmapRect(painter, icon_rect)

    @property
    def progress(self) -> float:
        return self.progress_

    def setProgress(self, p: float, ani: bool = True) -> None:
        self.progress_ = max(0.0, min(p, 1.0))
        self._updateProgress(ani)
        self.update()

    def _stepLength(self) -> float:
        return (1 - self.progress_) / 16 + 0.001

    def _onMousePressed(self) -> None:
        self.setProgress(self.progress_ + self._stepLength(), ani=False)

    def _updateProgress(self, ani: bool) -> None:
        if ani is True:
            self.progress_ani.setTarget(self.progress_)
            self.progress_ani.start()
        else:
            self.progress_ani.setTarget(self.progress_)
            self.progress_ani.setCurrent(self.progress_)
            self.progress_ani.stop()

        if self.progress_ == 1.0:
            self.mouse_pressed_timer.stop()
            self.go_backwards_timer.stop()
            self.longPressed.emit()
            self._onLongPressed()
            self._goBackwards(200)

    def _onLongPressed(self) -> None:
        self.highlight_ani.setCurrent(self.style_data.click_color)
        self.highlight_ani.start()

    def _goBackwards(self, delay: int = 0) -> None:
        self.progress_ = 0
        self.progress_ani.setTarget(0)
        self.progress_ani.start(delay)

    def mousePressEvent(self, e) -> None:
        super().mousePressEvent(e)
        if self.progress_ani.isActive() is False and self.mouse_pressed_timer.isActive() is False:
            self.mouse_pressed_timer.start()
            self.go_backwards_timer.stop()

    def mouseReleaseEvent(self, e) -> None:
        super().mouseReleaseEvent(e)
        self.mouse_pressed_timer.stop()
        self.go_backwards_timer.start()


class SiFlatButton(QPushButton):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.style_data = FlatButtonStyleData()

        self.highlight_ani = SiExpAnimation(self)
        self.highlight_ani.init(1/8, 0.2, SiColor.toArray("#00FFFFFF"), SiColor.toArray("#00FFFFFF"))
        self.highlight_ani.ticked.connect(self._onAnimationTicked)

        self.clicked.connect(self._onButtonClicked)

        self._initStyle()

    def flash(self) -> None:
        self.highlight_ani.setCurrent(self.style_data.click_color)
        self.highlight_ani.try_to_start()

    def setToolTip(self, tooltip: str) -> None:
        super().setToolTip(tooltip)
        self._updateToolTip()

    def setIconTextGap(self, gap: int) -> None:
        self.style_data.icon_text_gap = gap
        self.update()

    def setBorderRadius(self, r: int) -> None:
        self.style_data.border_radius = r
        self.update()

    def setButtonColor(self, code: str) -> None:
        self.style_data.button_color = SiColor.toArray(code, "rgba")
        self.update()

    def setSvgIcon(self, svg_data: bytes) -> None:
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        svg_renderer = QSvgRenderer(svg_data)
        svg_renderer.render(painter)
        painter.end()
        self.setIcon(QIcon(pixmap))
        self.update()

    def sizeHint(self) -> QSize:
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(self.text())
        text_height = font_metrics.height()
        icon_width = self.iconSize().width() if not self.icon().isNull() else 0
        icon_height = self.iconSize().height() if not self.icon().isNull() else 0
        gap = self.style_data.icon_text_gap if text_width > 0 and icon_width > 0 else 0

        preferred_width = text_width + icon_width + gap + 32
        preferred_height = max(32, text_height, icon_height)
        return QSize(preferred_width, preferred_height)

    @property
    def styleData(self) -> PushButtonStyleData:
        return self.style_data

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

    def _updateToolTip(self) -> None:
        tool_tip_window = SiGlobal.siui.windows.get("TOOL_TIP")
        if tool_tip_window is not None and tool_tip_window.nowInsideOf() == self:
            tool_tip_window.setText(self.toolTip())

    def _onAnimationTicked(self, _) -> None:
        self.update()

    def _onButtonClicked(self) -> None:
        self.highlight_ani.setCurrent(self.style_data.click_color)
        self.highlight_ani.start()

    def event(self, event):
        if event.type() == QEvent.ToolTip:
            return True  # 忽略工具提示事件
        return super().event(event)

    def _initStyle(self):
        self.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
        self.setStyleSheet("color: #DFDFDF;")
        self.setIconSize(QSize(20, 20))

    def _drawButtonPath(self, rect: QRect) -> QPainterPath:
        radius = self.style_data.border_radius
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, rect.width(), rect.height()), radius, radius)
        return path

    def _drawButtonRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(QColor(*self.style_data.button_color))
        painter.drawPath(self._drawButtonPath(rect))

    def _drawHighLightRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(QColor(SiColor.toCode(self.highlight_ani.current_)))
        painter.drawPath(self._drawButtonPath(rect))

    def _drawTextRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setPen(self.palette().text().color())
        painter.setFont(self.font())
        painter.drawText(rect, Qt.AlignCenter, self.text())

    def _drawPixmapRect(self, painter: QPainter, rect: QRectF) -> None:
        painter.drawPixmap(rect, self.icon().pixmap(64, 64))

    def textRectAndIconRect(self) -> (QRectF, QRect):
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(self.text())
        icon_width = self.iconSize().width() if not self.icon().isNull() else 0
        icon_height = self.iconSize().height() if not self.icon().isNull() else 0
        gap = self.style_data.icon_text_gap if text_width > 0 and icon_width > 0 else 0

        text_rect = QRectF((self.width() - icon_width - text_width - gap) / 2 + icon_width + gap,
                           0,
                           text_width,
                           self.height())
        pixmap_rect = QRect((self.width() - icon_width - text_width - gap) // 2,
                            (self.height() - icon_height) // 2,
                            icon_width,
                            icon_height)

        return text_rect, pixmap_rect

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        rect = self.rect()
        text_rect, icon_rect = self.textRectAndIconRect()
        self._drawButtonRect(painter, rect)
        self._drawHighLightRect(painter, rect)
        self._drawTextRect(painter, text_rect)
        self._drawPixmapRect(painter, icon_rect)

    def enterEvent(self, event) -> None:
        super().enterEvent(event)
        self.highlight_ani.setTarget(self.style_data.hover_color)
        self.highlight_ani.start()
        self._showToolTip()
        self._updateToolTip()

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)
        self.highlight_ani.setTarget(self.style_data.idle_color)
        self.highlight_ani.start()
        self._hideToolTip()


class SiToggleButtonRefactor(QPushButton):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setCheckable(True)
        self.style_data = ToggleButtonStyleData()

        self.toggle_btn_color_ani = SiExpAnimation(self)
        self.toggle_btn_color_ani.init(1/8, 0.01, self.style_data.button_color, self.style_data.button_color)
        self.toggle_btn_color_ani.ticked.connect(lambda _: self.update())

        self.toggle_text_color_ani = SiExpAnimation(self)
        self.toggle_text_color_ani.init(1/8, 0.01, (223, 223, 223, 255), (223, 223, 223, 255))
        self.toggle_text_color_ani.ticked.connect(lambda _: self.update())

        self.highlight_ani = SiExpAnimation(self)
        self.highlight_ani.init(1/8, 0.2, SiColor.toArray("#00FFFFFF"), SiColor.toArray("#00FFFFFF"))
        self.highlight_ani.ticked.connect(self._onAnimationTicked)

        self.clicked.connect(self._onButtonClicked)
        self.toggled.connect(self._onButtonToggled)

        self._initStyle()

    def flash(self) -> None:
        self.highlight_ani.setCurrent(self.style_data.click_color)
        self.highlight_ani.try_to_start()

    def setToolTip(self, tooltip: str) -> None:
        super().setToolTip(tooltip)
        self._updateToolTip()

    def setIconTextGap(self, gap: int) -> None:
        self.style_data.icon_text_gap = gap
        self.update()

    def setBorderRadius(self, r: int) -> None:
        self.style_data.border_radius = r
        self.update()

    def setButtonColor(self, code: str) -> None:
        self.style_data.button_color = SiColor.toArray(code, "rgba")
        self.update()

    def setSvgIcon(self, svg_data: bytes) -> None:
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        svg_renderer = QSvgRenderer(svg_data)
        svg_renderer.render(painter)
        painter.end()
        self.setIcon(QIcon(pixmap))
        self.update()

    def sizeHint(self) -> QSize:
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(self.text())
        text_height = font_metrics.height()
        icon_width = self.iconSize().width() if not self.icon().isNull() else 0
        icon_height = self.iconSize().height() if not self.icon().isNull() else 0
        gap = self.style_data.icon_text_gap if text_width > 0 and icon_width > 0 else 0

        preferred_width = text_width + icon_width + gap + 32
        preferred_height = max(32, text_height, icon_height)
        return QSize(preferred_width, preferred_height)

    @property
    def styleData(self) -> ToggleButtonStyleData:
        return self.style_data

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

    def _updateToolTip(self) -> None:
        tool_tip_window = SiGlobal.siui.windows.get("TOOL_TIP")
        if tool_tip_window is not None and tool_tip_window.nowInsideOf() == self:
            tool_tip_window.setText(self.toolTip())

    def _onAnimationTicked(self, _) -> None:
        self.update()

    def _onButtonClicked(self) -> None:
        self.highlight_ani.setCurrent(self.style_data.click_color)
        self.highlight_ani.start()

    def event(self, event):
        if event.type() == QEvent.ToolTip:
            return True  # 忽略工具提示事件
        return super().event(event)

    def _initStyle(self):
        self.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
        self.setStyleSheet("color: #DFDFDF;")
        self.setIconSize(QSize(20, 20))

    def _drawButtonPath(self, rect: QRect) -> QPainterPath:
        radius = self.style_data.border_radius
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, rect.width(), rect.height()), radius, radius)
        return path

    def _drawHighLightRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(QColor(SiColor.toCode(self.highlight_ani.current_)))
        painter.drawPath(self._drawButtonPath(rect))

    def _drawPixmapRect(self, painter: QPainter, rect: QRectF) -> None:
        painter.drawPixmap(rect, self.icon().pixmap(64, 64))

    def textRectAndIconRect(self) -> (QRectF, QRect):
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(self.text())
        icon_width = self.iconSize().width() if not self.icon().isNull() else 0
        icon_height = self.iconSize().height() if not self.icon().isNull() else 0
        gap = self.style_data.icon_text_gap if text_width > 0 and icon_width > 0 else 0

        text_rect = QRectF((self.width() - icon_width - text_width - gap) / 2 + icon_width + gap,
                           0,
                           text_width,
                           self.height())
        pixmap_rect = QRect((self.width() - icon_width - text_width - gap) // 2,
                            (self.height() - icon_height) // 2,
                            icon_width,
                            icon_height)

        return text_rect, pixmap_rect

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        rect = self.rect()
        text_rect, icon_rect = self.textRectAndIconRect()
        self._drawButtonRect(painter, rect)
        self._drawHighLightRect(painter, rect)
        self._drawTextRect(painter, text_rect)
        self._drawPixmapRect(painter, icon_rect)

    def enterEvent(self, event) -> None:
        super().enterEvent(event)
        self.highlight_ani.setTarget(self.style_data.hover_color)
        self.highlight_ani.start()
        self._showToolTip()
        self._updateToolTip()

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)
        self.highlight_ani.setTarget(self.style_data.idle_color)
        self.highlight_ani.start()
        self._hideToolTip()

    def setToggledButtonColor(self, code: str) -> None:
        self.style_data.toggled_button_color = SiColor.toArray(code, "rgba")
        self.update()

    def setToggledTextColor(self, code: str) -> None:
        self.style_data.toggled_text_color = SiColor.toArray(code, "rgba")
        self.update()

    def _onButtonToggled(self, state: bool) -> None:
        if state:
            self.toggle_btn_color_ani.setTarget(self.style_data.toggled_button_color)
            self.toggle_text_color_ani.setTarget(self.style_data.toggled_text_color)
            self.toggle_btn_color_ani.try_to_start()
            self.toggle_text_color_ani.try_to_start()
        else:
            self.toggle_btn_color_ani.setTarget(self.style_data.button_color)
            self.toggle_text_color_ani.setTarget(self.palette().text().color().getRgb())
            self.toggle_btn_color_ani.try_to_start()
            self.toggle_text_color_ani.try_to_start()

    def _drawButtonRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(QColor(*self.toggle_btn_color_ani.current_))
        painter.drawPath(self._drawButtonPath(rect))

    def _drawTextRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setPen(QColor(*self.toggle_text_color_ani.current_))
        painter.setFont(self.font())
        painter.drawText(rect, Qt.AlignCenter, self.text())
