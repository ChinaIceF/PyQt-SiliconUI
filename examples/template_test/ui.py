from components.page_homepage import ExampleHomepage
from components.page_option_cards import ExampleOptionCards
from components.page_widgets import ExampleWidgets
from icons import IconDictionary

from siui.core.globals import SiGlobal
from siui.templates.application import SiliconApplication

# 载入图标
SiGlobal.siui.loadIcons(IconDictionary(color="#FFFFFF").icons)


class MySiliconApp(SiliconApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setMinimumSize(1024, 380)
        self.initUI()

    def initUI(self):
        self.addPage(ExampleHomepage(self), SiGlobal.siui.icons["fi-rr-home"], "主页", "top")
        self.addPage(ExampleOptionCards(self), SiGlobal.siui.icons["fi-rr-rectangle-horizontal"], "选项卡", "top")
        self.addPage(ExampleWidgets(self), SiGlobal.siui.icons["fi-rr-cube"], "控件", "top")
