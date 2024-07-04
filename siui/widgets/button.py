from PyQt5.QtCore import Qt

from siui.gui import SiFont
from siui.gui.colorsets import colorset
from siui.widgets.abstracts import ABCAnimatedWidget, ABCPushButton
from siui.widgets.label import SiIconLabel, SiLabel


class SiPushButton(ABCPushButton):
    """
    PushButton
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.themed = False  # 是否使用主题颜色

        # 实例化文本标签
        self.label = SiIconLabel(self)
        self.label.setAutoAdjustSize(True)
        self.label.setFont(SiFont.fromToken("S_BOLD"))
        self.label.setStyleSheet(f"color: {colorset.color.TEXT_GRAD_HEX[1]}")
        self.label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        # 绑定到主体
        self.setAttachment(self.label)

    def reloadStylesheet(self):
        super().reloadStylesheet()

        # 设置文字颜色
        self.label.setStyleSheet(f"color: {colorset.color.TEXT_GRAD_HEX[0]}")

        # 设置按钮表面和阴影的颜色
        if self.themed is True:
            # 主题样式
            self.body_top.setStyleSheet("""
                background-color:qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                 stop:0 {}, stop:1 {})""".format(*colorset.color.BTN_HL_HEX[0:2]))
            self.body_bottom.setStyleSheet("""
                background-color:qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                 stop:0 {}, stop:1 {})""".format(*colorset.color.BTN_HL_HEX[2:4]))

        else:
            # 非主题样式
            self.body_top.setStyleSheet(f"background-color: {colorset.color.BTN_NORM_HEX[0]}")
            self.body_bottom.setStyleSheet(f"background-color: {colorset.color.BTN_NORM_HEX[1]}")

    def setThemed(self, b: bool):
        """
        设置按钮是否成为主题按钮
        :param b: 是否设为主题按钮
        :return:
        """
        self.themed = b

    def load(self, path_or_data):
        """
        从字符串或者文件加载 svg 数据
        :param path_or_data: 文件路径或是 svg 字符串
        :return:
        """
        self.label.load(path_or_data)

    def setSvgSize(self, w, h):
        """
        设置 svg 图标的大小
        :param w: 宽度
        :param h: 高度
        """
        self.label.setSvgSize(w, h)

    def setText(self, text: str):
        self.label.setText(text)

    def text(self):
        return self.label.text()


