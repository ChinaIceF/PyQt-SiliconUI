from __future__ import annotations

from dataclasses import dataclass
from typing import overload

from PyQt5.QtCore import QRectF, QSize, Qt
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QPixmap
from PyQt5.QtWidgets import QBoxLayout, QLabel, QWidget, QSizePolicy

from siui.components.label import SiRoundPixmapWidget
from siui.core import GlobalFont, createPainter
from siui.gui import SiFont
from siui.typing import T_WidgetParent


class SiBoxContainer(QWidget):
    LeftToRight = QBoxLayout.LeftToRight
    RightToLeft = QBoxLayout.RightToLeft
    TopToBottom = QBoxLayout.TopToBottom
    BottomToTop = QBoxLayout.BottomToTop

    def __init__(self,
                 parent: T_WidgetParent = None,
                 direction: QBoxLayout.Direction = QBoxLayout.LeftToRight) -> None:
        super().__init__(parent)

        layout = QBoxLayout(direction)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def layout(self) -> QBoxLayout | None:  # overloaded for coding hints, has no effect on any impl.
        return super().layout()


class SiDenseContainer(QWidget):
    LeftToRight = QBoxLayout.LeftToRight
    RightToLeft = QBoxLayout.RightToLeft
    TopToBottom = QBoxLayout.TopToBottom
    BottomToTop = QBoxLayout.BottomToTop

    def __init__(self,
                 parent: T_WidgetParent = None,
                 direction: QBoxLayout.Direction = QBoxLayout.LeftToRight) -> None:
        super().__init__(parent)

        self._is_stretch_widget_muted = False
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

    def muteStretchWidget(self) -> None:
        self.layout().setStretchFactor(self.stretch_widget, 0)
        self._is_stretch_widget_muted = True

    def isStretchWidgetMuted(self) -> bool:
        return self._is_stretch_widget_muted

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
    提供“立体样式”的卡片样容器
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

        self._header.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self._body.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self._footer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

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


class RowCardStyleData:
    background_color: QColor = QColor("#332e38")
    border_radius: float = 6


class SiRowCard(SiDenseContainer):
    """
    提供“平面化样式”的条状卡片样容器
    """

    def __init__(self,
                 parent: T_WidgetParent = None,
                 direction: QBoxLayout.Direction = QBoxLayout.LeftToRight) -> None:
        super().__init__(parent, direction)

        self.style_data = RowCardStyleData()

        self.setContentsMargins(0, 0, 0, 0)

    def _drawBackgroundPath(self, rect: QRectF) -> QPainterPath:
        fore_radius = self.style_data.border_radius

        path = QPainterPath()
        path.addRoundedRect(rect, fore_radius, fore_radius)
        return path

    def _drawBackgroundRect(self, painter: QPainter, rect: QRectF) -> None:
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.style_data.background_color)
        painter.drawPath(self._drawBackgroundPath(rect))

    def paintEvent(self, a0):
        background_rect = QRectF(0, 0, self.width(), self.height())

        with createPainter(self) as painter:
            self._drawBackgroundRect(painter, background_rect)


class SiTriSectionRowCard(SiRowCard):
    def __init__(self,
                 parent: T_WidgetParent = None,
                 pixmap: QPixmap | None = None,
                 title: str = "Tri-Section Row Card",
                 description: str = "This is the description text of this card.") -> None:
        super().__init__(parent, self.LeftToRight)

        self._icon_container = SiDenseContainer(self, self.TopToBottom)
        self._text_container = SiDenseContainer(self, self.TopToBottom)
        self._action_container = SiDenseContainer(self, self.RightToLeft)

        self._icon = SiRoundPixmapWidget(self, pixmap)
        self._title = QLabel(title, self)
        self._description = QLabel(description, self)

        self._icon_container.addWidget(self._icon)
        self._text_container.addWidget(self._title)
        self._text_container.addWidget(self._description)

        self.addWidget(self._icon_container)
        self.addWidget(self._text_container)
        self.addWidget(self._action_container, Qt.RightEdge)

        self._initStyle()

    def _initStyle(self) -> None:
        self.setMinimumHeight(80)
        self.layout().setSpacing(0)

        self._icon.setFixedSize(80, 80)
        self._icon.setVisualSizeEnabled(True)
        self._icon.setVisualSize(QSize(32, 32))

        self._title.setFont(SiFont.tokenized(GlobalFont.S_BOLD))
        self._title.setStyleSheet(
            "color: #D1CBD4"
        )

        self._description.setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
        self._description.setStyleSheet(
            "color: #918497"
        )

        self._icon_container.setFixedWidth(80)
        self._icon_container.layout().setSpacing(0)
        self._icon_container.layout().setAlignment(self._icon, Qt.AlignCenter)
        self._icon_container.layout().setStretchFactor(self._icon_container.stretchWidget(), 0)

        self._text_container.layout().setSpacing(0)
        self._text_container.layout().setStretchFactor(self._text_container.stretchWidget(), 0)
        self._text_container.setContentsMargins(0, 20, 0, 20)

        self._action_container.setContentsMargins(16, 0, 28, 0)

        self.adjustSize()

    def iconContainer(self) -> SiDenseContainer:
        return self._icon_container

    def textContainer(self) -> SiDenseContainer:
        return self._text_container

    def actionsContainer(self) -> SiDenseContainer:
        return self._action_container

    def titleLabel(self) -> QLabel:
        return self._title

    def descriptionLabel(self) -> QLabel:
        return self._description

#
# class SiStackWidget():