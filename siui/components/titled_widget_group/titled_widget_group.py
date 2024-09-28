from PyQt5.QtCore import Qt

from siui.components.widgets.container import SiDenseVContainer
from siui.components.widgets.label import SiLabel
from siui.core import SiGlobal, GlobalFont
from siui.core import Si
from siui.gui import SiFont


class GroupTitle(SiLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFixedHeight(26)

        # 标题文字
        self.title_label = SiLabel(self)
        self.title_label.setFont(SiFont.tokenized(GlobalFont.M_BOLD))
        self.title_label.setFixedHeight(26)
        self.title_label.setAlignment(Qt.AlignBottom)
        self.title_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)

        # 标题高光，显示在文字下方
        self.title_highlight = SiLabel(self)
        self.title_highlight.lower()
        self.title_highlight.setFixedStyleSheet("border-radius: 4px")

        # 标题指示器，显示在文字左侧
        self.title_indicator = SiLabel(self)
        self.title_indicator.resize(5, 18)
        self.title_indicator.setFixedStyleSheet("border-radius: 2px")

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        self.setStyleSheet("background-color: transparent")
        self.title_label.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_A"]))
        self.title_indicator.setStyleSheet("background-color: {}".format(SiGlobal.siui.colors["TITLE_INDICATOR"]))
        self.title_highlight.setStyleSheet("background-color: {}".format(SiGlobal.siui.colors["TITLE_HIGHLIGHT"]))

    def setText(self, text: str):
        self.title_label.setText(text)
        self.adjustSize()

    def adjustSize(self):
        self.resize(self.title_label.width() + 12 + 4, self.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.title_indicator.move(0, 4)
        self.title_label.move(12, 0)
        self.title_highlight.setGeometry(12, 12, self.title_label.width() + 4, 13)


class SiTitledWidgetGroup(SiDenseVContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setAdjustWidgetsSize(True)
        self.setSpacing(8)

    def addTitle(self, title):
        """
        添加新标题，这将创建一个标题组件并添加到自身中
        :param title: 标题文字
        """
        if len(self.widgets_top) > 0:
            self.addPlaceholder(16)

        new_title = GroupTitle(self)
        new_title.setText(title)
        self.addWidget(new_title)

    def addWidget(self, widget, side="top", index=10000):
        super().addWidget(widget, side, index)
        try:
            widget.resized.connect(self._on_child_resized)
        except:  # noqa: E722
            pass
            # print(f"子控件 {widget} 似乎不具有正确形式的 resized 信号（pyqtSignal(list)）")

    def _on_child_resized(self, _):
        self.adjustSize()
