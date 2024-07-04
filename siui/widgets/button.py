from siui.widgets.abstracts import ABCPushButton, ABCAnimatedWidget
from siui.widgets.label import SiLabel
from siui.gui.colorsets import colorset
from siui.gui import SiFont

from PyQt5.QtCore import Qt

class SiPushButtonBlank(ABCPushButton):
    """
    所有类型的SiPushButton的基类，只有按钮图形和按钮功能，没有文字或图标\n
    但它提供一个可供绑定的接口，用于绑定任何将放置在按钮正中央的部件
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.themed = False  # 是否使用主题颜色

        # 占位用的被绑定部件，显示在按钮正中央
        self.attachment = ABCAnimatedWidget()

        # 按钮表面
        self.body_top = SiLabel(self)
        self.body_top.lower()

        # 绘制最底层阴影部分
        self.body_bottom = SiLabel(self)
        self.body_bottom.lower()

    def reloadStylesheet(self):
        super().reloadStylesheet()

        # 设置按钮表面的圆角边框
        self.body_top.setFixedStyleSheet("""
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            border-bottom-left-radius: 2px;
            border-bottom-right-radius: 2px;
        """)

        # 设置按钮阴影的圆角边框
        self.body_bottom.setFixedStyleSheet("border-radius: 4px")

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

    def setAttachment(self, widget):
        """
        设置绑定部件。被绑定部件将会被设为按钮的子控件，并显示在按钮的正中央
        :param widget: 部件
        :return:
        """
        self.attachment = widget
        self.attachment.setParent(self)
        self.resize(self.size())  # 实现刷新位置

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.body_top.resize(w, h - 3)
        self.body_bottom.resize(w, h)

        self.attachment.move((w - self.attachment.width()) // 2, (h - 3 - self.attachment.height()) // 2)


class SiPushButton(SiPushButtonBlank):
    """
    可以设置按钮文字的 PushButton
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 实例化文本标签
        self.text_label = SiLabel(self)
        self.text_label.setAutoAdjustSize(True)
        self.text_label.setFont(SiFont.fromToken("S_BOLD"))
        self.text_label.setStyleSheet(f"color: {colorset.color.TEXT_GRAD_HEX[1]}")
        self.text_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        # 绑定到主体
        self.setAttachment(self.text_label)

    def setText(self, text):
        """
        设置按钮的文本
        :param text: 文本
        :return:
        """
        self.text_label.setText(text)

    def text(self):
        """
        获取按钮的文本
        :return:
        """
        return self.text_label.text()

    def reloadStylesheet(self):
        super().reloadStylesheet()

        self.text_label.setStyleSheet(f"color: {colorset.TEXT_GRAD_HEX[0]}")

