from PyQt5.QtCore import Qt, pyqtSignal

from siui.gui import SiFont
from siui.gui.colorsets import colorset
from siui.widgets.abstracts import ABCPushButton, ABCHoldAnimation
from siui.widgets.label import SiIconLabel


class SiPushButton(ABCPushButton):
    """
    点击按钮，可以设置文字、图标或是兼有
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


class SiHoldButton(ABCPushButton):
    holdTimeout = pyqtSignal()  # 长按等待时间超时时触发
    """
    需要持续长按一段时间才能触发点击事件的按钮
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 跟踪按钮按下的状态，用于长按动画的处理
        self.pressed_state = False

        # 实例化动画，由于是特殊化的动画，所以不 tokenize 到动画组
        self.animation_hold = ABCHoldAnimation(self)

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

        self.body_top.setStyleSheet(f"background-color: {colorset.color.BTN_HOLD_HEX[0]}")
        self.body_bottom.setStyleSheet(f"background-color: {colorset.color.BTN_HOLD_HEX[1]}")

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

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.pressed_state = True

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.pressed_state = False

    def isPressed(self):
        """
        返回当前按钮是否处于被按下状态，这个方法往往用于内部使用
        :return: 是否被按下
        """
        return self.pressed_state
