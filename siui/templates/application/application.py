
from PyQt5.QtWidgets import QMainWindow

from siui.components.tooltip import ToolTipWindow
from siui.components.widgets.abstracts import SiWidget
from siui.core import SiGlobal
from siui.templates.application.components.layer.layer_child_page.layer_child_page import LayerChildPage
from siui.templates.application.components.layer.layer_left_global_drawer.layer_left_global_drawer import (
    LayerLeftGlobalDrawer,
)
from siui.templates.application.components.layer.layer_main.layer_main import LayerMain
from siui.templates.application.components.layer.layer_modal_dialog.layer_modal_dialog import LayerModalDialog
from siui.templates.application.components.layer.layer_overlays.layer_overlays import LayerOverLays
from siui.templates.application.components.layer.layer_right_message_sidebar.layer_right_message_sidebar import (
    LayerRightMessageSidebar,
)


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

        # 层的组
        self.group_main_interface = SiWidget(self)
        self.groups_ = {
            "MAIN_INTERFACE": self.group_main_interface
        }

        # 构建界面
        self.layer_main = LayerMain(self.group_main_interface)
        self.layer_child_page = LayerChildPage(self.group_main_interface)

        self.layer_left_global_drawer = LayerLeftGlobalDrawer(self)
        self.layer_right_message_sidebar = LayerRightMessageSidebar(self)
        self.layer_modal_dialog = LayerModalDialog(self)
        self.layer_overlays = LayerOverLays(self)

    def groups(self):
        return self.groups_

    def layerMain(self):
        return self.layer_main

    def LayerRightMessageSidebar(self):
        return self.layer_right_message_sidebar

    def layerChildPage(self):
        return self.layer_child_page

    def layerModalDialog(self):
        return self.layer_modal_dialog

    def layerLeftGlobalDrawer(self):
        return self.layer_left_global_drawer

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.group_main_interface.resize(w, h)

        # Set the maximum height of the sidebar to prevent performance from dropping when too many message boxes exist.
        self.layer_right_message_sidebar.setMaximumHeight(event.size().height())
        self.layer_right_message_sidebar.adjustSize()

        self.layer_main.resize(event.size())
        self.layer_child_page.resize(event.size())
        self.layer_right_message_sidebar.setGeometry(w - 400, 80, 400, self.layer_right_message_sidebar.height())
        self.layer_modal_dialog.resize(event.size())
        self.layer_left_global_drawer.resize(event.size())
        self.layer_overlays.resize(event.size())
