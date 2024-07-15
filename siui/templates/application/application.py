from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow

from siui.core.globals import SiGlobal
from siui.gui import ToolTipWindow
from siui.components.widgets import SiDenseHContainer, SiDenseVContainer, SiLabel, SiPixLabel, SiSimpleButton
from .page_view import PageView



class SiliconApplication(QMainWindow):
    """
    SiliconUI 应用程序模板，包含工具提示窗口
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 将自己添加到全局
        SiGlobal.siui.windows["MAIN_WINDOW"] = self

        # 创建工具提示窗口，并添加到全局
        SiGlobal.siui.windows["TOOL_TIP"] = ToolTipWindow()
        SiGlobal.siui.windows["TOOL_TIP"].show()
        SiGlobal.siui.windows["TOOL_TIP"].setOpacity(0)

        # 构建界面
        self.init_ui()

        # 重载全部窗口的样式表
        SiGlobal.siui.reloadAllWindowsStyleSheet()

    def init_ui(self):
        """
        构建界面
        """

        # 初始化窗口
        screen_geo = QDesktopWidget().screenGeometry()
        w, h = 1200, 700
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setGeometry((screen_geo.width() - w) // 2, (screen_geo.height() - h) // 2, w, h)
        self.setWindowTitle("Silicon Application Template")

        # 整个窗口的垫底标签
        self.background_label = SiLabel(self)
        self.background_label.setFixedStyleSheet("border-radius: 8px")

        # -> 垂直容器，上方是标题，下方是窗口内容
        self.container_title_and_content = SiDenseVContainer(self)
        self.container_title_and_content.setSpacing(0)
        self.container_title_and_content.setAdjustWidgetsSize(True)

        # -> 标题栏处的水平容器，左侧是图标和标题，右侧是操作按钮
        self.container_title = SiDenseHContainer(self)
        self.container_title.setSpacing(0)
        self.container_title.setAlignCenter(True)
        self.container_title.setFixedHeight(64)

        # 应用内图标
        self.app_icon = SiPixLabel(self)
        self.app_icon.resize(24, 24)
        self.app_icon.load("./img/logo.png")

        # 应用标题
        self.app_title = SiLabel(self)
        self.app_title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.app_title.setFont(SiGlobal.siui.fonts["S_NORMAL"])
        self.app_title.setAutoAdjustSize(True)
        self.app_title.setText("Silicon 应用模版")

        # 关闭窗口按钮
        self.close_window_button = SiSimpleButton(self)
        self.close_window_button.attachment().load(SiGlobal.siui.icons["fi-rr-cross-small"])
        self.close_window_button.resize(32, 32)
        self.close_window_button.clicked.connect(self.close)

        # <- 添加到水平容器
        self.container_title.addPlaceholder(2)
        self.container_title.addPlaceholder(16)
        self.container_title.addWidget(self.app_icon)
        self.container_title.addPlaceholder(16)
        self.container_title.addWidget(self.app_title)

        self.container_title.addPlaceholder(16, "right")
        self.container_title.addWidget(self.close_window_button, "right")

        # 创建 page view，它继承自水平容器
        self.page_view = PageView()

        # <- 添加到垂直容器
        self.container_title_and_content.addWidget(self.container_title)
        self.container_title_and_content.addWidget(self.page_view)

    def addPage(self, page, svg_data: bytes, hint: str, side="top"):
        """
        添加新页面
        :param page: 页面控件
        :param svg_data: 页面按钮的 svg 数据
        :param hint: 页面按钮的工具提示
        :param side: 页面按钮置于哪一侧
        """
        self.page_view.addPage(page, svg_data, hint, side)

    def reloadStyleSheet(self):
        """
        重载样式表
        """
        self.background_label.setStyleSheet(
            """
            background-color: {};
            border: 1px solid {};
            """.format(SiGlobal.siui.colors["INTERFACE_BG_A"], SiGlobal.siui.colors["INTERFACE_BG_B"])
        )
        self.app_title.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_B"]))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.background_label.resize(w, h)
        self.container_title_and_content.resize(w, h)
        self.page_view.resize(w, h-64)

    def showEvent(self, a0):
        super().showEvent(a0)
        SiGlobal.siui.reloadAllWindowsStyleSheet()
        self.page_view.stacked_container.setCurrentIndex(0)  # 显示第一页
