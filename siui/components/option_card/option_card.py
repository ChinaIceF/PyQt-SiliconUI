from PyQt5.QtCore import Qt

from siui.components.option_card.abstracts.option_card import ABCSiOptionCardPlane
from siui.components.widgets.abstracts.widget import SiWidget
from siui.components.widgets.container import SiDenseHContainer
from siui.components.widgets.label import SiLabel, SiSvgLabel
from siui.core import GlobalFont, Si, SiGlobal
from siui.gui import SiFont


class SiOptionCardLinear(SiWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.panel = SiLabel(self)
        self.panel.setFixedStyleSheet(f"background-color:{SiGlobal.siui.colors['INTERFACE_BG_C']}; border-radius:4px")

        # 设定最小高度
        self.setMinimumHeight(80)

        # 创建整体容器
        self.container = SiDenseHContainer(self)
        self.container.setSpacing(0)
        self.container.setAlignment(Qt.AlignCenter)
        self.container.setAdjustWidgetsSize(True)

        # 开始从左到右构建所需控件
        # svg图标
        self.svg_icon = SiSvgLabel(self)
        self.svg_icon.setSvgSize(24, 24)
        self.svg_icon.resize(80, 80)

        # 文字标签
        self.text_label = SiLabel(self)
        self.text_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.text_label.setFixedStyleSheet("padding-top: 20px; padding-bottom: 20px;")

        # 控件紧密排列容器
        self.widgets_container = SiDenseHContainer(self)
        self.widgets_container.setAlignment(Qt.AlignCenter)
        self.widgets_container.resize(0, 0)

        # 添加到整体容器中
        self.container.addWidget(self.svg_icon)
        self.container.addWidget(self.text_label)

        self.container.addPlaceholder(28, "right")  # 防止控件和右侧边缘紧贴
        self.container.addWidget(self.widgets_container, "right")
        self.container.addPlaceholder(16, "right")  # 防止文字和控件紧贴

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

    def setTitle(self, title, subtitle=""):
        """
        为选项卡设置文字
        :param title: 选项卡标题
        :param subtitle: 选项卡副标题
        :return:
        """
        # 根据是否有副标题，设置两种文字显示方式
        if subtitle == "":
            self.text_label.setText("<font color='{}'>{}</font>".format(SiGlobal.siui.colors["TEXT_A"], title))

        else:
            subtitle = subtitle.replace("\n", "<br>")
            self.text_label.setText("<font color='{}'><strong>{}</strong></font><br><font color='{}'>{}</font>".format(
                SiGlobal.siui.colors["TEXT_A"], title, SiGlobal.siui.colors["TEXT_C"], subtitle))

        self.adjustSize()

    def setText(self, text: str):
        raise AttributeError("请使用 setTitle 方法设置选项卡文字")

    def load(self, path_or_data):
        """
        加载图标
        :param path_or_data: svg 文件路径或 svg 数据
        :return:
        """
        self.svg_icon.load(path_or_data)

    def addWidget(self, widget):
        """
        添加控件于选项卡右侧，这将改变控件的父对象
        :param widget: 控件
        :return:
        """
        self.widgets_container.addWidget(widget, "right")

    def adjustSize(self):
        self.container.resize(self.container.width(), self.text_label.height())
        self.container.adjustSize()
        self.resize(self.container.size())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w, h = event.size().width(), event.size().height()

        self.panel.resize(w, h)
        self.container.resize(w, h)

        # 让文字标签充满闲置区域
        spare_space = self.container.getSpareSpace()
        self.text_label.setFixedWidth(spare_space + self.text_label.width())

        # 确保其所有控件都在中轴线上，需要调用调整尺寸方法
        self.container.adjustSize()


class SiOptionCardPlane(ABCSiOptionCardPlane):
    """
    平面式选项卡。相较于其抽象类，此类提供
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 在 header 创建标题
        self.title = SiLabel(self)
        self.title.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.title.setFont(SiFont.tokenized(GlobalFont.M_BOLD))
        self.title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.title.setFixedHeight(32)

        self.header().setAlignment(Qt.AlignCenter)
        self.header().setFixedHeight(64)
        self.header().addWidget(self.title, "left")

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.title.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_A"]))

    def setTitle(self, text: str):
        """
        设置标题
        :param text: 标题
        :return:
        """
        self.title.setText(text)
