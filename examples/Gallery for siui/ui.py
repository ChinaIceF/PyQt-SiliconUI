import icons
from components.page_homepage import ExampleHomepage
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
        self.init_my_app_ui()
        self.resize(1200, 900)

    def init_my_app_ui(self):
        self.addPage(ExampleHomepage(self), SiGlobal.siui.icons["fi-rr-home"], "主页", "top")
        self.addPage(ExampleOptionCards(self), SiGlobal.siui.icons["fi-rr-rectangle-horizontal"], "选项卡", "top")
        self.addPage(ExampleWidgets(self), SiGlobal.siui.icons["fi-rr-cube"], "控件", "top")

    def showEvent(self, a0):
        super().showEvent(a0)
