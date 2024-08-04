from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel

from siui.components import SiDenseVContainer, SiFlowContainer, SiLabel, SiOptionCardPlane, SiSimpleButton, SiWidget, \
    SiScrollArea, SiDenseHContainer, SiPushButton
from siui.components.page import SiPage
from siui.core.color import SiColor
from siui.core.effect import SiQuickEffect
from siui.core.globals import SiGlobal
from siui.core.silicon import Si


def get_on_button_clicked_func(button):
    return lambda: SiGlobal.siui.windows["TOOL_TIP"].setText(
                f"{button.objectName()}<br>"
                f'<span style="color: {button.colorGroup().fromToken(SiColor.TEXT_D)}">复制成功</span>',
            )


class ExampleIcons(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.icon_page_index = 0

        self.setPadding(64)
        self.setScrollMaximumWidth(950)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("图标库")

        self.content_container = SiDenseVContainer(self)
        self.content_container.setAlignCenter(True)
        self.content_container.setAdjustWidgetsSize(True)

        self.icon_scroll_area = SiScrollArea(self)

        self.icon_container = SiFlowContainer(self)
        self.icon_container.setLineHeight(96)

        self.icon_scroll_area.setAttachment(self.icon_container)

        self.operation_panel_container_v = SiDenseVContainer(self)
        self.operation_panel_container_v.setAlignCenter(True)

        self.operation_panel_container_h = SiDenseHContainer(self)
        self.operation_panel_container_h.setFixedHeight(48)
        self.operation_panel_container_h.setAlignCenter(True)
        SiQuickEffect.applyDropShadowOn(self.operation_panel_container_h,
                                        color=(0, 0, 0, 50),
                                        blur_radius=32)

        self.page_up_button = SiPushButton(self)
        self.page_up_button.attachment().setText("上一页")
        self.page_up_button.setFixedSize(128, 32)
        self.page_up_button.clicked.connect(lambda: self.load_icon_page_to(self.icon_page_index - 1))

        self.page_index_label = SiLabel(self)
        self.page_index_label.setAlignment(Qt.AlignVCenter)
        self.page_index_label.setFixedHeight(32)
        self.page_index_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.page_index_label.setStyleSheet("color: {}".format(self.colorGroup().fromToken(SiColor.TEXT_D)))

        self.page_down_button = SiPushButton(self)
        self.page_down_button.attachment().setText("下一页")
        self.page_down_button.setFixedSize(128, 32)
        self.page_down_button.clicked.connect(lambda: self.load_icon_page_to(self.icon_page_index + 1))

        self.operation_panel_container_h.addWidget(self.page_up_button)
        self.operation_panel_container_h.addWidget(self.page_index_label)
        self.operation_panel_container_h.addWidget(self.page_down_button)
        self.operation_panel_container_h.adjustSize()

        self.operation_panel_container_v.addWidget(self.operation_panel_container_h)

        self.content_container.addWidget(self.icon_scroll_area)
        self.content_container.addWidget(self.operation_panel_container_v, "bottom")

        # load icon page 0
        self.load_icon_page_to(0)

    def load_icon_page_to(self, page_index):
        if (page_index < 0) or (page_index > len(SiGlobal.siui.icons.keys()) // 50 + 1):
            return

        self.icon_page_index = page_index
        self.page_index_label.setText("{}/{}".format(self.icon_page_index+1, len(SiGlobal.siui.icons.keys()) // 50 + 2))
        self.operation_panel_container_h.adjustSize()

        for index, widget in enumerate(list(self.icon_container.widgets())):
            self.icon_container.removeWidget(widget, fade_out=True, fade_out_delay=index*3)

        self.icon_container.setVisible(True)
        from_index, to_index = 50*page_index, 50*(page_index+1)
        for key, value in list(zip(SiGlobal.siui.icons.keys(), SiGlobal.siui.icons.values()))[from_index:to_index]:
            widget = SiLabel(self)
            widget.setFixedSize(96, 96)
            widget.setObjectName(key)

            svg_button = SiSimpleButton(widget)
            svg_button.colorGroup().assign(SiColor.BUTTON_OFF,
                                           svg_button.colorGroup().fromToken(SiColor.INTERFACE_BG_C))
            svg_button.attachment().setSvgSize(32, 32)
            svg_button.attachment().load(value)
            svg_button.setFixedSize(96, 96)
            svg_button.setHint(
                f"{key}<br>"
                f'<span style="color: {self.colorGroup().fromToken(SiColor.TEXT_D)}">点击复制图标名称</span>'
            )
            svg_button.clicked.connect(get_on_button_clicked_func(widget))
            svg_button.reloadStyleSheet()

            self.icon_container.addWidget(widget, arrange=False)
            widget.show()

        self.icon_container.arrangeWidgets(ani=False, all_fade_in=True, fade_in_delay=50, fade_in_delay_cumulate_rate=2)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.icon_container.resize(event.size().width() - 2 * self.padding, self.icon_container.height())
        self.icon_container.arrangeWidgets()
        self.icon_container.adjustSize()

        self.content_container.setGeometry(self.padding,
                                           self.title_height,
                                           event.size().width() - 2 * self.padding,
                                           event.size().height() - self.title_height - 64)
        self.content_container.adjustWidgetsGeometry()
        self.icon_scroll_area.resize(self.icon_scroll_area.width(), self.content_container.height() - 64)

    def showEvent(self, a0):
        super().showEvent(a0)
        self.icon_container.arrangeWidgets(ani=False, all_fade_in=True, fade_in_delay=0, fade_in_delay_cumulate_rate=2)