from PyQt5.QtCore import Qt

from siui.components import SiWidget, SiDenseHContainer, SiLabel, SiTitledWidgetGroup
from siui.components.page import SiPage
from siui.core import SiColor
from siui.core import SiQuickEffect
from siui.core import Si


class SiChildPage(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.width_ratio = 0.618
        self.height_ratio = (1-0.618) * 2

        self.view_ = SiWidget(self)

        # content
        self.background_content = SiLabel(self.view_)
        self.background_content.setStyleSheet(
            "border-radius: 8px;"
            f"background-color: {self.getColor(SiColor.INTERFACE_BG_B)};"
            f"border: 1px solid {self.getColor(SiColor.INTERFACE_BG_C)};"
        )


        self.content_ = SiPage(self.view_)

        # panel
        self.background_panel = SiLabel(self.view_)
        self.background_panel.setStyleSheet(
            "border-top-left-radius: 8px;"
            "border-top-right-radius: 8px;"
            f"background-color: {self.getColor(SiColor.INTERFACE_BG_C)}"
        )
        SiQuickEffect.applyDropShadowOn(self.background_panel, (0, 0, 0, 60), blur_radius=48)

        self.panel_ = SiDenseHContainer(self.view_)
        self.panel_.setAlignment(Qt.AlignCenter)
        self.panel_.setFixedHeight(80)

        # set self.view as center widget
        self.setCenterWidget(self.view_)

    def content(self):
        return self.content_

    def panel(self):
        return self.panel_

    def view(self):
        return self.view_

    def closeParentLayer(self):
        self.parent().closeLayer()

    def setSizeRatio(self, width_ratio, height_ratio):
        self.width_ratio = width_ratio
        self.height_ratio = height_ratio

    def getSizeFitParent(self):
        return int(self.parent().width() * self.width_ratio), int(self.parent().height() * self.height_ratio)

    def adjustSize(self):
        width_from_ratio = int(self.parent().width() * self.width_ratio)
        height_from_ratio = int(self.parent().height() * self.height_ratio)
        self.view_.resize(width_from_ratio, height_from_ratio)

        total_width, total_height = self.view_.width(), self.view_.height()
        self.resize(total_width, total_height)                                  # to update position of center widget
        self.content_.resize(total_width, total_height - self.panel_.height())
        self.panel_.setGeometry(48, total_height - self.panel_.height(), total_width - 96, self.panel_.height())

        self.background_content.resize(total_width, total_height)
        self.background_panel.setGeometry(0, total_height - self.panel_.height(), total_width, self.panel_.height())