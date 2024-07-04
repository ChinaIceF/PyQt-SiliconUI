from siui.widgets.abstracts import ABCPushButton
from siui.widgets.label import SiLabel
from siui.gui.colorsets import colorset

class SiPushButtonBlank(ABCPushButton):
    """
    所有类型的SiPushButton的基类，只有按钮图形和按钮功能，没有文字或图标
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.themed = False  # 是否使用主题颜色

        # 绘制按钮表面
        self.body_top = SiLabel(self)
        self.body_top.lower()
        self.body_top.setFixedStyleSheet("""
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            border-bottom-left-radius: 2px;
            border-bottom-right-radius: 2px;
        """)

        # 绘制最底层阴影部分
        self.body_bottom = SiLabel(self)
        self.body_bottom.lower()
        self.body_bottom.setFixedStyleSheet("border-radius: 4px")

        # 加载样式表
        self.reloadStylesheet()

    def reloadStylesheet(self):
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

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.body_top.resize(w, h - 3)
        self.body_bottom.resize(w, h)
