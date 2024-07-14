from PyQt5.QtCore import Qt

from siui.components.widgets.container import SiDenseVContainer
from siui.components.widgets.label import SiLabel
from siui.components.widgets.scrollarea import SiScrollArea
from siui.core.globals import SiGlobal


class SiPage(SiDenseVContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSpacing(0)

        # 滚动区域宽度限制
        self.scroll_maximum_width = 10000

        # 左对齐横坐标偏移量
        self.x_offset_on_align_left = 0

        # 滚动区域对齐方式
        self.scroll_alignment = Qt.AlignCenter

        # 标题
        self.title = SiLabel(self)
        self.title.setFixedStyleSheet("padding-left: 64px")
        self.title.setFont(SiGlobal.siui.fonts["L_BOLD"])
        self.title.setFixedHeight(32)
        self.title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.title.setAutoAdjustSize(True)

        # 滚动区域
        self.scroll_area = SiScrollArea(self)

        self.addPlaceholder(32)
        self.addWidget(self.title)
        self.addPlaceholder(32)
        self.addWidget(self.scroll_area)

    def setScrollMaximumWidth(self, width: int):
        """
        设置滚动区域的子控件的最大宽度
        :param width: 最大宽度
        :return:
        """
        self.scroll_maximum_width = width
        self.resize(self.size())

    def setScrollAlignment(self, a0):
        """
        设置滚动区域的对齐方式
        :param a0: Qt 枚举值
        """
        if a0 not in [Qt.AlignCenter, Qt.AlignLeft, Qt.AlignRight]:
            raise ValueError(f"Invalid alignment value: {a0}")
        self.scroll_alignment = a0
        self.resize(self.size())

    def setXOffsetOnAlignLeft(self, offset):
        """
        当内容中置时，横坐标的偏移量
        :param offset: 像素数
        """
        self.x_offset_on_align_left = offset
        self.resize(self.size())

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.title.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_A"]))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()

        self.scroll_area.resize(size.width(), size.height() - 96)
        self.scroll_area.attachment().setFixedWidth(min(size.width(), self.scroll_maximum_width))

        # 处理对齐
        if self.scroll_alignment == Qt.AlignCenter:
            scroll_widget_x = (size.width() - self.scroll_area.attachment().width())//2 + self.x_offset_on_align_left
        elif self.scroll_alignment == Qt.AlignLeft:
            scroll_widget_x = 0
        elif self.scroll_alignment == Qt.AlignRight:
            scroll_widget_x = size.width() - self.scroll_area.attachment().width()
        else:
            raise ValueError(f"Invalid alignment value: {self.scroll_alignment}")

        self.scroll_area.attachment().move(scroll_widget_x, self.scroll_area.attachment().y())



