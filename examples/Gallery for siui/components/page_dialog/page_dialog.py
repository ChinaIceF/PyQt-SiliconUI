from PyQt5.QtCore import Qt

from siui.components import SiTitledWidgetGroup, SiPushButton, SiLabel, SiLongPressButton, SiDenseHContainer
from siui.components.combobox import SiComboBox
from siui.components.page import SiPage
from siui.core.color import SiColor
from siui.core.globals import SiGlobal
from siui.templates.application.components.dialog.modal import SiModalDialog

from ..option_card import OptionCardPlaneForWidgetDemos
from .components.child_page_example import ChildPageExample
from .components.side_msg_box import send_simple_message, send_titled_message, send_custom_message
from .components.modal_dialog_example import ModalDialogExample


class ExampleDialogs(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
            self.demo_send_message_to_sidebar.clicked.connect(lambda: send_simple_message(self.message_type))

            self.demo_send_message_to_sidebar_titled = SiPushButton(self)
            self.demo_send_message_to_sidebar_titled.resize(128, 32)
            self.demo_send_message_to_sidebar_titled.attachment().setText("具标题测试信息")
            self.demo_send_message_to_sidebar_titled.clicked.connect(lambda: send_titled_message(self.message_type))

            self.demo_send_message_to_sidebar_custom = SiPushButton(self)
            self.demo_send_message_to_sidebar_custom.resize(128, 32)
            self.demo_send_message_to_sidebar_custom.attachment().setText("发送自定义信息")
            self.demo_send_message_to_sidebar_custom.clicked.connect(lambda: send_custom_message(self.message_type))

            self.demo_type_combobox = SiComboBox(self)
            self.demo_type_combobox.resize(80, 32)
            self.demo_type_combobox.addOption("标准", value=0)
            self.demo_type_combobox.addOption("成功", value=1)
            self.demo_type_combobox.addOption("提示", value=2)
            self.demo_type_combobox.addOption("警告", value=3)
            self.demo_type_combobox.addOption("错误", value=4)
            self.demo_type_combobox.menu().setShowIcon(False)
            self.demo_type_combobox.menu().setIndex(0)
            self.demo_type_combobox.valueChanged.connect(self.set_message_box_type)

            side_message_container.addWidget(self.demo_send_message_to_sidebar)
            side_message_container.addWidget(self.demo_send_message_to_sidebar_titled)
            side_message_container.addWidget(self.demo_send_message_to_sidebar_custom)

            self.side_messages.body().addWidget(side_message_container)
            self.side_messages.body().addWidget(self.demo_type_combobox)
            self.side_messages.body().addPlaceholder(12)
            self.side_messages.adjustSize()

            group.addWidget(self.side_messages)

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
            self.ctrl_show_child_pages_example.attachment().setText("显示示例子页面")
            self.ctrl_show_child_pages_example.clicked.connect(
                lambda: SiGlobal.siui.windows["MAIN_WINDOW"].layerChildPage().setChildPage(ChildPageExample(self))
            )

            self.child_pages.body().addWidget(self.ctrl_show_child_pages_example)
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

