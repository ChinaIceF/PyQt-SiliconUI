from PyQt5.QtCore import Qt

from siui.components import (
    SiDenseHContainer,
    SiOptionCardLinear,
    SiPushButton,
    SiTitledWidgetGroup,
)
from siui.components.combobox import SiComboBox
from siui.components.page import SiPage
from siui.components.spinbox.spinbox import SiDoubleSpinBox
from siui.core import SiGlobal

from ..option_card import OptionCardPlaneForWidgetDemos
from .components.child_page_example import ChildPageExample, ChildPageExample2
from .components.modal_dialog_example import ModalDialogExample
from .components.side_msg_box import send_custom_message, send_simple_message, send_titled_message


class ExampleDialogs(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.message_auto_close_duration = None
        self.message_auto_close = None
        self.message_type = 0

        self.setPadding(64)
        self.setScrollMaximumWidth(950)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("消息与二级界面")

        # 创建控件组
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setSpacing(32)
        self.titled_widgets_group.setAdjustWidgetsSize(False)  # 禁用调整宽度

        # 侧边栏信息
        with self.titled_widgets_group as group:
            group.addTitle("侧边栏信息")

            # 侧边栏信息
            self.side_messages = OptionCardPlaneForWidgetDemos(self)
            self.side_messages.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                "/widgets/progress_bar/progress_bar.py")
            self.side_messages.setTitle("侧边栏信息")
            self.side_messages.setFixedWidth(800)

            side_message_container = SiDenseHContainer(self)
            side_message_container.setFixedHeight(32)

            self.demo_send_message_to_sidebar = SiPushButton(self)
            self.demo_send_message_to_sidebar.resize(128, 32)
            self.demo_send_message_to_sidebar.attachment().setText("发送测试信息")
            self.demo_send_message_to_sidebar.clicked.connect(
                lambda: send_simple_message(self.message_type, self.message_auto_close, self.message_auto_close_duration))

            self.demo_send_message_to_sidebar_titled = SiPushButton(self)
            self.demo_send_message_to_sidebar_titled.resize(128, 32)
            self.demo_send_message_to_sidebar_titled.attachment().setText("具标题测试信息")
            self.demo_send_message_to_sidebar_titled.clicked.connect(
                lambda: send_titled_message(self.message_type, self.message_auto_close, self.message_auto_close_duration))

            self.demo_send_message_to_sidebar_custom = SiPushButton(self)
            self.demo_send_message_to_sidebar_custom.resize(128, 32)
            self.demo_send_message_to_sidebar_custom.attachment().setText("发送自定义信息")
            self.demo_send_message_to_sidebar_custom.clicked.connect(
                lambda: send_custom_message(self.message_type, self.message_auto_close, self.message_auto_close_duration))

            side_message_container.addWidget(self.demo_send_message_to_sidebar)
            side_message_container.addWidget(self.demo_send_message_to_sidebar_titled)
            side_message_container.addWidget(self.demo_send_message_to_sidebar_custom)

            # -- 信息类型
            self.ctrl_type_combobox = SiComboBox(self)
            self.ctrl_type_combobox.resize(80, 32)
            self.ctrl_type_combobox.addOption("标准", value=0)
            self.ctrl_type_combobox.addOption("成功", value=1)
            self.ctrl_type_combobox.addOption("提示", value=2)
            self.ctrl_type_combobox.addOption("警告", value=3)
            self.ctrl_type_combobox.addOption("错误", value=4)
            self.ctrl_type_combobox.menu().setShowIcon(False)
            self.ctrl_type_combobox.menu().setIndex(0)
            self.ctrl_type_combobox.valueChanged.connect(self.set_message_box_type)

            self.option_card_type = SiOptionCardLinear(self)
            self.option_card_type.load(SiGlobal.siui.iconpack.get("ic_fluent_tag_multiple_regular"))
            self.option_card_type.setTitle("信息类型", "使用不同的信息类型以提供更直观的提示")
            self.option_card_type.addWidget(self.ctrl_type_combobox)

            # -- 自动消失
            self.ctrl_auto_close = SiComboBox(self)
            self.ctrl_auto_close.resize(80, 32)
            self.ctrl_auto_close.addOption("禁用", value=False)
            self.ctrl_auto_close.addOption("启用", value=True)
            self.ctrl_auto_close.menu().setShowIcon(False)
            self.ctrl_auto_close.menu().setIndex(0)
            self.ctrl_auto_close.valueChanged.connect(self.set_message_box_auto_close)

            self.option_card_auto_close = SiOptionCardLinear(self)
            self.option_card_auto_close.load(SiGlobal.siui.iconpack.get("ic_fluent_panel_right_contract_regular"))
            self.option_card_auto_close.setTitle("自动隐藏", "以降低操作复杂性，或是保留重要信息")
            self.option_card_auto_close.addWidget(self.ctrl_auto_close)

            # -- 停留时长
            self.ctrl_stay_duration = SiDoubleSpinBox(self)
            self.ctrl_stay_duration.resize(128, 32)
            self.ctrl_stay_duration.lineEdit().textChanged.connect(self.set_message_box_auto_close)
            self.ctrl_stay_duration.setValue(1.0)

            self.option_card_stay_duration = SiOptionCardLinear(self)
            self.option_card_stay_duration.load(SiGlobal.siui.iconpack.get("ic_fluent_timer_regular"))
            self.option_card_stay_duration.setTitle("停留时长", "如果自动隐藏被启用，提示消息将在设定的秒数后隐藏")
            self.option_card_stay_duration.addWidget(self.ctrl_stay_duration)

            self.side_messages.body().setAdjustWidgetsSize(True)
            self.side_messages.body().addWidget(side_message_container)
            self.side_messages.body().addWidget(self.option_card_type)
            self.side_messages.body().addWidget(self.option_card_auto_close)
            self.side_messages.body().addWidget(self.option_card_stay_duration)
            self.side_messages.body().addPlaceholder(12)
            self.side_messages.adjustSize()

            group.addWidget(self.side_messages)

        # 全局侧边抽屉
        with self.titled_widgets_group as group:
            group.addTitle("全局侧边抽屉")

            # 子页面
            self.global_drawer_left = OptionCardPlaneForWidgetDemos(self)
            self.global_drawer_left.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                              "/widgets/progress_bar/progress_bar.py")
            self.global_drawer_left.setTitle("全局左侧抽屉")
            self.global_drawer_left.setFixedWidth(800)

            self.ctrl_show_global_drawer_left = SiPushButton(self)
            self.ctrl_show_global_drawer_left.resize(128, 32)
            self.ctrl_show_global_drawer_left.attachment().setText("打开")
            self.ctrl_show_global_drawer_left.clicked.connect(
                lambda: SiGlobal.siui.windows["MAIN_WINDOW"].layerLeftGlobalDrawer().showLayer()
            )

            self.ctrl_new_page = SiPushButton(self)
            self.ctrl_new_page.resize(128, 32)
            self.ctrl_new_page.attachment().setText("DEBUG: 新页面")
            self.ctrl_new_page.clicked.connect(
                lambda: SiGlobal.siui.windows["MAIN_WINDOW"].layerMain().addPage(ExampleDialogs(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_info_filled"),
                                 hint="关于", side="top")
            )

            self.global_drawer_left.body().addWidget(self.ctrl_show_global_drawer_left)
            self.global_drawer_left.body().addWidget(self.ctrl_new_page)
            self.global_drawer_left.body().addPlaceholder(12)
            self.global_drawer_left.adjustSize()

            group.addWidget(self.global_drawer_left)

        # 二级界面
        with self.titled_widgets_group as group:
            group.addTitle("二级界面")

            # 子页面
            self.child_pages = OptionCardPlaneForWidgetDemos(self)
            self.child_pages.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                              "/widgets/progress_bar/progress_bar.py")
            self.child_pages.setTitle("子页面")
            self.child_pages.setFixedWidth(800)

            self.ctrl_show_child_pages_example = SiPushButton(self)
            self.ctrl_show_child_pages_example.resize(128, 32)
            self.ctrl_show_child_pages_example.attachment().setText("显示示例子页面A")
            self.ctrl_show_child_pages_example.clicked.connect(
                lambda: SiGlobal.siui.windows["MAIN_WINDOW"].layerChildPage().setChildPage(ChildPageExample(self))
            )

            self.ctrl_show_child_pages_example2 = SiPushButton(self)
            self.ctrl_show_child_pages_example2.resize(128, 32)
            self.ctrl_show_child_pages_example2.attachment().setText("显示示例子页面B")
            self.ctrl_show_child_pages_example2.clicked.connect(
                lambda: SiGlobal.siui.windows["MAIN_WINDOW"].layerChildPage().setChildPage(ChildPageExample2(self))
            )

            self.child_pages.body().addWidget(self.ctrl_show_child_pages_example)
            self.child_pages.body().addWidget(self.ctrl_show_child_pages_example2)
            self.child_pages.body().addPlaceholder(12)
            self.child_pages.adjustSize()

            # 模态弹窗
            self.modal_dialog = OptionCardPlaneForWidgetDemos(self)
            self.modal_dialog.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                               "/widgets/progress_bar/progress_bar.py")
            self.modal_dialog.setTitle("模态弹窗")
            self.modal_dialog.setFixedWidth(800)

            self.ctrl_show_modal_dialog_example = SiPushButton(self)
            self.ctrl_show_modal_dialog_example.resize(128, 32)
            self.ctrl_show_modal_dialog_example.attachment().setText("显示模态弹窗")
            self.ctrl_show_modal_dialog_example.clicked.connect(
                lambda: SiGlobal.siui.windows["MAIN_WINDOW"].layerModalDialog().setDialog(ModalDialogExample(self))
            )

            self.modal_dialog.body().addWidget(self.ctrl_show_modal_dialog_example)
            self.modal_dialog.body().addPlaceholder(12)
            self.modal_dialog.adjustSize()

            group.addWidget(self.child_pages)
            group.addWidget(self.modal_dialog)

        # 添加页脚的空白以增加美观性
        self.titled_widgets_group.addPlaceholder(64)

        # 设置控件组为页面对象
        self.setAttachment(self.titled_widgets_group)

    def set_message_box_type(self, type_):
        self.message_type = type_

    def set_message_box_auto_close(self, value):
        if isinstance(value, bool):
            self.message_auto_close = value
        if isinstance(value, str):
            try:
                self.message_auto_close_duration = int(float(value) * 1000)
            except ValueError:
                self.message_auto_close_duration = 1
