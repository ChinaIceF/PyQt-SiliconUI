from __future__ import annotations

from dataclasses import dataclass

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QPainter, QPainterPath
from PyQt5.QtWidgets import QBoxLayout, QLabel, QWidget

from siui.components.button import SiPushButtonRefactor
from siui.core import GlobalFont, createPainter
from siui.gui import SiFont
from siui.typing import T_WidgetParent


class SiDenseContainer(QWidget):
    LeftToRight = QBoxLayout.LeftToRight
    RightToLeft = QBoxLayout.RightToLeft
    TopToBottom = QBoxLayout.TopToBottom
    BottomToTop = QBoxLayout.BottomToTop

    def __init__(self,
                 parent: T_WidgetParent = None,
                 direction: QBoxLayout.Direction = QBoxLayout.LeftToRight) -> None:
        super().__init__(parent)

        self.stretch_widget = QWidget(self)
        self.stretch_widget.resize(0, 0)
        self._initLayout(direction)

    def _initLayout(self, direction) -> None:
        layout = QBoxLayout(direction)
        layout.addWidget(self.stretch_widget)
        layout.setStretchFactor(self.stretch_widget, 1)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def layout(self) -> QBoxLayout | None:  # overloaded for coding hints, has no effect on any impl.
        return super().layout()

    def stretchWidget(self) -> QWidget:
        return self.stretch_widget

    def addWidget(self, widget: QWidget, side: Qt.Edges = Qt.LeftEdge | Qt.TopEdge) -> None:
        sw_index = self.layout().indexOf(self.stretch_widget)
        if side & Qt.LeftEdge or side & Qt.TopEdge:
            self.layout().insertWidget(sw_index, widget)
        elif side & Qt.RightEdge or side & Qt.BottomEdge:
            self.layout().insertWidget(sw_index+1, widget)
        else:
            raise ValueError(f"Unexpected side: {side}")


class PanelCardStyleData:
    background_fore_color: QColor = QColor("#332e38")
    background_back_color: QColor = QColor("#1C191F")
    border_radius_fore: float = 6
    border_radius_back: float = 9


class SiPanelCard(SiDenseContainer):
    """
    提供“立体样式”的卡片容器
    """

    def __init__(self,
                 parent: T_WidgetParent = None,
                 direction: QBoxLayout.Direction = QBoxLayout.LeftToRight) -> None:
        super().__init__(parent, direction)

        self.style_data = PanelCardStyleData()

        self.setContentsMargins(0, 0, 0, 3)

    def _drawBackgroundForePath(self, rect: QRectF) -> QPainterPath:
        fore_radius = self.style_data.border_radius_fore

        rect = QRectF(rect.x(), rect.y(), rect.width(), rect.height() - 3)
        path = QPainterPath()
        path.addRoundedRect(rect, fore_radius, fore_radius)
        return path

    def _drawBackgroundBackPath(self, rect: QRectF) -> QPainterPath:
        back_radius = self.style_data.border_radius_back

        path = QPainterPath()
        path.addRoundedRect(rect, back_radius, back_radius)
        return path

    def _drawBackgroundRect(self, painter: QPainter, rect: QRectF) -> None:
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.style_data.background_back_color)
        painter.drawPath(self._drawBackgroundBackPath(rect))

        painter.setBrush(self.style_data.background_fore_color)
        painter.drawPath(self._drawBackgroundForePath(rect))

    def paintEvent(self, a0):
        background_rect = QRectF(0, 0, self.width(), self.height())

        with createPainter(self) as painter:
            self._drawBackgroundRect(painter, background_rect)


class SiTriSectionPanelCard(SiPanelCard):
    def __init__(self,
                 parent: T_WidgetParent = None,
                 title: str = "Tri-Section Panel Card",) -> None:
        super().__init__(parent, self.TopToBottom)

        self._header = SiDenseContainer(self, self.LeftToRight)
        self._body = SiDenseContainer(self, self.TopToBottom)
        self._footer = SiDenseContainer(self, self.LeftToRight)

        self._title = QLabel(title, self)
        self._header.addWidget(self._title)

        self.addWidget(self._header)
        self.addWidget(self._body)
        self.addWidget(self._footer, Qt.BottomEdge)

        self._initStyle()

    def _initStyle(self) -> None:
        self._header.setFixedHeight(64)
        self._header.setContentsMargins(24, 16, 24, 16)
        self._header.layout().setSpacing(16)

        self._body.setContentsMargins(24, 0, 24, 0)
        self._body.layout().setSpacing(8)

        self._footer.setContentsMargins(24, 14, 24, 14)
        self._footer.layout().setSpacing(16)

        self._title.setFont(SiFont.tokenized(GlobalFont.M_BOLD))
        self._title.setStyleSheet("color: #FFFFFF")

        self.layout().setSpacing(0)
        self.layout().setStretchFactor(self.stretchWidget(), 0)
        self.layout().setStretchFactor(self._body, 1)

    def title(self) -> str:
        return self._title.text()

    def setTitle(self, title: str) -> None:
        self._title.setText(title)

    def header(self) -> SiDenseContainer:
        return self._header

    def body(self) -> SiDenseContainer:
        return self._body

    def footer(self) -> SiDenseContainer:
        return self._footer
