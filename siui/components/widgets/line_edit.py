from PyQt5.QtCore import Qt

from siui.core.globals import SiGlobal
from siui.components.widgets import SiLabel
from siui.components.widgets.abstracts import ABCSiLineEdit


class SiLineEdit(SiLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 创建 LineEdit
        self.line_edit = ABCSiLineEdit(self)
        self.line_edit.setTextMargins(12, 0, 12, 2)
        self.line_edit.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.line_edit.onFocus.connect(self._focus_handler)
        self.line_edit.returnPressed.connect(self.line_edit.clearFocus)  # 按下回车，移出焦点

        # 创建外观标签
        # 承载文字的部分
        self.outfit_label_top = SiLabel(self)
        self.outfit_label_top.lower()
        self.outfit_label_top.setFixedStyleSheet("""border-top-left-radius:4px; border-top-right-radius:4px;
            border-bottom-left-radius:2px; border-bottom-right-radius:2px """)

        # 带主题色的地边条
        self.outfit_label_bottom = SiLabel(self)
        self.outfit_label_bottom.stackUnder(self.outfit_label_top)
        self.outfit_label_bottom.setFixedStyleSheet("border-radius: 4px")

    def reloadStyleSheet(self):
        """
        重载样式表
        """
        super().reloadStyleSheet()

        self.outfit_label_top.setStyleSheet("background-color: {}".format(SiGlobal.siui.colors["INTERFACE_BG_B"]))
        self.outfit_label_bottom.setStyleSheet("""
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {}, stop:1 {});
            """.format(SiGlobal.siui.colors["THEME_TRANSITION_A"], SiGlobal.siui.colors["THEME_TRANSITION_B"]))

    def attachment(self):
        """
        返回 LineEdit 对象
        :return: LineEdit 对象
        """
        return self.line_edit

    def _focus_handler(self, is_on):
        w, h = self.size().width(), self.size().height()
        if is_on:
            self.outfit_label_top.resize(w, h - 2)
        else:
            self.outfit_label_top.resize(w, h - 1)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()
        w, h = size.width(), size.height()

        self.line_edit.resize(w, h)

        self.outfit_label_bottom.resize(w, h)
        self.outfit_label_top.resize(w, h-1)
