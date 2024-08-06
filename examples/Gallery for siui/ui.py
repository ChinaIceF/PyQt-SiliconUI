from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDesktopWidget

import icons
from components.page_homepage import ExampleHomepage
from components.page_icons import ExampleIcons
from components.page_option_cards import ExampleOptionCards
from components.page_widgets import ExampleWidgets

import siui
from siui.core.color import SiColor
from siui.core.globals import SiGlobal
from siui.templates.application.application import SiliconApplication

# 载入图标
siui.core.globals.SiGlobal.siui.loadIcons(
    icons.IconDictionary(color=SiGlobal.siui.colors.fromToken(SiColor.SVG_NORMAL)).icons
)


class MySiliconApp(SiliconApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        screen_geo = QDesktopWidget().screenGeometry()
        self.setMinimumSize(1024, 380)
        self.resize(1240, 910)
        self.move((screen_geo.width() - self.width()) // 2, (screen_geo.height() - self.height()) // 2)
        self.layerMain().setTitle("Silicon UI Gallery")
        self.setWindowTitle("Silicon UI Gallery")
        self.setWindowIcon(QIcon("./img/empty_icon.png"))

        self.layerMain().addPage(ExampleHomepage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_home_filled"),
                                 hint="主页", side="top")
        self.layerMain().addPage(ExampleIcons(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_diversity_filled"),
                                 hint="图标包", side="top")
        self.layerMain().addPage(ExampleOptionCards(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_align_space_evenly_vertical_filled"),
                                 hint="选项卡", side="top")
        self.layerMain().addPage(ExampleWidgets(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_box_multiple_filled"),
                                 hint="控件", side="top")

        self.layerMain().setPage(0)
        self.layerMain().showDimMask()

        SiGlobal.siui.reloadAllWindowsStyleSheet()
