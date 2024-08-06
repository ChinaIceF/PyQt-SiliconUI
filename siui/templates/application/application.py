import ctypes

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QGraphicsDropShadowEffect

from siui.components.tooltip import ToolTipWindow
from siui.core.globals import SiGlobal
from siui.templates.application.components.layer.layer_main.layer_main import LayerMain
from siui.templates.application.components.layer.layer_right_message_sidebar.layer_right_message_sidebar import \
    LayerRightMessageSidebar


class SiliconApplication(QMainWindow):
    """
    SiliconUI 应用程序模板，包含工具提示窗口
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 添加全局窗口
        SiGlobal.siui.windows["MAIN_WINDOW"] = self
        SiGlobal.siui.windows["TOOL_TIP"] = ToolTipWindow()
        SiGlobal.siui.windows["TOOL_TIP"].show()
        SiGlobal.siui.windows["TOOL_TIP"].setOpacity(0)

        # 初始化窗口
        self.resize(1200, 700)
        self.setWindowTitle("Silicon Application Template")

        # 构建界面
        self.layer_main = LayerMain(self)
        self.layer_right_message_sidebar = LayerRightMessageSidebar(self)

    def layerMain(self):
        return self.layer_main

    def rightMessageSidebar(self):
        return self.layer_right_message_sidebar

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.layer_main.resize(event.size())
        self.layer_right_message_sidebar.setGeometry(w - 400, 80, 400, self.layer_right_message_sidebar.height())

