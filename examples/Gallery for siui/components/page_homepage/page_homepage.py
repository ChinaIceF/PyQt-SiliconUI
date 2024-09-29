
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from siui.components import SiPixLabel
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
from siui.core import GlobalFont, Si, SiColor, SiGlobal, SiQuickEffect, GlobalFontSize
from siui.gui import SiFont

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
        self.background_image = SiPixLabel(self.head_area)
        self.background_image.setFixedSize(1366, 300)
        self.background_image.setBorderRadius(6)
        self.background_image.load("./img/homepage_background.png")

        self.background_fading_transition = SiLabel(self.head_area)
        self.background_fading_transition.setGeometry(0, 100, 0, 200)
        self.background_fading_transition.setStyleSheet(
            """
            background-color: qlineargradient(x1:0, y1:1, x2:0, y2:0, stop:0 {}, stop:1 {})
            """.format(SiGlobal.siui.colors["INTERFACE_BG_B"],
                       SiColor.trans(SiGlobal.siui.colors["INTERFACE_BG_B"], 0))
        )

        # 创建大标题和副标题
        self.title = SiLabel(self.head_area)
        self.title.setGeometry(64, 0, 500, 128)
        self.title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.title.setText("Silicon UI")
        self.title.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_A"]))
        self.title.setFont(SiFont.tokenized(GlobalFont.XL_MEDIUM))

        self.subtitle = SiLabel(self.head_area)
        self.subtitle.setGeometry(64, 72, 500, 48)
        self.subtitle.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.subtitle.setText("A powerful and artistic UI library based on PyQt5")
        self.subtitle.setStyleSheet("color: {}".format(SiColor.trans(SiGlobal.siui.colors["TEXT_A"], 0.9)))
        self.subtitle.setFont(SiFont.tokenized(GlobalFont.S_MEDIUM))

        # 创建一个水平容器
        self.container_for_cards = SiDenseHContainer(self.head_area)
        self.container_for_cards.move(0, 130)
        self.container_for_cards.setFixedHeight(310)
        self.container_for_cards.setAlignment(Qt.AlignCenter)
        self.container_for_cards.setSpacing(32)

        # 添加卡片
        self.option_card_project = ThemedOptionCardPlane(self)
        self.option_card_project.setTitle("GitHub Repo")
        self.option_card_project.setFixedSize(218, 270)
        self.option_card_project.setThemeColor("#855198")
        self.option_card_project.setDescription(
            "check PyQt-SiliconUI Repository on GitHub to get the latest release, report errors, provide suggestions and more.")  # noqa: E501
        self.option_card_project.setURL("https://github.com/ChinaIceF/PyQt-SiliconUI")

        self.option_card_example = ThemedOptionCardPlane(self)
        self.option_card_example.setTitle("Examples")
        self.option_card_example.setFixedSize(218, 270)
        self.option_card_example.setThemeColor("#7573aa")
        self.option_card_example.setDescription("Check examples to understand how to use PyQt-SiliconUI to develop your first work.")  # noqa: E501
        self.option_card_example.setURL("Examples are Coming soon...")

        # 添加到水平容器
        self.container_for_cards.addPlaceholder(64 - 32)
        self.container_for_cards.addWidget(self.option_card_project)
        self.container_for_cards.addWidget(self.option_card_example)

        # 添加到滚动区域容器
        self.scroll_container.addWidget(self.head_area)

        # SiQuickEffect.applyDropShadowOn(self.container_for_cards, color=(0, 0, 0, 80), blur_radius=48)

        # 下方区域标签
        self.body_area = SiLabel(self)
        self.body_area.setSiliconWidgetFlag(Si.EnableAnimationSignals)
        self.body_area.resized.connect(lambda _: self.scroll_container.adjustSize())

        # 下面的 titledWidgetGroups
        self.titled_widget_group = SiTitledWidgetGroup(self.body_area)
        self.titled_widget_group.setSiliconWidgetFlag(Si.EnableAnimationSignals)
        self.titled_widget_group.resized.connect(lambda size: self.body_area.setFixedHeight(size[1]))
        self.titled_widget_group.move(64, 0)

        # 开始搭建界面
        # 控件的线性选项卡

        self.titled_widget_group.setSpacing(16)
        self.titled_widget_group.addTitle("Widgets")
        self.titled_widget_group.addWidget(WidgetsExamplePanel(self))

        self.titled_widget_group.addTitle("Option Cards")
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
        self.button_bug.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_bug_regular"))
        self.button_bug.resize(32, 32)
        self.button_bug.setHint("Report bugs")

        self.button_source_code = SiSimpleButton(self)
        self.button_source_code.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_open_regular"))
        self.button_source_code.resize(32, 32)
        self.button_source_code.setHint("Source code")

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
        self.option_card_button.setTitle("Push Button")

        option_card_button_container_h = SiDenseHContainer(self)
        option_card_button_container_h.setFixedHeight(32)

        button_a = SiPushButton(self)
        button_a.resize(128, 32)
        button_a.attachment().setText("Push Button")

        button_b = SiPushButton(self)
        button_b.resize(128, 32)
        button_b.setUseTransition(True)
        button_b.attachment().setText("Themed")

        button_c = SiLongPressButton(self)
        button_c.resize(128, 32)
        button_c.attachment().setText("Hold-to-Confirm")

        option_card_button_container_h.addWidget(button_a)
        option_card_button_container_h.addWidget(button_b)
        option_card_button_container_h.addWidget(button_c)

        self.option_card_button.body().addWidget(option_card_button_container_h)

        # 开关
        option_card_switch = WidgetsExampleOptionCardPlane(self)
        option_card_switch.setTitle("Switch")
        option_card_switch.setFixedWidth(300)

        option_card_switch_container_h = SiDenseHContainer(self)
        option_card_switch_container_h.setFixedHeight(40)
        option_card_switch_container_h.setAlignment(Qt.AlignCenter)

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
        self.option_card_edit.setTitle("Line Edit")
        self.option_card_edit.setFixedWidth(300)

        line_edit = SiLineEdit(self)
        line_edit.setFixedSize(252, 32)

        self.option_card_edit.body().addWidget(line_edit)

        # 滑条
        self.option_card_slider = WidgetsExampleOptionCardPlane(self)
        self.option_card_slider.setTitle("Slider")
        self.option_card_slider.setFixedWidth(300)

        slider = SiSliderH(self)
        slider.setFixedHeight(32)
        slider.setMinimum(-20)
        slider.setMaximum(20)

        self.option_card_slider.body().setAdjustWidgetsSize(True)
        self.option_card_slider.body().addWidget(slider)

        # 添加到第二个水平容器
        container_h_b.addWidget(self.option_card_edit)
        container_h_b.addWidget(self.option_card_slider)

        # 解释按钮
        button_description = SiSimpleButton(self)
        button_description.attachment().setText("See More")
        button_description.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_apps_add_in_regular"))
        button_description.colorGroup().assign(SiColor.BUTTON_OFF, "#2C2930")
        button_description.reloadStyleSheet()
        button_description.resize(210, 32)

        # 查看更多容器
        container_v_button = SiDenseVContainer(self)
        container_v_button.setAlignment(Qt.AlignCenter)
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
        attached_button_a.attachment().setText("Attachment")

        attached_button_b = SiPushButton(self)
        attached_button_b.resize(32, 32)
        attached_button_b.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_attach_regular"))

        self.option_card_linear_attaching = SiOptionCardLinear(self)
        self.option_card_linear_attaching.setTitle("Attach Widgets", "The linear option card provides a horizontal container where any control can be added,\nwith no limit on the number")
        self.option_card_linear_attaching.load(SiGlobal.siui.iconpack.get("ic_fluent_attach_regular"))
        self.option_card_linear_attaching.addWidget(attached_button_a)
        self.option_card_linear_attaching.addWidget(attached_button_b)

        # <- ADD
        self.addWidget(self.option_card_linear_attaching)

        # 平面选项卡
        header_button = SiSimpleButton(self)
        header_button.setFixedHeight(32)
        header_button.attachment().setText("Header Attachment")
        header_button.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_window_header_horizontal_regular"))
        header_button.adjustSize()

        body_label = SiLabel(self)
        body_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
        body_label.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_B"]))
        body_label.setText("SiOptionCardPlane provides three containers: header, body, and footer."
                           "\nHeader and Footer are SiDenseHContainer, while body is a SiDenseVContainer."
                           "\nHere is the body container, where you can realize your interface function. Enjoy it!")

        footer_button_a = SiSimpleButton(self)
        footer_button_a.resize(32, 32)
        footer_button_a.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_pen_regular"))
        footer_button_a.setHint("Draw")

        footer_button_b = SiSimpleButton(self)
        footer_button_b.resize(32, 32)
        footer_button_b.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_eyedropper_regular"))
        footer_button_b.setHint("Eyedropper")

        footer_button_c = SiSimpleButton(self)
        footer_button_c.resize(32, 32)
        footer_button_c.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_save_regular"))
        footer_button_c.setHint("Save")

        self.option_card_plane_beginning = SiOptionCardPlane(self)
        self.option_card_plane_beginning.setTitle("Plane Option Card")
        self.option_card_plane_beginning.header().addWidget(header_button, side="right")
        self.option_card_plane_beginning.body().addWidget(body_label, side="top")
        self.option_card_plane_beginning.footer().setFixedHeight(64)
        self.option_card_plane_beginning.footer().setSpacing(8)
        self.option_card_plane_beginning.footer().setAlignment(Qt.AlignCenter)
        self.option_card_plane_beginning.footer().addWidget(footer_button_a, side="left")
        self.option_card_plane_beginning.footer().addWidget(footer_button_b, side="left")
        self.option_card_plane_beginning.footer().addWidget(footer_button_c, side="left")
        self.option_card_plane_beginning.adjustSize()

        # <- ADD
        self.addWidget(self.option_card_plane_beginning)

        # 解释按钮
        button_description = SiSimpleButton(self)
        button_description.attachment().setText("See More")
        button_description.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_apps_add_in_regular"))
        button_description.colorGroup().assign(SiColor.BUTTON_OFF, "#2C2930")
        button_description.colorGroup().assign(SiColor.BUTTON_ON, "#2C2930")
        button_description.reloadStyleSheet()
        button_description.resize(210, 32)

        # 查看更多容器
        container_v_button = SiDenseVContainer(self)
        container_v_button.setAlignment(Qt.AlignCenter)
        container_v_button.addWidget(button_description)

        self.addWidget(container_v_button)
