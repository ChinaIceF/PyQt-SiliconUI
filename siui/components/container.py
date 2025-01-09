from __future__ import annotations

from dataclasses import dataclass

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QBoxLayout, QWidget

from siui.typing import T_WidgetParent


class SiDenseContainer(QWidget):
    def __init__(self, parent: T_WidgetParent = None, direction: QBoxLayout.Direction = QBoxLayout.LeftToRight) -> None:
        super().__init__(parent)

        self.stretch_widget = QWidget(self)
        self._initLayout(direction)

    def _initLayout(self, direction) -> None:
        layout = QBoxLayout(direction)
        layout.addWidget(self.stretch_widget)
        layout.setStretchFactor(self.stretch_widget, 1)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def layout(self) -> QBoxLayout | None:  # overloaded for coding hints, has no effect on any impl.
        return super().layout()

    def addWidget(self, widget: QWidget, side: Qt.Edges = Qt.LeftEdge | Qt.TopEdge) -> None:
        sw_index = self.layout().indexOf(self.stretch_widget)
        if side & Qt.LeftEdge or side & Qt.TopEdge:
            self.layout().insertWidget(sw_index, widget)
        elif side & Qt.RightEdge or side & Qt.BottomEdge:
            self.layout().insertWidget(sw_index+1, widget)
        else:
            raise ValueError(f"Unexpected side: {side}")
