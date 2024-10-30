# NOTE This is the refactor of button component. It's working in progress. It will
# replace button once it's done. Now it's draft, code may be ugly and verbose temporarily.
from __future__ import annotations

import random
from dataclasses import dataclass

from PyQt5.QtCore import QEvent, QRect, QRectF, QSize, Qt, QTimer
from PyQt5.QtGui import QColor, QFontMetrics, QIcon, QLinearGradient, QPainter, QPainterPath, QPaintEvent, QPixmap
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QPushButton, QWidget

from siui.core import GlobalFont, SiColor, SiExpAnimation, SiGlobal
from siui.gui import SiFont


@dataclass
class ButtonStyleData:
    idle_color = SiColor.toArray("#00baadc7")
    hover_color = SiColor.toArray("#1abaadc7")
    click_color = SiColor.toArray("#50baadc7")
    button_color = SiColor.toArray("#4C4554", "rgba")
    border_radius: int = 7
    icon_text_gap: int = 4


class ABCButton(QPushButton):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.style_data = None

        self.highlight_ani = SiExpAnimation(self)
        self.highlight_ani.setFactor(1/8)
        self.highlight_ani.setBias(0.2)
        self.highlight_ani.setTarget(SiColor.toArray("#00FFFFFF"))
        self.highlight_ani.setCurrent(SiColor.toArray("#00FFFFFF"))
        self.highlight_ani.ticked.connect(self._onAnimationTicked)
        self.clicked.connect(self._onButtonClicked)

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

    def sizeHint(self):
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

    def _onButtonClicked(self):
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


@dataclass
class PushButtonStyleData(ButtonStyleData):
    background_color = SiColor.toArray("#2d2932", "rgba")
    border_inner_radius: int = 4
    border_height: int = 3


class SiPushButtonRefactor(ABCButton):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.style_data = PushButtonStyleData()
        self._initStyle()

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
        self.highlight_ani.setCurrent(self.style_data.click_color)
        self.highlight_ani.start()

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


@dataclass
class FlatButtonStyleData(ButtonStyleData):
    pass


class SiFlatButton(ABCButton):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.style_data = FlatButtonStyleData()
        self._initStyle()

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

    def _onAnimationTicked(self, _) -> None:
        self.update()

    def _onButtonClicked(self) -> None:
        self.highlight_ani.setCurrent(self.style_data.click_color)
        self.highlight_ani.start()

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


@dataclass
class ProgressPushButtonStyleData(PushButtonStyleData):
    progress_color = SiColor.toArray("#806799", "rgba")


class SiProgressPushButton(SiPushButtonRefactor):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.style_data = ProgressPushButtonStyleData()
        self.progress_ = 0

        self.progress_ani = SiExpAnimation(self)
        self.progress_ani.setFactor(1/6)
        self.progress_ani.setBias(0.005)
        self.progress_ani.setTarget(0)
        self.progress_ani.setCurrent(0)
        self.progress_ani.ticked.connect(lambda _: self.update())

    @property
    def progress(self):
        return self.progress_

    def setProgress(self, p: float, ani: bool = True) -> None:
        p = max(0.0, min(p, 1.0))
        self.progress_ = p
        if ani is True:
            self.progress_ani.setTarget(p)
            self.progress_ani.start()
        else:
            self.progress_ani.setTarget(p)
            self.progress_ani.setCurrent(p)
            self.progress_ani.stop()
            self.update()

    def _drawButtonRect(self, painter: QPainter, rect: QRect) -> None:
        gradient = QLinearGradient(rect.left(), rect.top(), rect.right(), rect.top())
        gradient.setColorAt(self.progress_ani.current_ - 0.001, QColor(*self.style_data.progress_color))
        gradient.setColorAt(self.progress_ani.current_,         QColor(*self.style_data.button_color))
        painter.setBrush(gradient)
        painter.drawPath(self._drawButtonPath(rect))
