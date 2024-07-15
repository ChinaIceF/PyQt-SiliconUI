from siui.templates.application import SiliconApplication
from siui.core.globals import SiGlobal
from siui.components.option_card import SiOptionCardLinear
from components.homepage import ExampleHomePage


class MySiliconApp(SiliconApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.init_my_app_ui()

    def init_my_app_ui(self):
        self.addPage(ExampleHomePage(self), SiGlobal.siui.icons["fi-rr-apple"], "测试页面", "top")
        self.addPage(ExampleHomePage(self), SiGlobal.siui.icons["fi-rr-copy"], "测试页面2", "top")