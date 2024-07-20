import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect

sys.path.append(str(Path().cwd()))
from siui.components.option_card import SiOptionCardLinear, SiOptionCardPlane
from siui.components.page import SiPage
from siui.components.slider import SiSliderH
from siui.components.titled_widget_group import SiTitledWidgetGroup
from siui.components.widgets import (
    SiDenseHContainer,
    SiDenseVContainer,
    SiLabel,
    SiLineEdit,
    SiLongPressButton,
    SiPushButton,
    SiSimpleButton,
    SiSwitch,
)

from siui.core.color import Color
from siui.core.globals import SiGlobal

from .components.themed_option_card import ThemedOptionCardPlane


class ExampleHomepage(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 滚动区域
        self.scroll_container = SiTitledWidgetGroup(self)

        # 整个顶部
        self.head_area = SiLabel(self)
        self.head_area.setFixedHeight(450)

        # 创建背景底图和渐变
        self.background_image = SiLabel(self.head_area)
        self.background_image.setFixedHeight(300)
        self.background_image.setObjectName("bg_image")
        self.background_image.setStyleSheet(
            """
            #bg_image {
                background-image: url('./examples/template_test/img/homepage_background.png');
                border-top-left-radius:6px
            }"""
        )

        self.background_fading_transition = SiLabel(self.head_area)
        self.background_fading_transition.setGeometry(0, 100, 0, 200)
        self.background_fading_transition.setStyleSheet(
            """
            background-color: qlineargradient(x1:0, y1:1, x2:0, y2:0, stop:0 {}, stop:1 {})
            """.format(
                SiGlobal.siui.colors["INTERFACE_BG_B"], Color.transparency(SiGlobal.siui.colors["INTERFACE_BG_B"], 0)
            )
        )

        # 创建大标题和副标题
        self.title = SiLabel(self.head_area)
        self.title.setGeometry(64, 0, 500, 128)
        self.title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.title.setText("Silicon UI")
        self.title.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_A"]))
        self.title.setFont(SiGlobal.siui.fonts["XL_NORMAL"])

        self.subtitle = SiLabel(self.head_area)
        self.subtitle.setGeometry(64, 72, 500, 48)
        self.subtitle.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.subtitle.setText("基于 PySide6 的 UI 框架，灵动、优雅而轻便")
        self.subtitle.setStyleSheet("color: {}".format(Color.transparency(SiGlobal.siui.colors["TEXT_A"], 0.9)))
        self.subtitle.setFont(SiGlobal.siui.fonts["S_BOLD"])

        # 创建一个水平容器
        self.container_for_cards = SiDenseHContainer(self.head_area)
        self.container_for_cards.move(0, 130)
        self.container_for_cards.setFixedHeight(310)
        self.container_for_cards.setAlignCenter(True)
        self.container_for_cards.setSpacing(32)

        # 添加卡片
        self.option_card_project = ThemedOptionCardPlane(self)
        self.option_card_project.setTitle("项目主页")
        self.option_card_project.setFixedSize(218, 270)
        self.option_card_project.setThemeColor("#855198")
        self.option_card_project.setDescription(
            "访问 GitHub 项目主页，以获取最新版本，报告错误，建言献策，参与开发，查询文档和须知，寻求他人答疑解惑</strong>"
        )
        self.option_card_project.setURL("https://github.com/ChinaIceF/PyQt-SiliconUI")

        self.option_card_example = ThemedOptionCardPlane(self)
        self.option_card_example.setTitle("应用示例")
        self.option_card_example.setFixedSize(218, 270)
        self.option_card_example.setThemeColor("#7573aa")
        self.option_card_example.setDescription("学习并快速上手，了解如何使用 SiliconUI 开发你的第一件作品")
        self.option_card_example.setURL("https://github.com/ChinaIceF/PyQt-SiliconUI")

        # 添加到水平容器
        self.container_for_cards.addPlaceholder(64 - 32)
        self.container_for_cards.addWidget(self.option_card_project)
        self.container_for_cards.addWidget(self.option_card_example)

        # 添加到滚动区域容器
        self.scroll_container.addWidget(self.head_area)

        # 创建QGraphicsDropShadowEffect对象，为水平容器创造阴影
        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 0)
        shadow.setBlurRadius(48)
        self.container_for_cards.setGraphicsEffect(shadow)

        # 下方区域标签
        self.body_area = SiLabel(self)
        self.body_area.setUseSignals(True)
        self.body_area.resized.connect(lambda _: self.scroll_container.adjustSize())

        # 下面的 titledWidgetGroups
        self.titled_widget_group = SiTitledWidgetGroup(self.body_area)
        self.titled_widget_group.setUseSignals(True)
        self.titled_widget_group.resized.connect(lambda size: self.body_area.setFixedHeight(size[1]))
        self.titled_widget_group.move(64, 0)

        # 开始搭建界面
        # 控件的线性选项卡

        self.titled_widget_group.setSpacing(16)
        self.titled_widget_group.addTitle("控件")
        self.titled_widget_group.addWidget(WidgetsExamplePanel(self))

        self.titled_widget_group.addTitle("选项卡")
        self.titled_widget_group.addWidget(OptionCardsExamplePanel(self))

        self.titled_widget_group.addPlaceholder(64)

        # 添加到滚动区域容器
        self.body_area.setFixedHeight(self.titled_widget_group.height())
        self.scroll_container.addWidget(self.body_area)

        # 添加到页面
        self.setAttachment(self.scroll_container)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = event.size().width()
        self.body_area.setFixedWidth(w)
        self.background_image.setFixedWidth(w)
        self.titled_widget_group.setFixedWidth(min(w - 128, 900))
        self.background_fading_transition.setFixedWidth(w)


class WidgetsExampleOptionCardPlane(SiOptionCardPlane):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.button_bug = SiSimpleButton(self)
        self.button_bug.attachment().load(SiGlobal.siui.icons["fi-rr-bug"])
        self.button_bug.resize(32, 32)
        self.button_bug.setHint("报告问题")

        self.button_source_code = SiSimpleButton(self)
        self.button_source_code.attachment().load(SiGlobal.siui.icons["fi-rr-link"])
        self.button_source_code.resize(32, 32)
        self.button_source_code.setHint("查看源代码")

        self.header().addWidget(self.button_source_code, "right")
        self.header().addWidget(self.button_bug, "right")


class WidgetsExamplePanel(SiDenseVContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setAdjustWidgetsSize(True)
        self.setSpacing(12)

        # 第一个水平容器
        container_h_a = SiDenseHContainer(self)
        container_h_a.setFixedHeight(128)
        container_h_a.setAdjustWidgetsSize(True)

        # 上面的两个选项卡，按钮和开关
        # 按钮
        self.option_card_button = WidgetsExampleOptionCardPlane(self)
        self.option_card_button.setTitle("按钮")

        option_card_button_container_h = SiDenseHContainer(self)
        option_card_button_container_h.setFixedHeight(32)

        button_a = SiPushButton(self)
        button_a.resize(128, 32)
        button_a.attachment().setText("普通按钮")

        button_b = SiPushButton(self)
        button_b.resize(128, 32)
        button_b.setThemed(True)
        button_b.attachment().setText("主题按钮")

        button_c = SiLongPressButton(self)
        button_c.resize(128, 32)
        button_c.attachment().setText("长按按钮")

        option_card_button_container_h.addWidget(button_a)
        option_card_button_container_h.addWidget(button_b)
        option_card_button_container_h.addWidget(button_c)

        self.option_card_button.body().addWidget(option_card_button_container_h)

        # 开关
        option_card_switch = WidgetsExampleOptionCardPlane(self)
        option_card_switch.setTitle("开关")
        option_card_switch.setFixedWidth(300)

        option_card_switch_container_h = SiDenseHContainer(self)
        option_card_switch_container_h.setFixedHeight(40)
        option_card_switch_container_h.setAlignCenter(True)

        switch = SiSwitch(self)
        switch.setFixedHeight(32)

        option_card_switch_container_h.addWidget(switch)

        option_card_switch.body().addWidget(option_card_switch_container_h)

        # 添加到第一个水平容器
        container_h_a.addWidget(self.option_card_button)
        container_h_a.addWidget(option_card_switch, "right")

        # 第二个水平容器
        container_h_b = SiDenseHContainer(self)
        container_h_b.setFixedHeight(128)
        container_h_b.setAdjustWidgetsSize(True)

        # 下面的两个选项卡，输入框和滑动条
        # 输入框
        self.option_card_edit = WidgetsExampleOptionCardPlane(self)
        self.option_card_edit.setTitle("输入框")
        self.option_card_edit.setFixedWidth(300)

        line_edit = SiLineEdit(self)
        line_edit.setFixedSize(252, 32)

        self.option_card_edit.body().addWidget(line_edit)

        # 滑条
        self.option_card_slider = WidgetsExampleOptionCardPlane(self)
        self.option_card_slider.setTitle("输入框")
        self.option_card_slider.setFixedWidth(300)

        slider = SiSliderH(self)
        slider.setFixedHeight(32)

        self.option_card_slider.body().setAdjustWidgetsSize(True)
        self.option_card_slider.body().addWidget(slider)

        # 添加到第二个水平容器
        container_h_b.addWidget(self.option_card_edit)
        container_h_b.addWidget(self.option_card_slider)

        # 解释按钮
        button_description = SiSimpleButton(self)
        button_description.attachment().setText("查看更多")
        button_description.attachment().load(SiGlobal.siui.icons["fi-rr-apps-add"])
        button_description.setColor("#2C2930")
        button_description.resize(210, 32)

        # 查看更多容器
        container_v_button = SiDenseVContainer(self)
        container_v_button.setAlignCenter(True)
        container_v_button.addWidget(button_description)

        # 添加两个水平容器到自己
        self.addWidget(container_h_a)
        self.addWidget(container_h_b)
        self.addWidget(container_v_button)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.option_card_button.setFixedWidth(event.size().width() - 300 - 16)
        self.option_card_slider.setFixedWidth(event.size().width() - 300 - 16)


class OptionCardsExamplePanel(SiDenseVContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setAdjustWidgetsSize(True)
        self.setSpacing(12)

        # 线性选项卡
        attached_button_a = SiPushButton(self)
        attached_button_a.resize(128, 32)
        attached_button_a.attachment().setText("绑定按钮")

        attached_button_b = SiPushButton(self)
        attached_button_b.resize(32, 32)
        attached_button_b.attachment().load(SiGlobal.siui.icons["fi-rr-portrait"])

        self.option_card_linear_attaching = SiOptionCardLinear(self)
        self.option_card_linear_attaching.setTitle("绑定控件", "线性选项卡提供水平容器，可以添加任意控件，不限数量")
        self.option_card_linear_attaching.load(SiGlobal.siui.icons["fi-rr-sign-in"])
        self.option_card_linear_attaching.addWidget(attached_button_a)
        self.option_card_linear_attaching.addWidget(attached_button_b)

        # <- ADD
        self.addWidget(self.option_card_linear_attaching)

        # 平面选项卡
        header_button = SiSimpleButton(self)
        header_button.setFixedHeight(32)
        header_button.attachment().setText("Header 区域")
        header_button.attachment().load(SiGlobal.siui.icons["fi-rr-portrait"])
        header_button.adjustSize()

        body_label = SiLabel(self)
        body_label.setAutoAdjustSize(True)
        body_label.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_B"]))
        body_label.setText(
            "平面选项卡提供了三个容器：header，body，footer，每个容器都可以独立访问\n其中 header 和 footer 是水平容器，body 是垂直容器\n这个容器是平面选项卡的 body，在这里尽情添加控件吧！"
        )

        footer_button_a = SiSimpleButton(self)
        footer_button_a.resize(32, 32)
        footer_button_a.attachment().load(SiGlobal.siui.icons["fi-rr-pencil"])
        footer_button_a.setHint("绘制")

        footer_button_b = SiSimpleButton(self)
        footer_button_b.resize(32, 32)
        footer_button_b.attachment().load(SiGlobal.siui.icons["fi-rr-eye-dropper"])
        footer_button_b.setHint("取色器")

        footer_button_c = SiSimpleButton(self)
        footer_button_c.resize(32, 32)
        footer_button_c.attachment().load(SiGlobal.siui.icons["fi-rr-disk"])
        footer_button_c.setHint("保存")

        self.option_card_plane_beginning = SiOptionCardPlane(self)
        self.option_card_plane_beginning.setTitle("平面选项卡")
        self.option_card_plane_beginning.header().addWidget(header_button, side="right")
        self.option_card_plane_beginning.body().addWidget(body_label, side="top")
        self.option_card_plane_beginning.footer().setFixedHeight(64)
        self.option_card_plane_beginning.footer().setSpacing(8)
        self.option_card_plane_beginning.footer().setAlignCenter(True)
        self.option_card_plane_beginning.footer().addWidget(footer_button_a, side="left")
        self.option_card_plane_beginning.footer().addWidget(footer_button_b, side="left")
        self.option_card_plane_beginning.footer().addWidget(footer_button_c, side="left")
        self.option_card_plane_beginning.adjustSize()

        # <- ADD
        self.addWidget(self.option_card_plane_beginning)

        # 解释按钮
        button_description = SiSimpleButton(self)
        button_description.attachment().setText("查看更多")
        button_description.attachment().load(SiGlobal.siui.icons["fi-rr-apps-add"])
        button_description.setColor("#2C2930")
        button_description.resize(210, 32)

        # 查看更多容器
        container_v_button = SiDenseVContainer(self)
        container_v_button.setAlignCenter(True)
        container_v_button.addWidget(button_description)

        self.addWidget(container_v_button)
