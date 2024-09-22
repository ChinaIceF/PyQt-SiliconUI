import os

from PyQt5.QtCore import Qt

from siui.components.option_card import SiOptionCardPlane
from siui.components.widgets import SiDenseVContainer, SiLabel, SiSimpleButton
from siui.core import SiGlobal
from siui.core import Si


class ThemedOptionCardPlane(SiOptionCardPlane):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.my_theme_color = "#855198"
        self.setSpacing(32)

        # 标题边的指示器
        self.title_indicator = SiLabel(self)
        self.title_indicator.setGeometry(0, 24, 4, 18)

        # 解释说明
        self.description = SiLabel(self)
        self.description.setWordWrap(True)
        self.description.setFixedHeight(128)
        self.description.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.body().setAdjustWidgetsSize(True)
        self.body().addWidget(self.description)

        # 链接按钮
        self.link_button = SiSimpleButton(self)
        self.link_button.setFixedSize(32, 32)
        self.link_button.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_open_regular"))

        link_button_container = SiDenseVContainer(self)
        link_button_container.setAlignment(Qt.AlignCenter)
        link_button_container.setFixedHeight(48)
        link_button_container.addWidget(self.link_button)
        self.footer().setSiliconWidgetFlag(Si.EnableAnimationSignals)
        self.footer().resized.connect(lambda size: link_button_container.setFixedWidth(size[0]))
        self.footer().setFixedHeight(48)
        self.footer().addWidget(link_button_container)

    def setDescription(self, text):
        self.description.setText(f"<p style='line-height: 23px'>{text}</p>")

    def setThemeColor(self, color_code):
        self.my_theme_color = color_code
        self.reloadStyleSheet()

    def setURL(self, url):
        self.link_button.setHint(url)
        self.link_button.clicked.connect(lambda: os.system(f"start {url}"))

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        self.outfit_label_upper.setStyleSheet(
            """
            border-radius: 8px; background-color: {}
            """.format(SiGlobal.siui.colors["INTERFACE_BG_C"])
        )
        self.outfit_label_lower.setStyleSheet(f"border-radius: 8px; background-color: {self.my_theme_color}")
        self.title_indicator.setStyleSheet(f"border-radius: 2px; background-color: {self.my_theme_color}")
        self.description.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_B"]))
