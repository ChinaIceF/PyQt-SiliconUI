from __future__ import annotations

from dataclasses import dataclass

import numpy
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QLabel, QWidget

from siui.core import SiColor, SiGlobal


@dataclass
class SiLabelStyleData:
    text_color = SiColor.toArray("#00FFFFFF")
    background_color = SiColor.toArray("#00FFFFFF")
    border_bottom_left_radius: int = 4
    border_bottom_right_radius: int = 4
    border_top_left_radius: int = 4
    border_top_right_radius: int = 4


class SiLabelRefactor(QLabel):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.style_data = SiLabelStyleData()

    @property
    def textColor(self) -> numpy.ndarray:
        return self.style_data.text_color

    def backgroundColor(self) -> numpy.ndarray:
        return self.style_data.background_color

    def borderRadius(self) -> tuple:
        return (self.style_data.border_bottom_left_radius, self.style_data.border_bottom_right_radius,
                self.style_data.border_top_left_radius, self.style_data.border_top_right_radius)

    def setTextColor(self, code: str | tuple) -> None:
        self.style_data.text_color = SiColor.toArray(code)
        self.update()

    def setBackgroundColor(self, code: str | tuple) -> None:
        self.style_data.background_color = SiColor.toArray(code)
        self.update()

    def setBorderRadius(self, *radius: int):
        """
        set the border radius of this label.
        accepts 1 or 4 param(s).
        """
        if len(radius) == 1:
            self.style_data.border_bottom_left_radius = radius[0]
            self.style_data.border_bottom_right_radius = radius[0]
            self.style_data.border_top_left_radius = radius[0]
            self.style_data.border_top_right_radius = radius[0]
        elif len(radius) == 4:
            self.style_data.border_bottom_left_radius = radius[0]
            self.style_data.border_bottom_right_radius = radius[1]
            self.style_data.border_top_left_radius = radius[2]
            self.style_data.border_top_right_radius = radius[3]
        else:
            raise ValueError(f"setBorderRadius expects 1 or 4 param, but {len(radius)} are given.")
        self.update()

    def event(self, event):
        if event.type() == QEvent.ToolTip:
            return True  # 忽略工具提示事件
        return super().event(event)

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

    def setToolTip(self, tooltip) -> None:
        super().setToolTip(tooltip)
        self._updateToolTip()

    def enterEvent(self, event) -> None:
        super().enterEvent(event)
        self._showToolTip()
        self._updateToolTip()

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)
        self._hideToolTip()

