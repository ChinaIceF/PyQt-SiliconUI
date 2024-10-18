from siui.components import SiWidget, SiLabel, SiSvgLabel, SiDenseVContainer
from siui.core import SiColor
from siui.core import SiGlobal


class SiModalDialog(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.body_padding_h = 43
        self.theme_padding_h = 26
        self.content_padding_v = 32
        self.button_padding_v = 24
        self.theme_label_top_height = 2
        self.theme_label_bottom_height = 0
        self.setFixedWidth(460)

        self.theme_label = SiLabel(self)
        self.theme_label.setFixedStyleSheet("border-radius: 8px")
        self.theme_label.setColor(self.getColor(SiColor.THEME))

        self.body_content_label = SiLabel(self)
        self.body_content_label.setObjectName("body_content_label")

        self.body_button_label = SiLabel(self)
        self.body_button_label.setObjectName("body_button_label")

        self.content_container = SiDenseVContainer(self.body_content_label)
        self.content_container.setAdjustWidgetsSize(True)

        self.button_container = SiDenseVContainer(self.body_button_label)
        self.button_container.setAdjustWidgetsSize(True)
        self.button_container.setSpacing(8)

        self.icon_ = SiSvgLabel(self.content_container)
        self.icon_.resize(64, 64)
        self.icon_.setSvgSize(64, 64)

    def icon(self):
        return self.icon_

    def contentContainer(self):
        return self.content_container

    def buttonContainer(self):
        return self.button_container

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.theme_label.setColor(self.getColor(SiColor.THEME))
        self.body_content_label.setStyleSheet(
            "#body_content_label {"
            "     border-radius: 8px;"
            f"    background-color: {self.getColor(SiColor.INTERFACE_BG_B)};"
            f"    border: 1px solid {self.getColor(SiColor.INTERFACE_BG_C)};"
            "}"
        )
        self.body_button_label.setStyleSheet(
            "#body_button_label {"
            "     border-radius: 8px;"
            f"    background-color: {self.getColor(SiColor.INTERFACE_BG_C)};"
            f"    border: 1px solid {self.getColor(SiColor.INTERFACE_BG_C)};"
            "}"

        )

    def adjustSize(self):
        self.content_container.setFixedWidth(self.width() - 2 * self.body_padding_h)
        self.button_container.setFixedWidth(self.width() - 2 * self.body_padding_h)
        self.content_container.adjustSize()
        self.button_container.adjustSize()

        self.body_content_label.setGeometry(
            0,
            self.theme_label_top_height,
            self.width(),
            self.content_container.height() + 2 * self.content_padding_v + self.button_container.height() + 2 * self.button_padding_v
        )

        self.body_button_label.setGeometry(
            0,
            self.theme_label_top_height + self.content_container.height() + 2 * self.content_padding_v,
            self.width(),
            self.button_container.height() + 2 * self.button_padding_v
        )

        self.content_container.move(self.body_padding_h, self.content_padding_v)
        self.button_container.move(self.body_padding_h, self.button_padding_v)
        self.theme_label.setGeometry(
            self.theme_padding_h,
            0,
            self.width() - 2 * self.theme_padding_h,
            self.content_container.height() + 2 * self.content_padding_v + self.button_container.height() + 2 * self.button_padding_v + self.theme_label_top_height + self.theme_label_bottom_height
        )
        self.icon_.move(self.content_container.width() - self.icon_.width(), 0)
        self.resize(self.width(), self.theme_label.height())
