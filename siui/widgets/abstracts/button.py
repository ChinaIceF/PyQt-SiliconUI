from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton

from siui.widgets.label import SiColoredLabel, SiLabel


class ABCButton(QPushButton):
    """
    为所有需要点击、按下或松开的场景提供支持的抽象控件
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().setStyleSheet("background-color: transparent")

        self.clicked.connect(self._clicked_slot)

        # 提供悬停时的颜色变化动画
        self.hover_highlight = SiColoredLabel(self)
        self.hover_highlight.stackUnder(self)  # 置于按钮的底部
        self.hover_highlight.setColor("#00FFFFFF")
        self.hover_highlight.getAnimationGroup().fromToken("color").setBias(0.2)
        self.hover_highlight.getAnimationGroup().fromToken("color").setFactor(1/8)

        # 提供点击时的颜色变化动画
        self.flash = SiColoredLabel(self)
        self.flash.stackUnder(self)  # 置于按钮的底部
        self.flash.setColor("#00FFFFFF")
        self.flash.getAnimationGroup().fromToken("color").setBias(0.2)
        self.flash.getAnimationGroup().fromToken("color").setFactor(1/8)

    def setFixedStyleSheet(self, style_sheet):  # 劫持这个按钮的stylesheet，只能设置outfit的样式表
        self.hover_highlight.setFixedStyleSheet(style_sheet)
        self.flash.setFixedStyleSheet(style_sheet)

    def setStyleSheet(self, style_sheet):  # 劫持这个按钮的stylesheet，只能设置outfit的样式表
        self.hover_highlight.setStyleSheet(style_sheet)
        self.flash.setStyleSheet(style_sheet)

    def _clicked_slot(self):
        self.flash.setColor("#10FFFFFF")
        self.flash.setColorTo("#00FFFFFF")

    def enterEvent(self, event):
        super().enterEvent(event)
        self.hover_highlight.setColorTo("#10FFFFFF")

    def leaveEvent(self, event):
        super().enterEvent(event)
        self.hover_highlight.setColorTo("#00FFFFFF")

    def resizeEvent(self, event):
        size = event.size()
        self.hover_highlight.resize(size)
        self.flash.resize(size)


class ABCPushButton(ABCButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置成 pushbutton 的形状
        self.setFixedStyleSheet("""
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            border-bottom-left-radius: 2px;
            border-bottom-right-radius: 2px;
        """)

    def resizeEvent(self, event):
        size = event.size()
        w, h = size.width(), size.height()
        self.hover_highlight.resize(w, h-3)
        self.flash.resize(w, h-3)
