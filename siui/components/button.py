# NOTE This is the refactor of button component. It's working in progress. It will
# replace button once it's done. Now it's draft, code may be ugly and verbose temporarily.
from __future__ import annotations

from PyQt5.QtCore import QEvent, QRect, QRectF, Qt
from PyQt5.QtGui import QColor, QIcon, QPainter, QPainterPath, QPaintEvent
from PyQt5.QtWidgets import QPushButton, QWidget

from siui.core import GlobalFont, SiColor, SiExpAnimation, SiGlobal
from siui.gui import SiFont


class SiPushButtonRefactor(QPushButton):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._initStyle()

        self.idle_color = SiColor.toArray("#00FFFFFF")
        self.hover_color = SiColor.toArray("#10FFFFFF")
        self.click_color = SiColor.toArray("#40FFFFFF")

        self.animation = SiExpAnimation(self)
        self.animation.setFactor(1/8)
        self.animation.setBias(0.2)
        self.animation.setTarget(self.idle_color)
        self.animation.setCurrent(self.idle_color)
        self.animation.ticked.connect(self.animate)

        self.clicked.connect(self._onButtonClicked)

    @classmethod
    def withText(cls, text: str, parent: QWidget | None = None) -> "SiPushButton":
        cls = cls(parent)
        cls.setText(text)
        return cls

    @classmethod
    def withIcon(cls, icon: QIcon, parent: QWidget | None = None) -> "SiPushButton":
        cls = cls(parent)
        cls.setIcon(icon)
        return cls

    @classmethod
    def withTextAndIcon(cls, text: str, icon: str, parent: QWidget | None = None) -> "SiPushButton":
        cls = cls(parent)
        cls.setText(text)
        cls.setIcon(icon)
        return cls

    def _initStyle(self):
        self.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
        self.setStyleSheet("color: #DFDFDF;")


    @property
    def bottomBorderHeight(self) -> int:
        return round(3)

    @staticmethod
    def _drawBackgroundPath(rect: QRect) -> QPainterPath:
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, rect.width(), rect.height()), 4, 4)
        return path

    def _drawBackgroundRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(QColor("#2D2932"))
        painter.drawPath(self._drawBackgroundPath(rect))

    def _drawButtonPath(self, rect: QRect) -> QPainterPath:
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, rect.width(), rect.height() - self.bottomBorderHeight), 3, 3)
        return path

    def _drawButtonRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(QColor("#4C4554"))
        painter.drawPath(self._drawButtonPath(rect))

    def _drawHighLightRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(QColor(SiColor.toCode(self.animation.current_)))
        painter.drawPath(self._drawButtonPath(rect))

    def _drawTextRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setPen(self.palette().text().color())
        painter.setFont(self.font())
        painter.drawText(rect, Qt.AlignCenter, self.text())

    def _onButtonClicked(self) -> None:
        self.animation.setCurrent(self.click_color)
        self.animation.start()

    def _showToolTip(self) -> None:
        if self.toolTip() != "" and "TOOL_TIP" in SiGlobal.siui.windows:
            SiGlobal.siui.windows["TOOL_TIP"].setNowInsideOf(self)
            SiGlobal.siui.windows["TOOL_TIP"].show_()

    def _hideToolTip(self) -> None:
        if self.toolTip() != "" and "TOOL_TIP" in SiGlobal.siui.windows:
            SiGlobal.siui.windows["TOOL_TIP"].setNowInsideOf(None)
            SiGlobal.siui.windows["TOOL_TIP"].hide_()

    def _updateToolTip(self) -> None:
        if SiGlobal.siui.windows["TOOL_TIP"].nowInsideOf() == self:
            SiGlobal.siui.windows["TOOL_TIP"].setText(self.toolTip())

    def animate(self, _) -> None:
        self.update()

    def setToolTip(self, tooltip) -> None:
        super().setToolTip(tooltip)
        self._updateToolTip()

    def event(self, event):
        if event.type() == QEvent.ToolTip:
            return True  # 忽略工具提示事件
        return super().event(event)

    def enterEvent(self, event) -> None:
        super().enterEvent(event)
        self.animation.setTarget(self.hover_color)
        self.animation.start()
        self._showToolTip()
        self._updateToolTip()

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)
        self.animation.setTarget(self.idle_color)
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
        text_rect = QRect(0, 0, self.width(), self.height() - 4)
        self._drawBackgroundRect(painter, rect)
        self._drawButtonRect(painter, rect)
        self._drawHighLightRect(painter, rect)
        self._drawTextRect(painter, text_rect)
