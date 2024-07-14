from siui.templates.application import SiliconApplication
from siui.


class MySiliconApp(SiliconApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.init_my_app_ui()

    def init_my_app_ui(self):
        self.page1 =