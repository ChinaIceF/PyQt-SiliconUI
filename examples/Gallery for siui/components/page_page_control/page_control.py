from PyQt5.QtCore import Qt

from siui.components import (
    SiPushButton,
    SiTitledWidgetGroup,
)
from siui.components.page import SiPage
from siui.core import SiGlobal

from ..option_card import OptionCardPlaneForWidgetDemos


class ExamplePageControl(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(64)
        self.setScrollMaximumWidth(950)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("页面控制")

        # 创建控件组
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setSpacing(32)
        self.titled_widgets_group.setAdjustWidgetsSize(False)  # 禁用调整宽度

        # 侧边栏信息
        with self.titled_widgets_group as group:
            group.addTitle("页面偏移")

            # 侧边栏信息
            self.global_shifting = OptionCardPlaneForWidgetDemos(self)
            self.global_shifting.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                "/widgets/progress_bar/progress_bar.py")
            self.global_shifting.setTitle("页面偏移")
            self.global_shifting.setFixedWidth(800)

            self.ctrl_shift_left = SiPushButton(self)
            self.ctrl_shift_left.resize(128, 32)
            self.ctrl_shift_left.attachment().setText("向左偏移")
            self.ctrl_shift_left.clicked.connect(
                lambda: SiGlobal.siui.windows["MAIN_WINDOW"].groups()["MAIN_INTERFACE"].moveTo(-100, 0))

            self.ctrl_shift_right = SiPushButton(self)
            self.ctrl_shift_right.resize(128, 32)
            self.ctrl_shift_right.attachment().setText("向右偏移")
            self.ctrl_shift_right.clicked.connect(
                lambda: SiGlobal.siui.windows["MAIN_WINDOW"].groups()["MAIN_INTERFACE"].moveTo(100, 0))

            self.ctrl_shift_restore = SiPushButton(self)
            self.ctrl_shift_restore.resize(128, 32)
            self.ctrl_shift_restore.attachment().setText("恢复")
            self.ctrl_shift_restore.clicked.connect(
                lambda: SiGlobal.siui.windows["MAIN_WINDOW"].groups()["MAIN_INTERFACE"].moveTo(0, 0))

            self.global_shifting.body().addWidget(self.ctrl_shift_left)
            self.global_shifting.body().addWidget(self.ctrl_shift_right)
            self.global_shifting.body().addWidget(self.ctrl_shift_restore)
            self.global_shifting.body().addPlaceholder(12)
            self.global_shifting.adjustSize()

            group.addWidget(self.global_shifting)

        # 添加页脚的空白以增加美观性
        self.titled_widgets_group.addPlaceholder(64)

        # 设置控件组为页面对象
        self.setAttachment(self.titled_widgets_group)
