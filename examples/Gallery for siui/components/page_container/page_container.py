from PyQt5.QtCore import Qt

from siui.components import SiTitledWidgetGroup, SiLabel, SiDenseHContainer, SiDenseVContainer, SiDividedHContainer, \
    SiDividedVContainer, SiFlowContainer, SiDraggableLabel, SiSimpleButton, SiPushButton, SiMasonryContainer
from siui.components.page import SiPage
from siui.core import SiColor, GlobalFont
from siui.core import SiGlobal
from siui.core import Si
from siui.gui import SiFont
from ..option_card import OptionCardPlaneForWidgetDemos

import random


class DemoLabel(SiLabel):
    def __init__(self, parent, text):
        super().__init__(parent)

        self.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(32)

        self.setFixedStyleSheet("border-radius: 4px")
        self.setText(text)
        self.adjustSize()
        self.resize(self.width() + 24, self.height())

    def reloadStyleSheet(self):
        self.setStyleSheet(f"color: {self.getColor(SiColor.TEXT_B)};"
                           f"background-color: {self.getColor(SiColor.INTERFACE_BG_D)}")


class ExampleContainer(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.message_type = 0

        self.setPadding(64)
        self.setScrollMaximumWidth(1000)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("容器")

        # 创建控件组
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setSpacing(32)
        self.titled_widgets_group.setAdjustWidgetsSize(True)

        # 密堆积容器
        with self.titled_widgets_group as group:
            group.addTitle("密堆积容器")

            # 水平密堆积容器
            self.dense_h_container = OptionCardPlaneForWidgetDemos(self)
            self.dense_h_container.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                    "/widgets/progress_bar/progress_bar.py")
            self.dense_h_container.setTitle("水平密堆积容器")

            self.demo_dense_h_container = SiDenseHContainer(self)
            self.demo_dense_h_container.setFixedHeight(32)
            self.demo_dense_h_container.addWidget(DemoLabel(self, "左侧A"), "left")
            self.demo_dense_h_container.addWidget(DemoLabel(self, "左侧B"), "left")
            self.demo_dense_h_container.addWidget(DemoLabel(self, "左侧C"), "left")
            self.demo_dense_h_container.addWidget(DemoLabel(self, "..."), "left")
            self.demo_dense_h_container.addWidget(DemoLabel(self, "右侧A"), "right")
            self.demo_dense_h_container.addWidget(DemoLabel(self, "右侧B"), "right")
            self.demo_dense_h_container.addWidget(DemoLabel(self, "右侧C"), "right")
            self.demo_dense_h_container.addWidget(DemoLabel(self, "..."), "right")

            self.dense_h_container.body().setAdjustWidgetsSize(True)
            self.dense_h_container.body().addWidget(self.demo_dense_h_container)
            self.dense_h_container.body().addPlaceholder(12)
            self.dense_h_container.adjustSize()

            # 竖直密堆积容器
            self.dense_v_container = OptionCardPlaneForWidgetDemos(self)
            self.dense_v_container.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                    "/widgets/progress_bar/progress_bar.py")
            self.dense_v_container.setTitle("竖直密堆积容器")

            self.demo_dense_v_container = SiDenseVContainer(self)
            self.demo_dense_v_container.setFixedHeight(300)
            self.demo_dense_v_container.addWidget(DemoLabel(self, "顶侧A"), "top")
            self.demo_dense_v_container.addWidget(DemoLabel(self, "顶侧B"), "top")
            self.demo_dense_v_container.addWidget(DemoLabel(self, "..."), "top")
            self.demo_dense_v_container.addWidget(DemoLabel(self, "底侧A"), "bottom")
            self.demo_dense_v_container.addWidget(DemoLabel(self, "底侧B"), "bottom")
            self.demo_dense_v_container.addWidget(DemoLabel(self, "..."), "bottom")

            self.dense_v_container.body().addWidget(self.demo_dense_v_container)
            self.dense_v_container.body().addPlaceholder(12)
            self.dense_v_container.adjustSize()

            group.addWidget(self.dense_h_container)
            group.addWidget(self.dense_v_container)

        # 分割容器
        with self.titled_widgets_group as group:
            group.addTitle("分割容器")

            # 水平分割容器
            self.divided_h_container = OptionCardPlaneForWidgetDemos(self)
            self.divided_h_container.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                    "/widgets/progress_bar/progress_bar.py")
            self.divided_h_container.setTitle("水平分割容器")

            self.indicator_container_divided_h_container = SiDenseHContainer(self)
            self.indicator_container_divided_h_container.setSpacing(0)
            self.indicator_container_divided_h_container.setFixedHeight(4)

            self.indicator_h_80 = SiLabel(self)
            self.indicator_h_80.resize(120, 4)
            self.indicator_h_80.setHint("该 Section 宽 120 像素")
            self.indicator_h_80.setFixedStyleSheet("border-radius: 2px")
            self.indicator_h_80.setColor(SiColor.trans(self.getColor(SiColor.THEME), 0.2))

            self.indicator_h_120 = SiLabel(self)
            self.indicator_h_120.resize(180, 4)
            self.indicator_h_120.setHint("该 Section 宽 180 像素")
            self.indicator_h_120.setFixedStyleSheet("border-radius: 2px")
            self.indicator_h_120.setColor(SiColor.trans(self.getColor(SiColor.THEME), 0.5))

            self.indicator_h_180 = SiLabel(self)
            self.indicator_h_180.resize(240, 4)
            self.indicator_h_180.setHint("该 Section 宽 240 像素")
            self.indicator_h_180.setFixedStyleSheet("border-radius: 2px")
            self.indicator_h_180.setColor(SiColor.trans(self.getColor(SiColor.THEME), 1.0))

            self.indicator_container_divided_h_container.addWidget(self.indicator_h_80)
            self.indicator_container_divided_h_container.addWidget(self.indicator_h_120)
            self.indicator_container_divided_h_container.addWidget(self.indicator_h_180)

            self.demo_divided_h_container = SiDividedHContainer(self)
            self.demo_divided_h_container.setFixedWidth(540)
            self.demo_divided_h_container.addSection(width=120, height=32, alignment=Qt.AlignLeft)
            self.demo_divided_h_container.addSection(width=180, height=32, alignment=Qt.AlignCenter)
            self.demo_divided_h_container.addSection(width=240, height=32, alignment=Qt.AlignRight)
            self.demo_divided_h_container.addWidget(DemoLabel(self, "120左对齐"))
            self.demo_divided_h_container.addWidget(DemoLabel(self, "180中心对齐"))
            self.demo_divided_h_container.addWidget(DemoLabel(self, "240右对齐"))
            self.demo_divided_h_container.adjustSize()
            self.demo_divided_h_container.arrangeWidgets()

            self.divided_h_container.body().addWidget(self.indicator_container_divided_h_container)
            self.divided_h_container.body().addWidget(self.demo_divided_h_container)
            self.divided_h_container.body().addPlaceholder(12)
            self.divided_h_container.adjustSize()

            # 垂直分割容器
            self.divided_v_container = OptionCardPlaneForWidgetDemos(self)
            self.divided_v_container.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                    "/widgets/progress_bar/progress_bar.py")
            self.divided_v_container.setTitle("垂直分割容器")

            self.container_h_for_divided_v_container = SiDenseHContainer(self)
            self.container_h_for_divided_v_container.setFixedHeight(192)

            self.indicator_container_divided_v_container = SiDenseVContainer(self)
            self.indicator_container_divided_v_container.setSpacing(0)
            self.indicator_container_divided_v_container.setFixedWidth(4)

            self.indicator_v_48 = SiLabel(self)
            self.indicator_v_48.resize(4, 48)
            self.indicator_v_48.setHint("该 Section 高 48 像素")
            self.indicator_v_48.setFixedStyleSheet("border-radius: 2px")
            self.indicator_v_48.setColor(SiColor.trans(self.getColor(SiColor.THEME), 0.2))

            self.indicator_v_64 = SiLabel(self)
            self.indicator_v_64.resize(4, 64)
            self.indicator_v_64.setHint("该 Section 高 64 像素")
            self.indicator_v_64.setFixedStyleSheet("border-radius: 2px")
            self.indicator_v_64.setColor(SiColor.trans(self.getColor(SiColor.THEME), 0.5))

            self.indicator_v_80 = SiLabel(self)
            self.indicator_v_80.resize(4, 80)
            self.indicator_v_80.setHint("该 Section 高 80 像素")
            self.indicator_v_80.setFixedStyleSheet("border-radius: 2px")
            self.indicator_v_80.setColor(SiColor.trans(self.getColor(SiColor.THEME), 1.0))

            self.indicator_container_divided_v_container.addWidget(self.indicator_v_48)
            self.indicator_container_divided_v_container.addWidget(self.indicator_v_64)
            self.indicator_container_divided_v_container.addWidget(self.indicator_v_80)

            self.demo_divided_v_container = SiDividedVContainer(self)
            self.demo_divided_v_container.setFixedSize(300, 192)
            self.demo_divided_v_container.addSection(width=256, height=48, alignment=Qt.AlignTop)
            self.demo_divided_v_container.addSection(width=256, height=64, alignment=Qt.AlignVCenter)
            self.demo_divided_v_container.addSection(width=256, height=80, alignment=Qt.AlignBottom)
            self.demo_divided_v_container.addWidget(DemoLabel(self, "48上对齐"))
            self.demo_divided_v_container.addWidget(DemoLabel(self, "64中心对齐"))
            self.demo_divided_v_container.addWidget(DemoLabel(self, "80下对齐"))
            self.demo_divided_v_container.adjustSize()
            self.demo_divided_v_container.arrangeWidgets()

            self.container_h_for_divided_v_container.addWidget(self.indicator_container_divided_v_container)
            self.container_h_for_divided_v_container.addWidget(self.demo_divided_v_container)

            self.divided_v_container.body().addWidget(self.container_h_for_divided_v_container)
            self.divided_v_container.body().addPlaceholder(12)
            self.divided_v_container.adjustSize()

            group.addWidget(self.divided_h_container)
            group.addWidget(self.divided_v_container)

        # 流式布局容器
        with self.titled_widgets_group as group:
            group.addTitle("流式布局容器")

            # 流式布局
            self.flow_container = OptionCardPlaneForWidgetDemos(self)
            self.flow_container.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                 "/widgets/progress_bar/progress_bar.py")
            self.flow_container.setTitle("经典流式布局容器")
            self.flow_container.setAdditionalDescription("支持拖拽")

            self.demo_flow_container = SiFlowContainer(self)
            self.demo_flow_container.resize(1000, 32)
            self.demo_flow_container.setSiliconWidgetFlag(Si.EnableAnimationSignals)

            for _ in range(15):
                label = SiDraggableLabel(self)
                button = SiSimpleButton(label)
                button.attachment().setFont(SiFont.tokenized(GlobalFont.S_NORMAL))
                button.attachment().setText(str(round(random.random(), int(6 * random.random() + 2))))
                button.colorGroup().assign(SiColor.BUTTON_OFF, button.getColor(SiColor.INTERFACE_BG_D))
                button.setFixedHeight(32)
                button.adjustSize()
                button.setAttribute(Qt.WA_TransparentForMouseEvents)
                label.button = button
                label.resize(button.size())
                self.demo_flow_container.addWidget(label, ani=False)
                self.demo_flow_container.regDraggableWidget(label)
            self.demo_flow_container.adjustSize()

            container_flow_cont_buttons = SiDenseHContainer(self)
            container_flow_cont_buttons.setFixedHeight(32)

            self.ctrl_flow_cont_fade_in = SiPushButton(self)
            self.ctrl_flow_cont_fade_in.resize(128, 32)
            self.ctrl_flow_cont_fade_in.attachment().setText("淡入")
            self.ctrl_flow_cont_fade_in.clicked.connect(
                lambda: self.demo_flow_container.arrangeWidgets(ani=False, all_fade_in=True)
            )

            self.ctrl_flow_cont_shuffle = SiPushButton(self)
            self.ctrl_flow_cont_shuffle.resize(128, 32)
            self.ctrl_flow_cont_shuffle.attachment().setText("打乱顺序")
            self.ctrl_flow_cont_shuffle.clicked.connect(lambda: self.demo_flow_container.shuffle(ani=True))

            self.ctrl_flow_cont_last_to_front = SiPushButton(self)
            self.ctrl_flow_cont_last_to_front.resize(128, 32)
            self.ctrl_flow_cont_last_to_front.attachment().setText("末尾元素提前")
            self.ctrl_flow_cont_last_to_front.clicked.connect(
                lambda: self.demo_flow_container.insertToByIndex(
                    len(self.demo_flow_container.widgets())-1,
                    0,
                    no_ani_exceptions=[self.demo_flow_container.widgets()[len(self.demo_flow_container.widgets())-1]]
                )
            )

            container_flow_cont_buttons.addWidget(self.ctrl_flow_cont_fade_in)
            container_flow_cont_buttons.addWidget(self.ctrl_flow_cont_shuffle)
            container_flow_cont_buttons.addWidget(self.ctrl_flow_cont_last_to_front)

            self.flow_container.body().setAdjustWidgetsSize(True)
            self.flow_container.body().addWidget(self.demo_flow_container)
            self.flow_container.body().addWidget(container_flow_cont_buttons)
            self.flow_container.body().addPlaceholder(12)
            self.flow_container.adjustSize()

            # 瀑布流
            self.masonry_container = OptionCardPlaneForWidgetDemos(self)
            self.masonry_container.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                    "/widgets/progress_bar/progress_bar.py")
            self.masonry_container.setTitle("瀑布流容器")
            self.masonry_container.setAdditionalDescription("支持拖拽")

            self.demo_masonry_container = SiMasonryContainer(self)
            self.demo_masonry_container.setAutoAdjustColumnAmount(True)
            self.demo_masonry_container.setColumns(4)

            for _ in range(16):
                label = SiDraggableLabel(self)
                button = SiSimpleButton(label)
                button.colorGroup().assign(SiColor.BUTTON_OFF, button.getColor(SiColor.INTERFACE_BG_D))
                button.resize(160, int(random.random() * 50 + 70))
                button.setAttribute(Qt.WA_TransparentForMouseEvents)
                label.button = button
                label.setFixedStyleSheet("border-radius: 4px")
                label.setColor(self.getColor(SiColor.INTERFACE_BG_D))
                label.resize(button.size())

                self.demo_masonry_container.addWidget(label, ani=False)
                self.demo_masonry_container.regDraggableWidget(label)

            self.masonry_container.body().setAdjustWidgetsSize(True)
            self.masonry_container.body().addWidget(self.demo_masonry_container)
            self.masonry_container.body().addPlaceholder(12)
            self.masonry_container.adjustSize()

            group.addWidget(self.flow_container)
            group.addWidget(self.masonry_container)

        # 添加页脚的空白以增加美观性
        self.titled_widgets_group.addPlaceholder(64)

        # 设置控件组为页面对象
        self.setAttachment(self.titled_widgets_group)
