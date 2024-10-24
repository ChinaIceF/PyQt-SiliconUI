# NOTE This is the refactor of button component. It's working in progress. It will
# replace button once it's done. Now it's draft, code may be ugly and verbose temporarily.

from PyQt5.QtCore import QRect, QRectF, Qt
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QPaintEvent
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget


class SiPushButton(QPushButton):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

    @property
    def bottomBorderHeight(self) -> int:
        return round(self.rect().height() * 0.125)

    @staticmethod
    def _drawBackgroundPath(rect: QRect) -> QPainterPath:
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, rect.width(), rect.height()), 40, 40)
        return path

    def _drawBackgroundRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(QColor("#2D2932"))
        painter.drawPath(self._drawBackgroundPath(rect))

    def _drawButtonPath(self, rect: QRect) -> QPainterPath:
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, rect.width(), rect.height() - self.bottomBorderHeight), 40, 40)
        return path

    def _drawBbuttonRect(self, painter: QPainter, rect: QRect) -> None:
        painter.setBrush(QColor("#4C4554"))
        painter.drawPath(self._drawButtonPath(rect))

    def enterEvent(self, event) -> None:
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        rect = self.rect()
        self._drawBackgroundRect(painter, rect)
        self._drawBbuttonRect(painter, rect)


class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.resize(600, 800)
        self.btn = SiPushButton(self)
        self.btn.setFixedSize(2400, 320)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.btn, alignment=Qt.AlignmentFlag.AlignCenter)


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()
