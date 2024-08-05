from PyQt5.QtWidgets import QDesktopWidget

import icons
from components.page_homepage import ExampleHomepage
from components.page_icons import ExampleIcons
from components.page_option_cards import ExampleOptionCards
from components.page_widgets import ExampleWidgets

import siui
from siui.core.color import SiColor
from siui.core.globals import SiGlobal
from siui.templates.application import SiliconApplication

# 载入图标
siui.core.globals.SiGlobal.siui.loadIcons(
    icons.IconDictionary(color=SiGlobal.siui.colors.fromToken(SiColor.SVG_NORMAL)).icons
)


class MySiliconApp(SiliconApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setMinimumSize(1024, 380)
        self.resize(1240, 910)
        screen_geo = QDesktopWidget().screenGeometry()
        self.setGeometry((screen_geo.width() - self.width()) // 2, (screen_geo.height() - self.height()) // 2,
                         self.width(), self.height())

        self.init_my_app_ui()
        self.setPage(0)

        SiGlobal.siui.reloadAllWindowsStyleSheet()

    def init_my_app_ui(self):
        self.addPage(ExampleHomepage(self), SiGlobal.siui.iconpack.get("ic_fluent_home_filled"), "主页", "top")
        self.addPage(ExampleIcons(self), SiGlobal.siui.iconpack.get("ic_fluent_diversity_filled"), "图标库", "top")
        self.addPage(ExampleOptionCards(self), SiGlobal.siui.iconpack.get("ic_fluent_align_space_evenly_vertical_filled"), "选项卡", "top")
        self.addPage(ExampleWidgets(self), SiGlobal.siui.iconpack.get("ic_fluent_box_multiple_filled"), "控件", "top")
