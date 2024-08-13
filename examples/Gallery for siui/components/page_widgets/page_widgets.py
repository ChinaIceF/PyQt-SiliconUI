import random

import numpy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

from siui.components import SiCircularProgressBar, SiOptionCardLinear, SiTitledWidgetGroup, SiWidget
from siui.components.combobox import SiComboBox
from siui.components.menu import SiMenu
from siui.components.page import SiPage
from siui.components.progress_bar import SiProgressBar
from siui.components.slider import SiSliderH
from siui.components.widgets import (
    SiCheckBox,
    SiDenseHContainer,
    SiDraggableLabel,
    SiFlowContainer,
    SiIconLabel,
    SiLabel,
    SiLongPressButton,
    SiMasonryContainer,
    SiPixLabel,
    SiPushButton,
    SiRadioButton,
    SiSimpleButton,
    SiSwitch,
    SiToggleButton,
)
from siui.components.widgets.navigation_bar import SiNavigationBarH
from siui.core.color import SiColor
from siui.core.globals import SiGlobal
from siui.core.silicon import Si

from ..option_card import OptionCardPlaneForWidgetDemos


class ExampleWidgets(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(64)
        self.setScrollMaximumWidth(950)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("控件")

        # 创建控件组
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setSpacing(32)
        self.titled_widgets_group.setAdjustWidgetsSize(False)  # 禁用调整宽度

        # 标签
        with self.titled_widgets_group as group:
            group.addTitle("标签")

            # 文字标签
            self.label_for_text = OptionCardPlaneForWidgetDemos(self)
            self.label_for_text.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                 "/widgets/label.py")
            self.label_for_text.setTitle("文字标签")
            self.label_for_text.setFixedWidth(800)

            self.demo_label = SiLabel(self)
            self.demo_label.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
            self.demo_label.setText("测试标签")

            self.demo_label_hinted = SiLabel(self)
            self.demo_label_hinted.setSiliconWidgetFlag(Si.AdjustSizeOnTextChanged)
            self.demo_label_hinted.setText("测试标签（具有工具提示）")
            self.demo_label_hinted.setHint("使用 setHint 方法设置工具提示")

            self.demo_label_with_svg = SiIconLabel(self)
            self.demo_label_with_svg.load(SiGlobal.siui.iconpack.get("ic_fluent_comment_link_regular"))
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
            self.pix_label.setFixedWidth(800)

            container_pix_label = SiDenseHContainer(self)
            container_pix_label.setAlignCenter(True)
            container_pix_label.setFixedHeight(80 + 24)

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
            self.label_ani.setFixedWidth(800)

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
            self.draggable_label.setFixedWidth(800)

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

            # 控件显示效果
            self.showup_effect = OptionCardPlaneForWidgetDemos(self)
            self.showup_effect.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui"
                                                  "/components/widgets/label.py")
            self.showup_effect.setTitle("控件显示效果")
            self.showup_effect.setFixedWidth(800)

            self.demo_widget = SiWidget(self)
            self.demo_widget.resize(350, 96)

            self.attachment_option_card = SiOptionCardLinear(self.demo_widget)
            self.attachment_option_card.load(SiGlobal.siui.iconpack.get("ic_fluent_card_ui_regular"))
            self.attachment_option_card.setTitle("测试选项卡",
                                                 "点击按钮，播放显示或隐藏动画")
            self.attachment_option_card.setFixedWidth(350)
            self.attachment_option_card.adjustSize()

            self.demo_widget.setCenterWidget(self.attachment_option_card)

            container_showup_effect = SiDenseHContainer(self)
            container_showup_effect.setFixedHeight(32)

            self.ctrl_show_ani_button = SiPushButton(self)
            self.ctrl_show_ani_button.attachment().setText("播放显示动画")
            self.ctrl_show_ani_button.resize(128, 32)
            self.ctrl_show_ani_button.clicked.connect(self.demo_widget.showCenterWidgetFadeIn)

            self.ctrl_hide_ani_button = SiPushButton(self)
            self.ctrl_hide_ani_button.attachment().setText("播放隐藏动画")
            self.ctrl_hide_ani_button.resize(128, 32)
            self.ctrl_hide_ani_button.clicked.connect(self.demo_widget.hideCenterWidgetFadeOut)

            container_showup_effect.addWidget(self.ctrl_show_ani_button)
            container_showup_effect.addWidget(self.ctrl_hide_ani_button)

            self.showup_effect.body().addWidget(self.demo_widget)
            self.showup_effect.body().addWidget(container_showup_effect)
            self.showup_effect.body().addPlaceholder(12)
            self.showup_effect.adjustSize()

            # <- 添加到控件组
            group.addWidget(self.label_for_text)
            group.addWidget(self.pix_label)
            group.addWidget(self.label_ani)
            group.addWidget(self.draggable_label)
            group.addWidget(self.showup_effect)

        # 按钮
        with self.titled_widgets_group as group:
            group.addTitle("按钮")

            # 按钮
            self.push_buttons = OptionCardPlaneForWidgetDemos(self)
            self.push_buttons.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                               "/widgets/button.py")
            self.push_buttons.setTitle("按压按钮")
            self.push_buttons.setFixedWidth(800)

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
            self.flat_buttons.setFixedWidth(800)

            container_flat_buttons_a = SiDenseHContainer(self)
            container_flat_buttons_a.setFixedHeight(32)

            self.demo_toggle_button_a = SiToggleButton(self)
            self.demo_toggle_button_a.resize(96, 32)
            self.demo_toggle_button_a.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_bookmark_regular"))
            self.demo_toggle_button_a.attachment().setText("收藏")
            self.demo_toggle_button_a.setHint("切换按钮，有开关两个状态可切换")
            self.demo_toggle_button_a.colorGroup().assign(SiColor.BUTTON_OFF, "#3b373f")
            self.demo_toggle_button_a.colorGroup().assign(SiColor.BUTTON_ON, "#855198")
            self.demo_toggle_button_a.colorGroup().assign(SiColor.BUTTON_HOVER, "#40855198")

            self.demo_toggle_button_b = SiToggleButton(self)
            self.demo_toggle_button_b.resize(32, 32)
            self.demo_toggle_button_b.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_bookmark_regular"))
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
            self.demo_simple_button_a.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_arrow_sync_regular"))
            self.demo_simple_button_a.attachment().setText("刷新")
            self.demo_simple_button_a.setHint("简单按钮，追求简洁清晰")

            self.demo_simple_button_b = SiSimpleButton(self)
            self.demo_simple_button_b.resize(32, 32)
            self.demo_simple_button_b.attachment().load(SiGlobal.siui.iconpack.get("ic_fluent_arrow_sync_regular"))
            self.demo_simple_button_b.setHint("刷新")

            container_flat_buttons_b.addWidget(self.demo_simple_button_a)
            container_flat_buttons_b.addWidget(self.demo_simple_button_b)

            self.flat_buttons.body().addWidget(container_flat_buttons_a)
            self.flat_buttons.body().addWidget(container_flat_buttons_b)
            self.flat_buttons.body().addPlaceholder(12)
            self.flat_buttons.adjustSize()

            # 开关
            self.switches = OptionCardPlaneForWidgetDemos(self)
            self.switches.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                           "/widgets/button.py")
            self.switches.setTitle("开关")
            self.switches.setFixedWidth(800)

            self.demo_switch = SiSwitch(self)

            self.switches.body().addWidget(self.demo_switch)
            self.switches.body().addPlaceholder(12)
            self.switches.adjustSize()

            # 单选框
            self.radio_buttons = OptionCardPlaneForWidgetDemos(self)
            self.radio_buttons.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                "/widgets/button.py")
            self.radio_buttons.setTitle("单选框")
            self.radio_buttons.setFixedWidth(800)

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
            self.checkboxes.setFixedWidth(800)

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
            group.addWidget(self.switches)
            group.addWidget(self.radio_buttons)
            group.addWidget(self.checkboxes)

        # 滑条
        with self.titled_widgets_group as group:
            group.addTitle("滑条")

            # 滑条
            self.sliders = OptionCardPlaneForWidgetDemos(self)
            self.sliders.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                          "/widgets/slider/slider.py")
            self.sliders.setTitle("滑条")
            self.sliders.setFixedWidth(800)

            self.demo_slider = SiSliderH(self)
            self.demo_slider.resize(500, 32)
            self.demo_slider.setMinimum(-20)
            self.demo_slider.setMaximum(20)
            self.demo_slider.setValue(0, move_to=False)

            self.sliders.body().addWidget(self.demo_slider)
            self.sliders.body().addPlaceholder(12)
            self.sliders.adjustSize()

            group.addWidget(self.sliders)

        # 进度条
        with self.titled_widgets_group as group:
            group.addTitle("进度条")

            # 进度条
            self.progress_bar_linear = OptionCardPlaneForWidgetDemos(self)
            self.progress_bar_linear.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                          "/widgets/progress_bar/progress_bar.py")
            self.progress_bar_linear.setTitle("进度条")
            self.progress_bar_linear.setFixedWidth(800)

            self.demo_progress_bar = SiProgressBar(self)
            self.demo_progress_bar.resize(700, 32)

            container_progress_bar_ctrl_buttons = SiDenseHContainer(self)
            container_progress_bar_ctrl_buttons.setFixedHeight(32)
            container_progress_bar_ctrl_buttons.setFixedWidth(700)

            self.ctrl_progress_bar_random_value = SiPushButton(self)
            self.ctrl_progress_bar_random_value.resize(128, 32)
            self.ctrl_progress_bar_random_value.attachment().setText("随机进度")
            self.ctrl_progress_bar_random_value.clicked.connect(lambda: self.demo_progress_bar.setValue(random.random()))  # noqa: E501

            self.ctrl_progress_bar_random_stepping = SiPushButton(self)
            self.ctrl_progress_bar_random_stepping.resize(128, 32)
            self.ctrl_progress_bar_random_stepping.attachment().setText("随机步进")
            self.ctrl_progress_bar_random_stepping.clicked.connect(lambda: self.demo_progress_bar.setValue(self.demo_progress_bar.value() + 0.1 * random.random()))  # noqa: E501

            self.ctrl_progress_bar_processing = SiPushButton(self)
            self.ctrl_progress_bar_processing.resize(64, 32)
            self.ctrl_progress_bar_processing.attachment().setText("加载")
            self.ctrl_progress_bar_processing.setHint("切换到 <strong>加载</strong> 状态")
            self.ctrl_progress_bar_processing.clicked.connect(lambda: self.demo_progress_bar.setState("processing"))  # noqa: E501

            self.ctrl_progress_bar_completing = SiPushButton(self)
            self.ctrl_progress_bar_completing.resize(64, 32)
            self.ctrl_progress_bar_completing.attachment().setText("处理")
            self.ctrl_progress_bar_completing.setHint("切换到 <strong>处理</strong> 状态")
            self.ctrl_progress_bar_completing.clicked.connect(lambda: self.demo_progress_bar.setState("completing"))  # noqa: E501

            self.ctrl_progress_bar_paused = SiPushButton(self)
            self.ctrl_progress_bar_paused.resize(64, 32)
            self.ctrl_progress_bar_paused.attachment().setText("暂停")
            self.ctrl_progress_bar_paused.setHint("切换到 <strong>暂停</strong> 状态")
            self.ctrl_progress_bar_paused.clicked.connect(lambda: self.demo_progress_bar.setState("paused"))  # noqa: E501

            container_progress_bar_ctrl_buttons.addWidget(self.ctrl_progress_bar_random_value)
            container_progress_bar_ctrl_buttons.addWidget(self.ctrl_progress_bar_random_stepping)
            container_progress_bar_ctrl_buttons.addWidget(self.ctrl_progress_bar_paused, side="right")
            container_progress_bar_ctrl_buttons.addWidget(self.ctrl_progress_bar_completing, side="right")
            container_progress_bar_ctrl_buttons.addWidget(self.ctrl_progress_bar_processing, side="right")

            self.progress_bar_linear.body().addWidget(self.demo_progress_bar)
            self.progress_bar_linear.body().addWidget(container_progress_bar_ctrl_buttons)
            self.progress_bar_linear.body().addPlaceholder(12)
            self.progress_bar_linear.adjustSize()

            # 环形进度条
            self.progress_bar_circular = OptionCardPlaneForWidgetDemos(self)
            self.progress_bar_circular.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui"
                                                        "/components/widgets/progress_bar/progress_bar.py")
            self.progress_bar_circular.setTitle("环形进度条")
            self.progress_bar_circular.setFixedWidth(800)

            self.demo_progress_bar_circular = SiCircularProgressBar(self)
            self.demo_progress_bar_circular.resize(32, 32)
            self.demo_progress_bar_circular.setValue(0.7)

            container_progress_bar_circular_ctrl_buttons = SiDenseHContainer(self)
            container_progress_bar_circular_ctrl_buttons.setFixedHeight(32)
            container_progress_bar_circular_ctrl_buttons.setFixedWidth(700)

            self.ctrl_progress_bar_circular_random_value = SiPushButton(self)
            self.ctrl_progress_bar_circular_random_value.resize(128, 32)
            self.ctrl_progress_bar_circular_random_value.attachment().setText("随机进度")
            self.ctrl_progress_bar_circular_random_value.clicked.connect(lambda: self.demo_progress_bar_circular.setValue(random.random()))  # noqa: E501

            self.ctrl_progress_bar_circular_random_stepping = SiPushButton(self)
            self.ctrl_progress_bar_circular_random_stepping.resize(128, 32)
            self.ctrl_progress_bar_circular_random_stepping.attachment().setText("随机步进")
            self.ctrl_progress_bar_circular_random_stepping.clicked.connect(lambda: self.demo_progress_bar_circular.setValue(self.demo_progress_bar_circular.value() + 0.1 * random.random()))  # noqa: E501

            container_progress_bar_circular_ctrl_buttons.addWidget(self.ctrl_progress_bar_circular_random_value)
            container_progress_bar_circular_ctrl_buttons.addWidget(self.ctrl_progress_bar_circular_random_stepping)

            self.progress_bar_circular.body().addWidget(self.demo_progress_bar_circular)
            self.progress_bar_circular.body().addWidget(container_progress_bar_circular_ctrl_buttons)
            self.progress_bar_circular.body().addPlaceholder(12)
            self.progress_bar_circular.adjustSize()

            # 环形不确定进度条
            self.progress_bar_circular_indeterminate = OptionCardPlaneForWidgetDemos(self)
            self.progress_bar_circular_indeterminate.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI"
                                                                      "/blob/main/siui/components/widgets"
                                                                      "/progress_bar/progress_bar.py")
            self.progress_bar_circular_indeterminate.setTitle("环形不确定进度条")
            self.progress_bar_circular_indeterminate.setFixedWidth(800)

            self.demo_progress_bar_circular_indeterminate = SiCircularProgressBar(self)
            self.demo_progress_bar_circular_indeterminate.resize(32, 32)
            self.demo_progress_bar_circular_indeterminate.setIndeterminate(True)

            self.progress_bar_circular_indeterminate.body().addWidget(self.demo_progress_bar_circular_indeterminate)
            self.progress_bar_circular_indeterminate.body().addPlaceholder(12)
            self.progress_bar_circular_indeterminate.adjustSize()

            group.addWidget(self.progress_bar_linear)
            group.addWidget(self.progress_bar_circular)
            group.addWidget(self.progress_bar_circular_indeterminate)

        # 菜单测试
        with self.titled_widgets_group as group:
            group.addTitle("菜单测试")

            # 进度条
            self.menus = OptionCardPlaneForWidgetDemos(self)
            self.menus.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                        "/widgets/progress_bar/progress_bar.py")
            self.menus.setTitle("菜单测试")
            self.menus.setFixedWidth(800)

            menu_child_menu_test = SiMenu()
            menu_child_menu_test.setFixedWidth(180)
            menu_child_menu_test.addOption("组", icon=SiGlobal.siui.iconpack.get("ic_fluent_folder_add_regular"))
            menu_child_menu_test.addOption("文件", icon=SiGlobal.siui.iconpack.get("ic_fluent_document_add_regular"))
            menu_child_menu_test.setShowIcon(True)
            menu_child_menu_test.setSelectionMenu(False)

            menu_test = SiMenu()
            menu_test.setFixedWidth(260)
            menu_test.addOption("具有子目录的项", icon=SiGlobal.siui.iconpack.get("ic_fluent_add_circle_regular"), child_menu=menu_child_menu_test)
            menu_test.addOption("没图标的选项")
            menu_test.addOption("从服务器同步", icon=SiGlobal.siui.iconpack.get("ic_fluent_cloud_sync_regular"))
            menu_test.addOption("共享", icon=SiGlobal.siui.iconpack.get("ic_fluent_share_regular"))
            menu_test.setSelectionMenu(False)
            menu_test.setShowIcon(True)

            self.demo_show_menu_button = SiPushButton(self)
            self.demo_show_menu_button.resize(128, 32)
            self.demo_show_menu_button.attachment().setText("显示菜单")
            self.demo_show_menu_button.clicked.connect(lambda: menu_test.unfold(QCursor.pos().x(), QCursor.pos().y()))

            self.demo_combobox = SiComboBox(self)
            self.demo_combobox.resize(256, 32)
            self.demo_combobox.addOption("Chicken you are so beautiful")
            self.demo_combobox.addOption("你干嘛嗨嗨呦~")
            self.demo_combobox.addOption("迎面走来的你让我如此蠢蠢欲动")
            self.demo_combobox.addOption("唱跳Rap篮球")
            self.demo_combobox.addOption("鸡你实在是太美")
            self.demo_combobox.addOption("我们一起学鸡叫")
            self.demo_combobox.menu().setShowIcon(False)
            self.demo_combobox.menu().setIndex(3)

            self.menus.body().addWidget(self.demo_show_menu_button)
            self.menus.body().addWidget(self.demo_combobox)
            self.menus.body().addPlaceholder(12)
            self.menus.adjustSize()

            group.addWidget(self.menus)

        # 导航栏
        with self.titled_widgets_group as group:
            group.addTitle("导航栏")

            # 侧边栏信息
            self.navigation_bar_h = OptionCardPlaneForWidgetDemos(self)
            self.navigation_bar_h.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                "/widgets/progress_bar/progress_bar.py")
            self.navigation_bar_h.setTitle("横向导航栏")
            self.navigation_bar_h.setFixedWidth(800)

            self.demo_navigation_bar_h = SiNavigationBarH(self)
            self.demo_navigation_bar_h.addItem("基本信息")
            self.demo_navigation_bar_h.addItem("排名")
            self.demo_navigation_bar_h.addItem("最近通过谱面")
            self.demo_navigation_bar_h.addItem("最佳表现")
            self.demo_navigation_bar_h.addItem("创建的谱面")
            self.demo_navigation_bar_h.setCurrentIndex(0)
            self.demo_navigation_bar_h.adjustSize()

            self.navigation_bar_h.body().addWidget(self.demo_navigation_bar_h)
            self.navigation_bar_h.body().addPlaceholder(12)
            self.navigation_bar_h.adjustSize()

            group.addWidget(self.navigation_bar_h)

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
