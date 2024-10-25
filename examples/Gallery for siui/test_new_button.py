# NOTE This is the refactor of button component. It's working in progress. It will
# replace button once it's done. Now it's draft, code may be ugly and verbose temporarily.
from __future__ import annotations

import os

from PyQt5.QtCore import QRect, QRectF, Qt
from PyQt5.QtGui import QColor, QIcon, QPainter, QPainterPath, QPaintEvent
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget

from siui.core import GlobalFont, SiColor, SiExpAnimation
from siui.gui import SiFont

os.environ["QT_SCALE_FACTOR"] = str(2)


class SiPushButton(QPushButton):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

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

    def withTextAndIcon(cls, text: str, icon: str, parent: QWidget | None = None) -> "SiPushButton":
        cls = cls(parent)
        cls.setText(text)
        cls.setIcon(icon)
        return cls

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

    def _onButtonClicked(self) -> None:
        self.animation.setCurrent(self.click_color)
        self.animation.start()

    def animate(self, _) -> None:
        self.update()

    def enterEvent(self, event) -> None:
        super().enterEvent(event)
        self.animation.setTarget(self.hover_color)
        self.animation.start()

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)
        self.animation.setTarget(self.idle_color)
        self.animation.start()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)

        painter.setPen(Qt.PenStyle.NoPen)
        rect = self.rect()
        self._drawBackgroundRect(painter, rect)
        self._drawButtonRect(painter, rect)
        self._drawHighLightRect(painter, rect)

        text_rect = QRect(0, 0, self.width(), self.height() - 4)
        painter.setPen(QColor(239, 239, 239))  # 设置文本颜色
        painter.setFont(self.font())  # 设置字体和大小
        painter.drawText(text_rect, Qt.AlignCenter, self.text())  # 在按钮中心绘制文本
        painter.end()


class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.resize(600, 800)
        self.setStyleSheet("background-color: #332E38")

        self.btn = SiPushButton(self)
        self.btn.setFixedSize(128, 32)
        self.btn.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
        self.btn.setText("我是按钮")
        self.btn.clicked.connect(lambda: print("clicked!"))

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.btn, alignment=Qt.AlignmentFlag.AlignCenter)


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()