import datetime
import random

import numpy
from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QGraphicsBlurEffect, QLabel

from siui.components import (
    SiCircularProgressBar,
    SiDenseVContainer,
    SiLineEditWithDeletionButton,
    SiLineEditWithItemName,
    SiOptionCardLinear,
    SiTitledWidgetGroup,
    SiWidget,
)
from siui.components.button import (
    SiFlatButton,
    SiLongPressButtonRefactor,
    SiProgressPushButton,
    SiPushButtonRefactor,
    SiRadioButtonRefactor,
    SiRadioButtonWithAvatar,
    SiRadioButtonWithDescription,
    SiSwitchRefactor,
    SiToggleButtonRefactor,
)
from siui.components.chart import SiTrendChart
from siui.components.combobox import SiComboBox
from siui.components.editbox import SiCapsuleLineEdit
from siui.components.label import HyperRoundBorderTest
from siui.components.menu import SiMenu
from siui.components.page import SiPage
from siui.components.progress_bar import SiProgressBar
from siui.components.slider import SiSliderH
from siui.components.slider_ import SiCoordinatePicker2D, SiCoordinatePicker3D, SiSlider
from siui.components.spinbox.spinbox import SiDoubleSpinBox, SiIntSpinBox
from siui.components.widgets import (
    SiCheckBox,
    SiDenseHContainer,
    SiDraggableLabel,
    SiIconLabel,
    SiLabel,
    SiLongPressButton,
    SiPixLabel,
    SiPushButton,
    SiRadioButton,
    SiSimpleButton,
    SiSwitch,
    SiToggleButton,
)
from siui.components.widgets.expands import SiHoverExpandWidget
from siui.components.widgets.navigation_bar import SiNavigationBarH, SiNavigationBarV
from siui.components.widgets.table import SiTableView
from siui.components.widgets.timedate import SiCalenderView, SiTimePicker, SiTimeSpanPicker
from siui.components.widgets.timeline import SiTimeLine, SiTimeLineItem
from siui.core import Si, SiColor, SiGlobal

from ..option_card import OptionCardPlaneForWidgetDemos
from .components.demo_tables import DemoOsuPlayerRankingTableManager


class ExampleWidgets(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(64)
        self.setScrollMaximumWidth(1000)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("控件")

        # 创建控件组
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setSpacing(32)
        self.titled_widgets_group.setAdjustWidgetsSize(True)  # 禁用调整宽度

        # 标签
        with self.titled_widgets_group as group:
            group.addTitle("标签")

            # 文字标签
            self.label_for_text = OptionCardPlaneForWidgetDemos(self)
            self.label_for_text.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                 "/widgets/label.py")
            self.label_for_text.setTitle("文字标签")

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

            container_pix_label = SiDenseHContainer(self)
            container_pix_label.setAlignment(Qt.AlignCenter)
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

            # 扩展控件
            self.expands = OptionCardPlaneForWidgetDemos(self)
            self.expands.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                           "/widgets/button.py")
            self.expands.setTitle("扩展控件")

            self.demo_expands = SiHoverExpandWidget(self)
            self.demo_expands.resize(96, 32)

            self.expands.body().addWidget(self.demo_expands)
            self.expands.body().addPlaceholder(12)
            self.expands.adjustSize()

            # <- 添加到控件组
            group.addWidget(self.label_for_text)
            group.addWidget(self.pix_label)
            group.addWidget(self.label_ani)
            group.addWidget(self.draggable_label)
            group.addWidget(self.showup_effect)
            group.addWidget(self.expands)

        # 按钮
        with self.titled_widgets_group as group:
            group.addTitle("按钮")

            # 按钮
            self.refactor_buttons = OptionCardPlaneForWidgetDemos(self)
            self.refactor_buttons.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                               "/widgets/button.py")
            self.refactor_buttons.setTitle("重构的按钮")

            self.refactor_pushbutton = SiPushButtonRefactor(self)
            self.refactor_pushbutton.setText("Confirm")
            self.refactor_pushbutton.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_mail_checkmark_filled"))
            self.refactor_pushbutton.adjustSize()

            self.refactor_progress_button = SiProgressPushButton(self)
            self.refactor_progress_button.setText("Downloading")
            self.refactor_progress_button.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_arrow_download_filled"))
            self.refactor_progress_button.setToolTip("Click me to set a random progress value.")
            self.refactor_progress_button.clicked.connect(lambda: self.refactor_progress_button.setProgress(random.random() * 1.3))
            self.refactor_progress_button.adjustSize()

            self.refactor_long_press_button = SiLongPressButtonRefactor(self)
            self.refactor_long_press_button.setText("Delete Files")
            self.refactor_long_press_button.setToolTip("Hold me to confirm.<br><strong>Your files will be lost forever!</strong>")
            self.refactor_long_press_button.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_delete_filled"))
            self.refactor_long_press_button.longPressed.connect(lambda: self.refactor_long_press_button.setToolTip("Deleted!"))
            self.refactor_long_press_button.adjustSize()

            self.refactor_flat_button = SiFlatButton(self)
            self.refactor_flat_button.setText("Flat Button")
            self.refactor_flat_button.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_wrench_settings_filled"))
            self.refactor_flat_button.adjustSize()

            self.refactor_toggle_button = SiToggleButtonRefactor(self)
            self.refactor_toggle_button.setText("Auto Save")
            self.refactor_toggle_button.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_save_filled"))
            self.refactor_toggle_button.adjustSize()

            self.refactor_slider = SiSlider(self)
            self.refactor_slider.resize(512, 32)
            self.refactor_slider.setValue(5)
            self.refactor_slider.setMinimum(-50)
            self.refactor_slider.setMaximum(50)
            self.refactor_slider.setToolTipConvertionFunc(lambda x: f"{x} ms")

            self.refactor_slider2 = SiSlider(self)
            self.refactor_slider2.resize(32, 256)
            self.refactor_slider2.setOrientation(Qt.Orientation.Vertical)
            self.refactor_slider2.setValue(0)
            self.refactor_slider2.setMinimum(-30)
            self.refactor_slider2.setMaximum(12)
            self.refactor_slider2.setToolTipConvertionFunc(lambda x: f"{x} dB")

            self.coordinate_picker_2d = SiCoordinatePicker3D(self)
            self.coordinate_picker_2d.resize(384, 256)
            self.coordinate_picker_2d.slider_z.setMaximum(6)

            self.refactor_switch = SiSwitchRefactor(self)

            self.test_rect = HyperRoundBorderTest(self)
            self.test_rect.resize(256, 128)

            self.original_rect = QLabel(self)
            self.original_rect.resize(64, 64)
            self.original_rect.setStyleSheet("background-color: transparent; border-radius: 14px; border: 1px solid #D087DF")
            # self.trend_chart.adjustViewRect()
            # print(self.trend_chart.viewRect())

            self.linear_edit_box = SiCapsuleLineEdit(self)
            self.linear_edit_box.resize(560, 36)
            self.linear_edit_box.setTitle("项目名称")

            self.linear_edit_box2 = SiCapsuleLineEdit(self)
            self.linear_edit_box2.resize(560, 36)
            self.linear_edit_box2.setTitle("项目所属人")

            # self.refactor_buttons.body().setAdjustWidgetsSize(True)
            self.refactor_buttons.body().addWidget(self.refactor_pushbutton)
            self.refactor_buttons.body().addWidget(self.refactor_progress_button)
            self.refactor_buttons.body().addWidget(self.refactor_long_press_button)
            self.refactor_buttons.body().addWidget(self.refactor_flat_button)
            self.refactor_buttons.body().addWidget(self.refactor_toggle_button)
            self.refactor_buttons.body().addWidget(self.refactor_switch)
            self.refactor_buttons.body().addWidget(self.refactor_slider)
            self.refactor_buttons.body().addWidget(self.refactor_slider2)
            self.refactor_buttons.body().addWidget(self.coordinate_picker_2d)
            self.refactor_buttons.body().addWidget(self.test_rect)
            self.refactor_buttons.body().addWidget(self.original_rect)
            self.refactor_buttons.body().addWidget(self.linear_edit_box)
            self.refactor_buttons.body().addWidget(self.linear_edit_box2)
            # self.refactor_buttons.body().addWidget(self.trend_chart)

            self.refactor_buttons.body().addPlaceholder(12)
            self.refactor_buttons.adjustSize()

            self.refactor_radiobuttons = OptionCardPlaneForWidgetDemos(self)
            self.refactor_radiobuttons.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                               "/widgets/button.py")
            self.refactor_radiobuttons.setTitle("单行单选框")

            radio_button_container = SiDenseVContainer(self)
            radio_button_container.setSpacing(6)

            self.refactor_radio_button = SiRadioButtonRefactor(self)
            self.refactor_radio_button.setText("I want to go sleep now")
            self.refactor_radio_button.adjustSize()
            self.refactor_radio_button.setChecked(True)

            self.refactor_radio_button2 = SiRadioButtonRefactor(self)
            self.refactor_radio_button2.setText("你干嘛嗨嗨呦")
            self.refactor_radio_button2.adjustSize()

            self.refactor_radio_button3 = SiRadioButtonRefactor(self)
            self.refactor_radio_button3.setText("唱跳 Rap 篮球")
            self.refactor_radio_button3.adjustSize()

            self.refactor_radio_button4 = SiRadioButtonRefactor(self)
            self.refactor_radio_button4.setText("不是哥们我真的要困死了让我睡觉吧")
            self.refactor_radio_button4.adjustSize()

            self.refactor_radio_button5 = SiRadioButtonRefactor(self)
            self.refactor_radio_button5.setText("nihao")
            self.refactor_radio_button5.adjustSize()

            radio_button_container.addWidget(self.refactor_radio_button)
            radio_button_container.addWidget(self.refactor_radio_button2)
            radio_button_container.addWidget(self.refactor_radio_button3)
            radio_button_container.addWidget(self.refactor_radio_button4)
            radio_button_container.addWidget(self.refactor_radio_button5)
            radio_button_container.adjustSize()

            self.refactor_radiobuttons.body().addWidget(radio_button_container)
            self.refactor_radiobuttons.body().addPlaceholder(12)
            self.refactor_radiobuttons.adjustSize()

            self.refactor_radiobuttons_desc = OptionCardPlaneForWidgetDemos(self)
            self.refactor_radiobuttons_desc.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                               "/widgets/button.py")
            self.refactor_radiobuttons_desc.setTitle("带解释的单选框")

            radio_button_container = SiDenseVContainer(self)
            radio_button_container.setSpacing(6)

            self.refactor_radio_button = SiRadioButtonWithDescription(self)
            self.refactor_radio_button.setText("Hello World")
            self.refactor_radio_button.setDescription("This is the description of Item1, which is very long.")
            self.refactor_radio_button.setDescriptionWidth(180)
            self.refactor_radio_button.adjustSize()
            self.refactor_radio_button.setChecked(True)

            self.refactor_radio_button2 = SiRadioButtonWithDescription(self)
            self.refactor_radio_button2.setText("我吃你牛魔")
            self.refactor_radio_button2.setDescription("这是第二个选项的解释，短一些")
            self.refactor_radio_button2.setDescriptionWidth(180)
            self.refactor_radio_button2.adjustSize()

            self.refactor_radio_button3 = SiRadioButtonWithDescription(self)
            self.refactor_radio_button3.setText("诗人我吃")
            self.refactor_radio_button3.setDescription("你干嘛嗨嗨呦~")
            self.refactor_radio_button3.setDescriptionWidth(180)
            self.refactor_radio_button3.adjustSize()

            radio_button_container.addWidget(self.refactor_radio_button)
            radio_button_container.addWidget(self.refactor_radio_button2)
            radio_button_container.addWidget(self.refactor_radio_button3)
            radio_button_container.adjustSize()

            self.refactor_radiobuttons_desc.body().addWidget(radio_button_container)
            self.refactor_radiobuttons_desc.body().addPlaceholder(12)
            self.refactor_radiobuttons_desc.adjustSize()


            self.refactor_radiobuttons_avatar = OptionCardPlaneForWidgetDemos(self)
            self.refactor_radiobuttons_avatar.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                               "/widgets/button.py")
            self.refactor_radiobuttons_avatar.setTitle("带头像的单选框")

            radio_button_container = SiDenseVContainer(self)
            radio_button_container.setSpacing(16)

            self.refactor_radio_button = SiRadioButtonWithAvatar(self)
            self.refactor_radio_button.setText("霏泠Ice")
            self.refactor_radio_button.setDescription("114514@nigamna.com")
            self.refactor_radio_button.setIcon(QIcon("./img/avatar1.png"))
            self.refactor_radio_button.adjustSize()
            self.refactor_radio_button.setChecked(True)

            self.refactor_radio_button2 = SiRadioButtonWithAvatar(self)
            self.refactor_radio_button2.setText("我家鸽鸽")
            self.refactor_radio_button2.setDescription("zhiyin@qq.com")
            self.refactor_radio_button2.setIcon(QIcon("./img/avatar2.png"))
            self.refactor_radio_button2.adjustSize()

            self.refactor_radio_button3 = SiRadioButtonWithAvatar(self)
            self.refactor_radio_button3.setText("你干嘛嗨嗨呦")
            self.refactor_radio_button3.setDescription("1231524232@qq.com")
            self.refactor_radio_button3.setIcon(QIcon("./img/avatar1.png"))
            self.refactor_radio_button3.adjustSize()

            radio_button_container.addWidget(self.refactor_radio_button)
            radio_button_container.addWidget(self.refactor_radio_button2)
            radio_button_container.addWidget(self.refactor_radio_button3)
            radio_button_container.adjustSize()

            self.refactor_radiobuttons_avatar.body().addWidget(radio_button_container)
            self.refactor_radiobuttons_avatar.body().addPlaceholder(12)
            self.refactor_radiobuttons_avatar.adjustSize()


            # 按钮
            self.push_buttons = OptionCardPlaneForWidgetDemos(self)
            self.push_buttons.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                               "/widgets/button.py")
            self.push_buttons.setTitle("按压按钮")

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

            self.demo_switch = SiSwitch(self)

            self.switches.body().addWidget(self.demo_switch)
            self.switches.body().addPlaceholder(12)
            self.switches.adjustSize()

            # 单选框
            self.radio_buttons = OptionCardPlaneForWidgetDemos(self)
            self.radio_buttons.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                "/widgets/button.py")
            self.radio_buttons.setTitle("单选框")

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

            self.demo_checkbox_a = SiCheckBox(self)
            self.demo_checkbox_a.setText("安装基本组件")

            self.demo_checkbox_b = SiCheckBox(self)
            self.demo_checkbox_b.setText("安装高级组件")

            self.checkboxes.body().addWidget(self.demo_checkbox_a)
            self.checkboxes.body().addWidget(self.demo_checkbox_b)
            self.checkboxes.body().addPlaceholder(12)
            self.checkboxes.adjustSize()

            group.addWidget(self.refactor_buttons)
            group.addWidget(self.refactor_radiobuttons)
            group.addWidget(self.refactor_radiobuttons_desc)
            group.addWidget(self.refactor_radiobuttons_avatar)
            group.addWidget(self.push_buttons)
            group.addWidget(self.flat_buttons)
            group.addWidget(self.switches)
            group.addWidget(self.radio_buttons)
            group.addWidget(self.checkboxes)

        # 输入组件
        with self.titled_widgets_group as group:
            group.addTitle("输入组件")

            # 带删除单行输入组件
            self.line_edit_with_del_button = OptionCardPlaneForWidgetDemos(self)
            self.line_edit_with_del_button.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                            "/widgets/slider/slider.py")
            self.line_edit_with_del_button.setTitle("带删除单行输入组件")

            self.demo_line_edit_with_del_button = SiLineEditWithDeletionButton(self)
            self.demo_line_edit_with_del_button.resize(256, 32)
            self.demo_line_edit_with_del_button.lineEdit().setText("点击右侧按钮以删除文字")

            self.line_edit_with_del_button.body().addWidget(self.demo_line_edit_with_del_button)
            self.line_edit_with_del_button.body().addPlaceholder(12)
            self.line_edit_with_del_button.adjustSize()

            # 整数微调组件
            self.int_spin_box = OptionCardPlaneForWidgetDemos(self)
            self.int_spin_box.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                               "/widgets/slider/slider.py")
            self.int_spin_box.setTitle("整数微调组件")

            self.demo_int_spin_box = SiIntSpinBox(self)
            self.demo_int_spin_box.resize(256, 32)

            self.int_spin_box.body().addWidget(self.demo_int_spin_box)
            self.int_spin_box.body().addPlaceholder(12)
            self.int_spin_box.adjustSize()

            # 浮点数微调组件
            self.double_spin_box = OptionCardPlaneForWidgetDemos(self)
            self.double_spin_box.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                  "/widgets/slider/slider.py")
            self.double_spin_box.setTitle("浮点数微调组件")

            self.demo_double_spin_box = SiDoubleSpinBox(self)
            self.demo_double_spin_box.resize(256, 32)

            self.double_spin_box.body().addWidget(self.demo_double_spin_box)
            self.double_spin_box.body().addPlaceholder(12)
            self.double_spin_box.adjustSize()

            # 具名输入框
            self.named_line_edit = OptionCardPlaneForWidgetDemos(self)
            self.named_line_edit.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                  "/widgets/slider/slider.py")
            self.named_line_edit.setTitle("具名输入框")

            self.demo_named_line_edit_1 = SiLineEditWithItemName(self)
            self.demo_named_line_edit_1.setName("项目名称")
            self.demo_named_line_edit_1.lineEdit().setText("PyQt-SiliconUI")
            self.demo_named_line_edit_1.resize(512, 32)

            self.demo_named_line_edit_2 = SiLineEditWithItemName(self)
            self.demo_named_line_edit_2.setName("项目所有人")
            self.demo_named_line_edit_2.lineEdit().setText("IceF")
            self.demo_named_line_edit_2.resize(512, 32)

            self.demo_named_line_edit_3 = SiLineEditWithItemName(self)
            self.demo_named_line_edit_3.setName("贡献者")
            self.demo_named_line_edit_3.lineEdit().setText("Every Contributor")
            self.demo_named_line_edit_3.resize(512, 32)

            self.named_line_edit.body().addWidget(self.demo_named_line_edit_1)
            self.named_line_edit.body().addWidget(self.demo_named_line_edit_2)
            self.named_line_edit.body().addWidget(self.demo_named_line_edit_3)
            self.named_line_edit.body().addPlaceholder(12)
            self.named_line_edit.adjustSize()

            group.addWidget(self.line_edit_with_del_button)
            group.addWidget(self.int_spin_box)
            group.addWidget(self.double_spin_box)
            group.addWidget(self.named_line_edit)

        # 滑条
        with self.titled_widgets_group as group:
            group.addTitle("滑条")

            # 滑条
            self.sliders = OptionCardPlaneForWidgetDemos(self)
            self.sliders.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                          "/widgets/slider/slider.py")
            self.sliders.setTitle("滑条")

            self.demo_slider = SiSliderH(self)
            self.demo_slider.resize(500, 32)
            self.demo_slider.setMinimum(-20)
            self.demo_slider.setMaximum(20)
            self.demo_slider.setValue(0, move_to=False)

            self.sliders.body().setAdjustWidgetsSize(True)
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

            self.demo_progress_bar = SiProgressBar(self)
            self.demo_progress_bar.resize(700, 32)

            container_progress_bar_ctrl_buttons = SiDenseHContainer(self)
            container_progress_bar_ctrl_buttons.setFixedHeight(32)

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

            self.progress_bar_linear.body().setAdjustWidgetsSize(True)
            self.progress_bar_linear.body().addWidget(self.demo_progress_bar)
            self.progress_bar_linear.body().addWidget(container_progress_bar_ctrl_buttons)
            self.progress_bar_linear.body().addPlaceholder(12)
            self.progress_bar_linear.adjustSize()

            # 环形进度条
            self.progress_bar_circular = OptionCardPlaneForWidgetDemos(self)
            self.progress_bar_circular.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui"
                                                        "/components/widgets/progress_bar/progress_bar.py")
            self.progress_bar_circular.setTitle("环形进度条")

            self.demo_progress_bar_circular = SiCircularProgressBar(self)
            self.demo_progress_bar_circular.resize(32, 32)
            self.demo_progress_bar_circular.setValue(0.7)

            container_progress_bar_circular_ctrl_buttons = SiDenseHContainer(self)
            container_progress_bar_circular_ctrl_buttons.setFixedHeight(32)

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

            self.demo_progress_bar_circular_indeterminate = SiCircularProgressBar(self)
            self.demo_progress_bar_circular_indeterminate.resize(32, 32)
            self.demo_progress_bar_circular_indeterminate.setIndeterminate(True)

            self.progress_bar_circular_indeterminate.body().addWidget(self.demo_progress_bar_circular_indeterminate)
            self.progress_bar_circular_indeterminate.body().addPlaceholder(12)
            self.progress_bar_circular_indeterminate.adjustSize()

            group.addWidget(self.progress_bar_linear)
            group.addWidget(self.progress_bar_circular)
            group.addWidget(self.progress_bar_circular_indeterminate)

        # 菜单
        with self.titled_widgets_group as group:
            group.addTitle("菜单")

            # 右键菜单
            self.menus = OptionCardPlaneForWidgetDemos(self)
            self.menus.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                        "/widgets/progress_bar/progress_bar.py")
            self.menus.setTitle("右键菜单")

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
            self.demo_show_menu_button.attachment().setText("点击显示菜单")
            self.demo_show_menu_button.clicked.connect(lambda: menu_test.unfold(QCursor.pos().x(), QCursor.pos().y()))

            self.menus.body().addWidget(self.demo_show_menu_button)
            self.menus.body().addPlaceholder(12)
            self.menus.adjustSize()

            # 下拉菜单
            self.combobox = OptionCardPlaneForWidgetDemos(self)
            self.combobox.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                           "/widgets/progress_bar/progress_bar.py")
            self.combobox.setTitle("下拉菜单")

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

            self.combobox.body().addWidget(self.demo_combobox)
            self.combobox.body().addPlaceholder(12)
            self.combobox.adjustSize()

            group.addWidget(self.menus)
            group.addWidget(self.combobox)

        # 表格
        with self.titled_widgets_group as group:
            group.addTitle("表格")

            # 简单表格
            self.table_simple = OptionCardPlaneForWidgetDemos(self)
            self.table_simple.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                               "/widgets/progress_bar/progress_bar.py")
            self.table_simple.setTitle("简单表格")

            self.demo_table_simple = SiTableView(self)
            self.demo_table_simple.resize(752, 360)
            self.demo_table_simple.addColumn("歌曲名", 190, 40, Qt.AlignLeft | Qt.AlignVCenter)
            self.demo_table_simple.addColumn("歌手", 160, 40, Qt.AlignLeft | Qt.AlignVCenter)
            self.demo_table_simple.addColumn("专辑", 240, 40, Qt.AlignLeft | Qt.AlignVCenter)
            self.demo_table_simple.addColumn("时长", 64, 40, Qt.AlignRight | Qt.AlignVCenter)
            self.demo_table_simple.addRow(data=["どうして", "高瀬統也", "どうして (feat. 野田愛実)", "03:01"])
            self.demo_table_simple.addRow(data=["風色Letter", "水瀬いのり", "glow", "04:38"])
            self.demo_table_simple.addRow(data=["ステンドノクターン", "初音ミク", "ステンドノクターン", "03:39"])
            self.demo_table_simple.addRow(data=["鯖鯖", "山崎あおい", "鯖鯖", "05:06"])
            self.demo_table_simple.addRow(data=["優しい恋人", "しまも", "優しい恋人", "05:42"])
            self.demo_table_simple.addRow(data=["Summer Dream", "Kirara Magic", "Summer Dream (feat. Chevy)", "03:36"])
            self.demo_table_simple.addRow(data=["RPG", "Lefty Hand Cream", "Lefty Hand Covers Ⅱ", "04:16"])
            self.demo_table_simple.addRow(data=["The des Alizes", "Foxtail-Grass Studio", "Re*Collection", "03:40"])
            self.demo_table_simple.addRow(data=["他追着风", "霏泠Ice", "他追着风", "04:39"])
            self.demo_table_simple.addRow(data=["ちるちる", "REOL", "Σ", "03:17"])
            self.demo_table_simple.addRow(data=["展 / Re: Expansion", "RABPIT", "序章: 弥卢", "04:00"])
            self.demo_table_simple.addRow(data=["Never Gonna Give You Up", "Rick Astley", "Whenever You Need Somebody", "03:34"])

            self.table_simple.body().setAdjustWidgetsSize(True)
            self.table_simple.body().addWidget(self.demo_table_simple)
            self.table_simple.body().addPlaceholder(12)
            self.table_simple.adjustSize()

            # 使用管理器的表格
            self.table_managed = OptionCardPlaneForWidgetDemos(self)
            self.table_managed.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                "/widgets/progress_bar/progress_bar.py")
            self.table_managed.setTitle("使用管理器的表格")

            self.demo_table_managed = SiTableView(self)
            self.demo_table_managed.resize(952, 250)
            self.demo_table_managed.setManager(DemoOsuPlayerRankingTableManager(self.demo_table_managed))
            self.demo_table_managed.addColumn("排名", 32, 40, Qt.AlignRight | Qt.AlignVCenter)
            self.demo_table_managed.addColumn("", 80, 40, Qt.AlignHCenter | Qt.AlignVCenter)
            self.demo_table_managed.addColumn("得分", 80, 40, Qt.AlignLeft | Qt.AlignVCenter)
            self.demo_table_managed.addColumn("准确度", 80, 40, Qt.AlignLeft | Qt.AlignVCenter)
            self.demo_table_managed.addColumn("", 33, 40, Qt.AlignLeft | Qt.AlignVCenter)
            self.demo_table_managed.addColumn("玩家用户名", 244, 40, Qt.AlignLeft | Qt.AlignVCenter)
            self.demo_table_managed.addColumn("GREAT", 54, 40, Qt.AlignLeft | Qt.AlignVCenter)
            self.demo_table_managed.addColumn("OK", 54, 40, Qt.AlignLeft | Qt.AlignVCenter)
            self.demo_table_managed.addColumn("MEM", 54, 40, Qt.AlignLeft | Qt.AlignVCenter)
            self.demo_table_managed.addColumn("MISS", 54, 40, Qt.AlignLeft | Qt.AlignVCenter)
            self.demo_table_managed.addColumn("PP", 54, 40, Qt.AlignLeft | Qt.AlignVCenter)
            self.demo_table_managed.addRow(
                data=["#1", "S", "1,144,713", "99.36%", "China", "PrettyChicken", "514", "3", "0", "0", "114"]
            )
            self.demo_table_managed.addRow(
                data=["#2", "SS", "1,122,268", "100.00%", "United State", "Rick_Astley_4123", "517", "0", "0", "0", "166"]
            )
            self.demo_table_managed.addRow(
                data=["#3", "SS", "1,122,257", "100.00%", "Great Britain", "FishAndChips", "517", "0", "0", "0", "169"]
            )
            self.demo_table_managed.addRow(
                data=["#4", "SS", "1,122,190", "100.00%", "China", "SunXiaoChuan", "517", "0", "0", "0", "157"]
            )
            self.demo_table_managed.addRow(
                data=["#5", "S", "1,100,785", "99.12%", "China", "Sagiri_Chan", "514", "2", "1", "0", "143"]
            )

            self.table_managed.body().setAdjustWidgetsSize(True)
            self.table_managed.body().addWidget(self.demo_table_managed)
            self.table_managed.body().addPlaceholder(12)
            self.table_managed.adjustSize()

            group.addWidget(self.table_simple)
            group.addWidget(self.table_managed)

        # 导航栏
        with self.titled_widgets_group as group:
            group.addTitle("导航栏")

            # 水平导航栏
            self.navigation_bar_h = OptionCardPlaneForWidgetDemos(self)
            self.navigation_bar_h.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                   "/widgets/progress_bar/progress_bar.py")
            self.navigation_bar_h.setTitle("水平导航栏")

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

            # 垂直导航栏
            self.navigation_bar_v = OptionCardPlaneForWidgetDemos(self)
            self.navigation_bar_v.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                   "/widgets/progress_bar/progress_bar.py")
            self.navigation_bar_v.setTitle("横向导航栏")

            self.demo_navigation_bar_v = SiNavigationBarV(self)
            self.demo_navigation_bar_v.addItem("基本信息")
            self.demo_navigation_bar_v.addItem("排名")
            self.demo_navigation_bar_v.addItem("最近通过谱面")
            self.demo_navigation_bar_v.addItem("最佳表现")
            self.demo_navigation_bar_v.addItem("创建的谱面")
            self.demo_navigation_bar_v.setCurrentIndex(0)
            self.demo_navigation_bar_v.adjustSize()

            self.navigation_bar_v.body().addWidget(self.demo_navigation_bar_v)
            self.navigation_bar_v.body().addPlaceholder(12)
            self.navigation_bar_v.adjustSize()

            group.addWidget(self.navigation_bar_h)
            group.addWidget(self.navigation_bar_v)

        # 单项选择栏
        with self.titled_widgets_group as group:
            group.addTitle("单项选择栏")

            # 水平单项选择栏
            self.selection_bar_h = OptionCardPlaneForWidgetDemos(self)
            self.selection_bar_h.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                  "/widgets/progress_bar/progress_bar.py")
            self.selection_bar_h.setTitle("水平单项选择栏")

            self.demo_selection_bar_h = SiNavigationBarH(self)
            self.demo_selection_bar_h.setNoIndicator(True)
            self.demo_selection_bar_h.addItem("全部语言")
            self.demo_selection_bar_h.addItem("汉语")
            self.demo_selection_bar_h.addItem("英语")
            self.demo_selection_bar_h.addItem("日语")
            self.demo_selection_bar_h.addItem("纯音乐")
            self.demo_selection_bar_h.setCurrentIndex(0)
            self.demo_selection_bar_h.adjustSize()

            self.selection_bar_h.body().addWidget(self.demo_selection_bar_h)
            self.selection_bar_h.body().addPlaceholder(12)
            self.selection_bar_h.adjustSize()

            # 垂直单项选择栏
            self.selection_bar_v = OptionCardPlaneForWidgetDemos(self)
            self.selection_bar_v.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                  "/widgets/progress_bar/progress_bar.py")
            self.selection_bar_v.setTitle("垂直单项选择栏")

            self.demo_selection_bar_v = SiNavigationBarV(self)
            self.demo_selection_bar_v.setNoIndicator(True)
            self.demo_selection_bar_v.addItem("唱歌")
            self.demo_selection_bar_v.addItem("跳舞")
            self.demo_selection_bar_v.addItem("说唱")
            self.demo_selection_bar_v.addItem("篮球")
            self.demo_selection_bar_v.setCurrentIndex(0)
            self.demo_selection_bar_v.adjustSize()

            self.selection_bar_v.body().addWidget(self.demo_selection_bar_v)
            self.selection_bar_v.body().addPlaceholder(12)
            self.selection_bar_v.adjustSize()

            group.addWidget(self.selection_bar_h)
            group.addWidget(self.selection_bar_v)

        with self.titled_widgets_group as group:
            group.addTitle("时间线")

            # 时间线
            self.timeline = OptionCardPlaneForWidgetDemos(self)
            self.timeline.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                           "/widgets/progress_bar/progress_bar.py")
            self.timeline.setTitle("时间线")

            self.demo_timeline = SiTimeLine(self)
            self.demo_timeline.setFixedWidth(600)

            item1 = SiTimeLineItem(self)
            item1.setContent("11:45:14", "田所浩二 访问了你的电脑")
            item1.adjustSize()

            item2 = SiTimeLineItem(self)
            item2.setContent("19:19:10", "警告：接受的包过多，可能存在潜在攻击行为")
            item2.setIcon(SiGlobal.siui.iconpack.get(
                "ic_fluent_warning_shield_filled", color_code=self.getColor(SiColor.PROGRESS_BAR_COMPLETING)))
            item2.setIconHint("安全警告")
            item2.setThemeColor(self.getColor(SiColor.PROGRESS_BAR_COMPLETING))
            item2.adjustSize()

            item3 = SiTimeLineItem(self)
            item3.setContent("00:00:00", "问题已清除")
            item3.setIcon(SiGlobal.siui.iconpack.get(
                "ic_fluent_shield_checkmark_filled", color_code=self.getColor(SiColor.SIDE_MSG_THEME_SUCCESS)))
            item3.setIconHint("警报解除")
            item3.setThemeColor(self.getColor(SiColor.SIDE_MSG_THEME_SUCCESS))
            item3.adjustSize()

            self.demo_timeline.addWidget(item1)
            self.demo_timeline.addWidget(item2)
            self.demo_timeline.addWidget(item3)

            self.timeline.body().addWidget(self.demo_timeline)
            self.timeline.body().addPlaceholder(12)
            self.timeline.adjustSize()

            # 日历视图
            self.calender_view = OptionCardPlaneForWidgetDemos(self)
            self.calender_view.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                "/widgets/progress_bar/progress_bar.py")
            self.calender_view.setTitle("日历视图")

            self.demo_calender_view = SiCalenderView(self)
            self.demo_calender_view.adjustSize()

            self.ctrl_set_today = SiPushButton(self)
            self.ctrl_set_today.resize(128, 32)
            self.ctrl_set_today.attachment().setText("设为今天")
            self.ctrl_set_today.clicked.connect(lambda: self.demo_calender_view.setDate(datetime.date.today()))

            self.calender_view.body().addWidget(self.demo_calender_view)
            self.calender_view.body().addWidget(self.ctrl_set_today)
            self.calender_view.body().addPlaceholder(12)
            self.calender_view.adjustSize()

            # 时间选择器
            self.time_picker = OptionCardPlaneForWidgetDemos(self)
            self.time_picker.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                "/widgets/progress_bar/progress_bar.py")
            self.time_picker.setTitle("时间选择器")

            self.demo_time_picker = SiTimePicker(self)
            self.demo_time_picker.adjustSize()

            self.ctrl_set_now = SiPushButton(self)
            self.ctrl_set_now.resize(128, 32)
            self.ctrl_set_now.attachment().setText("还原")
            self.ctrl_set_now.clicked.connect(lambda: self.demo_time_picker.setTime(datetime.time(0, 0, 0)))

            self.time_picker.body().addWidget(self.demo_time_picker)
            self.time_picker.body().addWidget(self.ctrl_set_now)
            self.time_picker.body().addPlaceholder(12)
            self.time_picker.adjustSize()

            # 时长选择器
            self.time_span_picker = OptionCardPlaneForWidgetDemos(self)
            self.time_span_picker.setSourceCodeURL("https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/siui/components"
                                                "/widgets/progress_bar/progress_bar.py")
            self.time_span_picker.setTitle("时长选择器")

            self.demo_time_span_picker = SiTimeSpanPicker(self)
            self.demo_time_span_picker.adjustSize()

            self.ctrl_set_zero = SiPushButton(self)
            self.ctrl_set_zero.resize(128, 32)
            self.ctrl_set_zero.attachment().setText("还原")
            self.ctrl_set_zero.clicked.connect(lambda: self.demo_time_span_picker.setTimeSpan(datetime.timedelta()))

            self.time_span_picker.body().addWidget(self.demo_time_span_picker)
            self.time_span_picker.body().addWidget(self.ctrl_set_zero)
            self.time_span_picker.body().addPlaceholder(12)
            self.time_span_picker.adjustSize()

            group.addWidget(self.timeline)
            group.addWidget(self.calender_view)
            group.addWidget(self.time_picker)
            group.addWidget(self.time_span_picker)

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
