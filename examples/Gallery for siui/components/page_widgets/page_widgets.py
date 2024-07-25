import time

import numpy
from PyQt5.QtCore import Qt

from siui.components import SiTitledWidgetGroup
from siui.components.page import SiPage
from siui.components.widgets import (
    SiDenseHContainer,
    SiDraggableLabel,
    SiIconLabel,
    SiLabel,
    SiLongPressButton,
    SiPixLabel,
    SiPushButton,
    SiRadioButton,
    SiCheckBox,
    SiToggleButton,
    SiSimpleButton,
)
from siui.core.globals import SiGlobal
from siui.core.silicon import Si
from siui.core.color import SiColor

from .option_card import OptionCardPlaneForWidgetDemos


class ExampleWidgets(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(64)
        self.setScrollMaximumWidth(950)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("控件")

        # 创建控件组
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setAdjustWidgetsSize(False)  # 禁用调整宽度

        # 标签
        with self.titled_widgets_group as group:
            group.addTitle("标签")

            # 文字标签
            self.label_for_text = OptionCardPlaneForWidgetDemos(self)
            self.label_for_text.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                 "/widgets/label.py")
            self.label_for_text.setTitle("文字标签")
            self.label_for_text.setFixedWidth(580)

            self.demo_label = SiLabel(self)
            self.demo_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
            self.demo_label.setText("测试标签")

            self.demo_label_hinted = SiLabel(self)
            self.demo_label_hinted.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
            self.demo_label_hinted.setText("测试标签（具有工具提示）")
            self.demo_label_hinted.setHint("使用 setHint 方法设置工具提示")

            self.demo_label_with_svg = SiIconLabel(self)
            self.demo_label_with_svg.load(SiGlobal.siui.icons["fi-rr-comment"])
            self.demo_label_with_svg.setText(" 具有 SVG 图标的标签")

            self.label_for_text.body().addWidget(self.demo_label)
            self.label_for_text.body().addWidget(self.demo_label_hinted)
            self.label_for_text.body().addWidget(self.demo_label_with_svg)
            self.label_for_text.body().addPlaceholder(12)
            self.label_for_text.adjustSize()

            # 图片标签
            self.pix_label = OptionCardPlaneForWidgetDemos(self)
            self.pix_label.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                            "/widgets/label.py")
            self.pix_label.setTitle("图片标签")
            self.pix_label.setFixedWidth(580)

            container_pix_label = SiDenseHContainer(self)
            container_pix_label.setFixedHeight(80)

            self.demo_pix_label_a = SiPixLabel(self)
            self.demo_pix_label_a.setFixedSize(80, 80)
            self.demo_pix_label_a.setBorderRadius(40)
            self.demo_pix_label_a.load("./img/avatar1.png")
            self.demo_pix_label_a.setHint("<strong>尺寸：</strong> 80px * 80px<br>"
                                          "<strong>圆角半径：</strong> 40px")

            self.demo_pix_label_b = SiPixLabel(self)
            self.demo_pix_label_b.setFixedSize(80, 80)
            self.demo_pix_label_b.setBorderRadius(32)
            self.demo_pix_label_b.load("./img/avatar1.png")
            self.demo_pix_label_b.setHint("<strong>尺寸：</strong> 80px * 80px<br>"
                                          "<strong>圆角半径：</strong> 32px")

            container_pix_label.addWidget(self.demo_pix_label_a)
            container_pix_label.addWidget(self.demo_pix_label_b)

            self.pix_label.body().addWidget(container_pix_label)
            self.pix_label.body().addPlaceholder(12)
            self.pix_label.adjustSize()

            # 标签动画
            self.label_ani = OptionCardPlaneForWidgetDemos(self)
            self.label_ani.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                            "/widgets/label.py")
            self.label_ani.setTitle("标签动画")
            self.label_ani.setAdditionalDescription("特性")
            self.label_ani.setFixedWidth(580)

            self.demo_move_area = SiLabel(self)
            self.demo_move_area.setFixedSize(526, 80)

            self.demo_label_ani = SiLabel(self.demo_move_area)
            self.demo_label_ani.setFixedStyleSheet("border-radius: 4px")
            self.demo_label_ani.resize(128, 32)
            self.demo_label_ani.setMoveLimits(0, 0, 526, 80)
            self.demo_label_ani.setHint("标签的 moveTo, resizeTo 等内置动画方法提供灵动的动画")

            container_label_ani_for_buttons = SiDenseHContainer(self)
            container_label_ani_for_buttons.setFixedHeight(32)

            self.ctrl_button_random_pos_for_label_ani = SiPushButton(self)
            self.ctrl_button_random_pos_for_label_ani.attachment().setText("随机位置")
            self.ctrl_button_random_pos_for_label_ani.resize(128, 32)
            self.ctrl_button_random_pos_for_label_ani.clicked.connect(
                lambda: self.demo_label_ani.moveTo(numpy.random.randint(0, 526), numpy.random.randint(0, 80)))

            self.ctrl_button_random_size_for_label_ani = SiPushButton(self)
            self.ctrl_button_random_size_for_label_ani.attachment().setText("随机尺寸")
            self.ctrl_button_random_size_for_label_ani.resize(128, 32)
            self.ctrl_button_random_size_for_label_ani.clicked.connect(
                lambda: self.demo_label_ani.resizeTo(numpy.random.randint(32, 256), numpy.random.randint(16, 64)))

            self.ctrl_button_reset_for_label_ani = SiPushButton(self)
            self.ctrl_button_reset_for_label_ani.attachment().setText("还原初始状态")
            self.ctrl_button_reset_for_label_ani.resize(128, 32)
            self.ctrl_button_reset_for_label_ani.clicked.connect(lambda: self.demo_label_ani.moveTo(0, 0))
            self.ctrl_button_reset_for_label_ani.clicked.connect(lambda: self.demo_label_ani.resizeTo(128, 32))

            container_label_ani_for_buttons.addWidget(self.ctrl_button_random_pos_for_label_ani)
            container_label_ani_for_buttons.addWidget(self.ctrl_button_random_size_for_label_ani)
            container_label_ani_for_buttons.addWidget(self.ctrl_button_reset_for_label_ani)

            self.label_ani.body().addWidget(self.demo_move_area)
            self.label_ani.body().addWidget(container_label_ani_for_buttons)
            self.label_ani.body().addPlaceholder(12)
            self.label_ani.adjustSize()

            # 可拖动标签
            self.draggable_label = OptionCardPlaneForWidgetDemos(self)
            self.draggable_label.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui"
                                                  "/components/widgets/label.py")
            self.draggable_label.setTitle("可拖动标签")
            self.draggable_label.setFixedWidth(580)

            self.demo_drag_area = SiLabel(self)
            self.demo_drag_area.setFixedSize(526, 80)

            self.demo_draggable_label = SiDraggableLabel(self.demo_drag_area)
            self.demo_draggable_label.setFixedStyleSheet("border-radius: 4px")
            self.demo_draggable_label.setMoveLimits(0, 0, 526, 80)
            self.demo_draggable_label.resize(128, 32)
            self.demo_draggable_label.setHint("使用 setMoveLimits 方法限制移动范围"
                                              "\n移动动画（可禁用）提供更平滑的移动效果")

            self.draggable_label.body().addWidget(self.demo_drag_area)
            self.draggable_label.body().addPlaceholder(12)
            self.draggable_label.adjustSize()

            # <- 添加到控件组
            group.addWidget(self.label_for_text)
            group.addWidget(self.pix_label)
            group.addWidget(self.label_ani)
            group.addWidget(self.draggable_label)

        # 按钮
        with self.titled_widgets_group as group:
            group.addTitle("按钮")

            # 按钮
            self.push_buttons = OptionCardPlaneForWidgetDemos(self)
            self.push_buttons.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                               "/widgets/button.py")
            self.push_buttons.setTitle("按压按钮")
            self.push_buttons.setFixedWidth(580)

            container_push_buttons = SiDenseHContainer(self)
            container_push_buttons.setFixedHeight(32)

            self.demo_push_button_normal = SiPushButton(self)
            self.demo_push_button_normal.resize(128, 32)
            self.demo_push_button_normal.attachment().setText("普通按钮")

            self.demo_push_button_transition = SiPushButton(self)
            self.demo_push_button_transition.resize(128, 32)
            self.demo_push_button_transition.setUseTransition(True)
            self.demo_push_button_transition.attachment().setText("主题按钮")

            self.demo_push_button_long_press = SiLongPressButton(self)
            self.demo_push_button_long_press.resize(128, 32)
            self.demo_push_button_long_press.attachment().setText("长按按钮")

            container_push_buttons.addWidget(self.demo_push_button_normal)
            container_push_buttons.addWidget(self.demo_push_button_transition)
            container_push_buttons.addWidget(self.demo_push_button_long_press)

            self.push_buttons.body().addWidget(container_push_buttons)
            self.push_buttons.body().addPlaceholder(12)
            self.push_buttons.adjustSize()

            # 扁平类按钮
            self.flat_buttons = OptionCardPlaneForWidgetDemos(self)
            self.flat_buttons.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                             "/widgets/button.py")
            self.flat_buttons.setTitle("扁平类按钮")
            self.flat_buttons.setFixedWidth(580)

            container_flat_buttons_a = SiDenseHContainer(self)
            container_flat_buttons_a.setFixedHeight(32)

            self.demo_toggle_button_a = SiToggleButton(self)
            self.demo_toggle_button_a.resize(96, 32)
            self.demo_toggle_button_a.attachment().load(SiGlobal.siui.icons["fi-rr-bookmark"])
            self.demo_toggle_button_a.attachment().setText("收藏")
            self.demo_toggle_button_a.setHint("切换按钮，有开关两个状态可切换")
            self.demo_toggle_button_a.colorGroup().assign(SiColor.BUTTON_OFF, "#3b373f")
            self.demo_toggle_button_a.colorGroup().assign(SiColor.BUTTON_ON, "#855198")
            self.demo_toggle_button_a.colorGroup().assign(SiColor.BUTTON_HOVER, "#40855198")

            self.demo_toggle_button_b = SiToggleButton(self)
            self.demo_toggle_button_b.resize(32, 32)
            self.demo_toggle_button_b.attachment().load(SiGlobal.siui.icons["fi-rr-bookmark"])
            self.demo_toggle_button_b.setHint("收藏")
            self.demo_toggle_button_b.colorGroup().assign(SiColor.BUTTON_OFF, "#3b373f")
            self.demo_toggle_button_b.colorGroup().assign(SiColor.BUTTON_ON, "#855198")
            self.demo_toggle_button_b.colorGroup().assign(SiColor.BUTTON_HOVER, "#40855198")

            container_flat_buttons_a.addWidget(self.demo_toggle_button_a)
            container_flat_buttons_a.addWidget(self.demo_toggle_button_b)

            container_flat_buttons_b = SiDenseHContainer(self)
            container_flat_buttons_b.setFixedHeight(32)

            self.demo_simple_button_a = SiSimpleButton(self)
            self.demo_simple_button_a.resize(96, 32)
            self.demo_simple_button_a.attachment().load(SiGlobal.siui.icons["fi-rr-refresh"])
            self.demo_simple_button_a.attachment().setText("刷新")
            self.demo_simple_button_a.setHint("简单按钮，追求简洁清晰")

            self.demo_simple_button_b = SiSimpleButton(self)
            self.demo_simple_button_b.resize(32, 32)
            self.demo_simple_button_b.attachment().load(SiGlobal.siui.icons["fi-rr-refresh"])
            self.demo_simple_button_b.setHint("刷新")

            container_flat_buttons_b.addWidget(self.demo_simple_button_a)
            container_flat_buttons_b.addWidget(self.demo_simple_button_b)

            self.flat_buttons.body().addWidget(container_flat_buttons_a)
            self.flat_buttons.body().addWidget(container_flat_buttons_b)
            self.flat_buttons.body().addPlaceholder(12)
            self.flat_buttons.adjustSize()

            # 单选框
            self.radio_buttons = OptionCardPlaneForWidgetDemos(self)
            self.radio_buttons.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                               "/widgets/button.py")
            self.radio_buttons.setTitle("单选框")
            self.radio_buttons.setFixedWidth(580)

            self.demo_radio_button_a = SiRadioButton(self)
            self.demo_radio_button_a.setText("西红柿炒鸡蛋")

            self.demo_radio_button_b = SiRadioButton(self)
            self.demo_radio_button_b.setText("水煮肉片")

            self.demo_radio_button_c = SiRadioButton(self)
            self.demo_radio_button_c.setText("秘制小汉堡")

            self.radio_buttons.body().addWidget(self.demo_radio_button_a)
            self.radio_buttons.body().addWidget(self.demo_radio_button_b)
            self.radio_buttons.body().addWidget(self.demo_radio_button_c)
            self.radio_buttons.body().addPlaceholder(12)
            self.radio_buttons.adjustSize()

            # 多选框
            self.checkboxes = OptionCardPlaneForWidgetDemos(self)
            self.checkboxes.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                             "/widgets/button.py")
            self.checkboxes.setTitle("多选框")
            self.checkboxes.setFixedWidth(580)

            self.demo_checkbox_a = SiCheckBox(self)
            self.demo_checkbox_a.setText("安装基本组件")

            self.demo_checkbox_b = SiCheckBox(self)
            self.demo_checkbox_b.setText("安装高级组件")

            self.checkboxes.body().addWidget(self.demo_checkbox_a)
            self.checkboxes.body().addWidget(self.demo_checkbox_b)
            self.checkboxes.body().addPlaceholder(12)
            self.checkboxes.adjustSize()

            group.addWidget(self.push_buttons)
            group.addWidget(self.flat_buttons)
            group.addWidget(self.radio_buttons)
            group.addWidget(self.checkboxes)

        # 添加页脚的空白以增加美观性
        self.titled_widgets_group.addPlaceholder(64)

        # 设置控件组为页面对象
        self.setAttachment(self.titled_widgets_group)

    def reloadStyleSheet(self):
        super().reloadStyleSheet()

        # 标签
        # 文字标签
        self.demo_label.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_A"]))
        self.demo_label_hinted.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_A"]))
        self.demo_label_with_svg.setStyleSheet("color: {}".format(SiGlobal.siui.colors["TEXT_A"]))
        # 标签动画
        self.demo_label_ani.setColorTo(SiGlobal.siui.colors["INTERFACE_BG_E"])
        # 可拖动标签
        self.demo_draggable_label.setColorTo(SiGlobal.siui.colors["INTERFACE_BG_E"])
