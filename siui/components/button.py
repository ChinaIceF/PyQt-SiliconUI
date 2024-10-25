# NOTE This is the refactor of button component. It's working in progress. It will
# replace button once it's done. Now it's draft, code may be ugly and verbose temporarily.
from __future__ import annotations

from dataclasses import dataclass

from PyQt5.QtCore import QEvent, QRect, QRectF, Qt
from PyQt5.QtGui import QColor, QIcon, QPainter, QPainterPath, QPaintEvent
from PyQt5.QtWidgets import QPushButton, QWidget

from siui.core import GlobalFont, SiColor, SiExpAnimation, SiGlobal
from siui.gui import SiFont


@dataclass
class PushButtonStyleData:
    idle_color = SiColor.toArray("#00FFFFFF")
    hover_color = SiColor.toArray("#10FFFFFF")
    click_color = SiColor.toArray("#40FFFFFF")
    background_color = SiColor.toArray("#2d2932", "rgba")
    button_color = SiColor.toArray("#4C4554", "rgba")
    border_radius: int = 4
    border_inner_radius: int = 3
    border_height: int = 3


class SiPushButtonRefactor(QPushButton):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.style_data = PushButtonStyleData()
        self._initStyle()

        self.animation = SiExpAnimation(self)
        self.animation.setFactor(1/8)
        self.animation.setBias(0.2)
        self.animation.setTarget(self.style_data.idle_color)
        self.animation.setCurrent(self.style_data.idle_color)
        self.animation.ticked.connect(self.animate)

        self.clicked.connect(self._onButtonClicked)

    def _initStyle(self):
        self.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
        self.setStyleSheet("color: #DFDFDF;")

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

    @property
    def styleData(self) -> PushButtonStyleData:
        return self.style_data

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
        painter.setBrush(QColor(SiColor.toCode(self.animation.current_)))
        painter.drawPath(self._drawButtonPath(rect))

    def _drawTextRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setPen(self.palette().text().color())
        painter.setFont(self.font())
        painter.drawText(rect, Qt.AlignCenter, self.text())

    def _onButtonClicked(self) -> None:
        self.animation.setCurrent(self.style_data.click_color)
        self.animation.start()

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

    def animate(self, _) -> None:
        self.update()

    def setToolTip(self, tooltip) -> None:
        super().setToolTip(tooltip)
        self._updateToolTip()

    def setButtonColor(self, code: str) -> None:
        self.style_data.button_color = SiColor.toArray(code, "rgba")

    def setBackgroundColor(self, code: str) -> None:
        self.style_data.background_color = SiColor.toArray(code, "rgba")

    def event(self, event):
        if event.type() == QEvent.ToolTip:
            return True  # 忽略工具提示事件
        return super().event(event)

    def enterEvent(self, event) -> None:
        super().enterEvent(event)
        self.animation.setTarget(self.style_data.hover_color)
        self.animation.start()
        self._showToolTip()
        self._updateToolTip()

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)
        self.animation.setTarget(self.style_data.idle_color)
        self.animation.start()
        self._hideToolTip()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)

        painter.setPen(Qt.PenStyle.NoPen)
        rect = self.rect()
        text_rect = QRect(0, 0, self.width(), self.height() - self.style_data.border_height - 1)
        self._drawBackgroundRect(painter, rect)
        self._drawButtonRect(painter, rect)
        self._drawHighLightRect(painter, rect)
        self._drawTextRect(painter, text_rect)
