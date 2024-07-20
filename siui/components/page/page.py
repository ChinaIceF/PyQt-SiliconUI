from PySide6.QtCore import Qt

from siui.components.widgets.container import SiDenseVContainer, SiDenseHContainer
from siui.components.widgets.label import SiLabel
from siui.components.widgets.scrollarea import SiScrollArea
from siui.core.globals import SiGlobal


class SiPage(SiDenseVContainer):
    """
    页面类，实例化后作为 SiliconApplication 中的单个页面
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSpacing(0)
        self.setUseSignals(True)

        # 滚动区域宽度限制
        self.scroll_maximum_width = 10000

        # 标题引入的高度偏移，内容的高度要减去标题的高度
        self.title_height = 0

        # 左右空白区域的宽度
        self.padding = 0

        # 滚动区域对齐方式
        self.scroll_alignment = Qt.AlignCenter

        # 滚动区域
        self.scroll_area = SiScrollArea(self)
        self.setAdjustWidgetsSize(True)

        # 添加到垂直容器
        self.addWidget(self.scroll_area)

    def setAttachment(self, widget):
        """
        设置子控件
        :param widget: 子控件
        """
        self.scroll_area.setAttachment(widget)

    def attachment(self):
        """
        获取子控件
        """
        return self.scroll_area.attachment()

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

    def setPadding(self, padding):
        """
        内容左右距离边框的距离
        :param padding: 像素数
        """
        self.padding = padding
        self.resize(self.size())

    def setTitle(self, title: str):
        """
        设置页面标题
        :param title: 标题
        """
        # 套标题用的水平容器
        self.title_container = SiDenseHContainer(self)
        self.title_container.setSpacing(0)
        self.title_container.setFixedHeight(32)
        self.title_container.setAlignCenter(True)

        # 标题
        self.title = SiLabel(self)
        self.title.setFont(SiGlobal.siui.fonts["L_BOLD"])
        self.title.setFixedHeight(32)
        self.title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.title.setAutoAdjustSize(True)

        # 添加到水平容器
        self.title_container.addPlaceholder(64)
        self.title_container.addWidget(self.title)

        self.title.setText(title)

        # 添加到垂直容器
        self.addPlaceholder(32, index=0)
        self.addWidget(self.title_container, index=0)
        self.addPlaceholder(32, index=0)

        self.title_height = 96

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.title.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_A"]))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        size = event.size()

        self.scroll_area.resize(size.width(), size.height() - self.title_height)
        self.scroll_area.attachment().setFixedWidth(min(size.width() - self.padding * 2, self.scroll_maximum_width))

        # 处理对齐
        if self.scroll_alignment == Qt.AlignCenter:
            scroll_widget_x = (size.width() - self.scroll_area.attachment().width())//2
        elif self.scroll_alignment == Qt.AlignLeft:
            scroll_widget_x = self.padding
        elif self.scroll_alignment == Qt.AlignRight:
            scroll_widget_x = size.width() - self.scroll_area.attachment().width() - self.padding
        else:
            raise ValueError(f"Invalid alignment value: {self.scroll_alignment}")

        scroll_widget_y = self.scroll_area.attachment().y()

        self.scroll_area.attachment().move(scroll_widget_x, scroll_widget_y)
        self.scroll_area.getAnimationGroup().fromToken("scroll").setTarget([scroll_widget_x, scroll_widget_y])
        self.scroll_area.getAnimationGroup().fromToken("scroll").setCurrent([scroll_widget_x, scroll_widget_y])
