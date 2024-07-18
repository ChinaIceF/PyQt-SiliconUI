import os

from PyQt5.QtCore import Qt

from siui.components.option_card import SiOptionCardPlane
from siui.components.widgets import SiDenseVContainer, SiLabel, SiSimpleButton
from siui.core.globals import SiGlobal


class ThemedOptionCardPlane(SiOptionCardPlane):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.my_theme_color = "#855198"
        self.setSpacing(32)

        # 标题边的指示器
        self.title_indicator = SiLabel(self)
        self.title_indicator.setGeometry(0, 24, 4, 18)

    def setThemeColor(self, color_code):
        self.my_theme_color = color_code

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        self.outfit_label_upper.setStyleSheet(
            """
            border-radius: 8px; background-color: {}; border: 1px solid {}; border-bottom: 0px solid #000000
            """.format(SiGlobal.siui.colors["BACKGROUND_COLOR"], SiGlobal.siui.colors["BORDER_COLOR"])
        )
        self.outfit_label_lower.setStyleSheet(f"border-radius: 8px; background-color: {self.my_theme_color}")
        self.title_indicator.setStyleSheet(f"border-radius: 2px; background-color: {self.my_theme_color}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()
        self.outfit_label_upper.resize(w, h - 2)
