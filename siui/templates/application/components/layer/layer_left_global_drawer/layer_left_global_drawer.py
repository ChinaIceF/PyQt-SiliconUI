from PyQt5.QtCore import Qt

from siui.components import SiLabel, SiTitledWidgetGroup, SiWidget
from siui.components.slider.slider import SiSliderH
from siui.components.combobox import SiComboBox
from siui.core import SiColor
from siui.core import SiGlobal

from ..global_drawer import SiLayerDrawer


class LayerLeftGlobalDrawer(SiLayerDrawer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.drawer.move(-self.drawer.width(), 0)

        self.drawer_widget_group = SiTitledWidgetGroup(self)
        self.drawer_widget_group.setSpacing(8)

        self.drawer_page.setPadding(48)
        self.drawer_page.setTitle("全局左侧抽屉")
        self.drawer_page.title.setContentsMargins(32, 0, 0, 0)
        self.drawer_page.setScrollAlignment(Qt.AlignLeft)

        with self.drawer_widget_group as group:
            group.addTitle("全局性")

            self.text_label = SiLabel(self)
            self.text_label.setTextColor(self.getColor(SiColor.TEXT_D))
            self.text_label.setWordWrap(True)
            self.text_label.setText("这里是全局抽屉，无论在何种情况下，该抽屉被打开时都会令界面发生侧移，保证抽屉正常展开\n\n"
                                    "不同于其他页面，全局抽屉推荐为唯一的，全局抽屉中的控件推荐为静态的")
            self.text_label.setFixedHeight(128)

            group.addWidget(self.text_label)

        with self.drawer_widget_group as group:
            group.addTitle("声音")

            self.label_output_device = SiLabel(self)
            self.label_output_device.setTextColor(self.getColor(SiColor.TEXT_C))
            self.label_output_device.setText("输出设备")

            self.demo_output_device = SiComboBox(self)
            self.demo_output_device.resize(256, 32)
            self.demo_output_device.addOption("默认设备")
            self.demo_output_device.addOption("RealTek(R) Output")
            self.demo_output_device.addOption("姬霓太美(R) Output")
            self.demo_output_device.menu().setShowIcon(False)
            self.demo_output_device.menu().setIndex(0)

            self.label_slider_1 = SiLabel(self)
            self.label_slider_1.setTextColor(self.getColor(SiColor.TEXT_C))
            self.label_slider_1.setText("总音量")

            self.demo_slider_1 = SiSliderH(self)
            self.demo_slider_1.resize(0, 16)
            self.demo_slider_1.setMinimum(0)
            self.demo_slider_1.setMaximum(100)
            self.demo_slider_1.setValue(80, move_to=False)

            self.label_slider_2 = SiLabel(self)
            self.label_slider_2.setTextColor(self.getColor(SiColor.TEXT_C))
            self.label_slider_2.setText("音乐音量")

            self.demo_slider_2 = SiSliderH(self)
            self.demo_slider_2.resize(0, 16)
            self.demo_slider_2.setMinimum(0)
            self.demo_slider_2.setMaximum(100)
            self.demo_slider_2.setValue(100, move_to=False)

            self.label_slider_3 = SiLabel(self)
            self.label_slider_3.setTextColor(self.getColor(SiColor.TEXT_C))
            self.label_slider_3.setText("音效音量")

            self.demo_slider_3 = SiSliderH(self)
            self.demo_slider_3.resize(0, 16)
            self.demo_slider_3.setMinimum(0)
            self.demo_slider_3.setMaximum(100)
            self.demo_slider_3.setValue(61, move_to=False)

            group.addWidget(self.label_output_device)
            group.addWidget(self.demo_output_device)
            group.addPlaceholder(8)
            group.addWidget(self.label_slider_1)
            group.addWidget(self.demo_slider_1)
            group.addPlaceholder(8)
            group.addWidget(self.label_slider_2)
            group.addWidget(self.demo_slider_2)
            group.addPlaceholder(8)
            group.addWidget(self.label_slider_3)
            group.addWidget(self.demo_slider_3)

        group.addPlaceholder(64)

        self.drawer_page.setAttachment(self.drawer_widget_group)

    def setOpened(self, state):
        super().setOpened(state)
        if state:
            self.drawer.moveTo(0, 0)
        else:
            self.drawer.moveTo(-self.drawer.width(), 0)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()
        self.drawer_panel.setStyleSheet(
            f"background-color: {self.getColor(SiColor.INTERFACE_BG_C)};"
            f"border-right: 1px solid {self.getColor(SiColor.INTERFACE_BG_D)}"
        )

    def showLayer(self):
        super().showLayer()
        SiGlobal.siui.windows["MAIN_WINDOW"].groups()["MAIN_INTERFACE"].moveTo(100, 0)

    def closeLayer(self):
        super().closeLayer()
        SiGlobal.siui.windows["MAIN_WINDOW"].groups()["MAIN_INTERFACE"].moveTo(0, 0)
