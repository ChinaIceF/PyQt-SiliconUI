import random

from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel

from siui.components import SiDenseHContainer, SiTitledWidgetGroup, SiLongPressButton, SiDenseVContainer
from siui.components.button import SiPushButtonRefactor, SiProgressPushButton, SiLongPressButtonRefactor, SiFlatButton, \
    SiToggleButtonRefactor, SiSwitchRefactor, SiRadioButtonWithAvatar, SiRadioButtonWithDescription, \
    SiRadioButtonRefactor
from siui.components.chart import SiTrendChart
from siui.components.page import SiPage
from siui.components.slider_ import SiSlider, SiCoordinatePicker2D, SiCoordinatePicker3D
from siui.core import SiGlobal
from siui.gui import SiFont

from ..option_card import OptionCardPlaneForWidgetDemos


class RefactoredWidgets(SiPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPadding(64)
        self.setScrollMaximumWidth(1000)
        self.setScrollAlignment(Qt.AlignLeft)
        self.setTitle("重构控件")

        # 创建控件组
        self.titled_widgets_group = SiTitledWidgetGroup(self)
        self.titled_widgets_group.setSpacing(32)
        self.titled_widgets_group.setAdjustWidgetsSize(True)  # 禁用调整宽度

        # 按钮
        with self.titled_widgets_group as group:
            group.addTitle("按钮")

            # 按压按钮
            self.push_buttons = OptionCardPlaneForWidgetDemos(self)
            self.push_buttons.setTitle("按压按钮")

            container = SiDenseHContainer(self)

            self.demo_push_button_text = SiPushButtonRefactor(self)
            self.demo_push_button_text.setText("按压按钮")
            self.demo_push_button_text.adjustSize()

            self.demo_push_button_text_icon = SiPushButtonRefactor(self)
            self.demo_push_button_text_icon.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_location_filled"))
            self.demo_push_button_text_icon.setText("获取定位")
            self.demo_push_button_text_icon.setToolTip("包括经纬度、朝向信息")
            self.demo_push_button_text_icon.adjustSize()

            self.demo_push_button_icon = SiPushButtonRefactor(self)
            self.demo_push_button_icon.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_location_filled"))
            self.demo_push_button_icon.setToolTip("获取定位")
            self.demo_push_button_icon.adjustSize()

            container.addWidget(self.demo_push_button_text)
            container.addWidget(self.demo_push_button_text_icon)
            container.addWidget(self.demo_push_button_icon)

            self.push_buttons.body().addWidget(container)
            self.push_buttons.body().addPlaceholder(12)
            self.push_buttons.adjustSize()

            # 进度按钮
            self.progress_buttons = OptionCardPlaneForWidgetDemos(self)
            self.progress_buttons.setTitle("进度按钮")

            container = SiDenseHContainer(self)

            self.demo_progress_button_text = SiProgressPushButton(self)
            self.demo_progress_button_text.setText("进度按钮")
            self.demo_progress_button_text.setToolTip("点击以设置随机进度")
            self.demo_progress_button_text.clicked.connect(lambda: self.demo_progress_button_text.setProgress(random.random() * 1.3))
            self.demo_progress_button_text.clicked.connect(lambda: self.demo_progress_button_text_icon.setProgress(random.random() * 1.3))
            self.demo_progress_button_text.clicked.connect(lambda: self.demo_progress_button_icon.setProgress(random.random() * 1.3))
            self.demo_progress_button_text.adjustSize()

            self.demo_progress_button_text_icon = SiProgressPushButton(self)
            self.demo_progress_button_text_icon.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_arrow_download_filled"))
            self.demo_progress_button_text_icon.setText("下载中")
            self.demo_progress_button_text_icon.adjustSize()

            self.demo_progress_button_icon = SiProgressPushButton(self)
            self.demo_progress_button_icon.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_arrow_download_filled"))
            self.demo_progress_button_icon.setToolTip("下载中")
            self.demo_progress_button_icon.adjustSize()

            container.addWidget(self.demo_progress_button_text)
            container.addWidget(self.demo_progress_button_text_icon)
            container.addWidget(self.demo_progress_button_icon)

            self.progress_buttons.body().addWidget(container)
            self.progress_buttons.body().addPlaceholder(12)
            self.progress_buttons.adjustSize()

            # 长按确定按钮
            self.long_press_buttons = OptionCardPlaneForWidgetDemos(self)
            self.long_press_buttons.setTitle("长按确定按钮")

            container = SiDenseHContainer(self)

            self.demo_long_press_button_text = SiLongPressButtonRefactor(self)
            self.demo_long_press_button_text.setText("格式化磁盘")
            self.demo_long_press_button_text.setToolTip("长按以确认")
            self.demo_long_press_button_text.adjustSize()

            self.demo_long_press_button_text_icon = SiLongPressButtonRefactor(self)
            self.demo_long_press_button_text_icon.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_delete_filled"))
            self.demo_long_press_button_text_icon.setText("删除备份")
            self.demo_long_press_button_text_icon.setToolTip("长按以确认")
            self.demo_long_press_button_text_icon.adjustSize()

            self.demo_long_press_button_icon = SiLongPressButtonRefactor(self)
            self.demo_long_press_button_icon.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_delete_filled"))
            self.demo_long_press_button_icon.setToolTip("长按以删除备份<br><strong>警告: 此操作将无法撤销</strong>")
            self.demo_long_press_button_icon.adjustSize()

            container.addWidget(self.demo_long_press_button_text)
            container.addWidget(self.demo_long_press_button_text_icon)
            container.addWidget(self.demo_long_press_button_icon)

            self.long_press_buttons.body().addWidget(container)
            self.long_press_buttons.body().addPlaceholder(12)
            self.long_press_buttons.adjustSize()

            # 扁平按钮
            self.flat_buttons = OptionCardPlaneForWidgetDemos(self)
            self.flat_buttons.setTitle("扁平按钮")

            container = SiDenseHContainer(self)

            self.demo_flat_button_text = SiFlatButton(self)
            self.demo_flat_button_text.setText("扁平按钮")
            self.demo_flat_button_text.adjustSize()

            self.demo_flat_button_text_icon = SiFlatButton(self)
            self.demo_flat_button_text_icon.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_zoom_in_filled"))
            self.demo_flat_button_text_icon.setText("放大")
            self.demo_flat_button_text_icon.adjustSize()

            self.demo_flat_button_icon = SiFlatButton(self)
            self.demo_flat_button_icon.resize(32, 32)
            self.demo_flat_button_icon.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_zoom_in_filled"))
            self.demo_flat_button_icon.setToolTip("放大")

            container.addWidget(self.demo_flat_button_text)
            container.addWidget(self.demo_flat_button_text_icon)
            container.addWidget(self.demo_flat_button_icon)

            self.flat_buttons.body().addWidget(container)
            self.flat_buttons.body().addPlaceholder(12)
            self.flat_buttons.adjustSize()

            # 状态切换按钮
            self.toggle_buttons = OptionCardPlaneForWidgetDemos(self)
            self.toggle_buttons.setTitle("状态切换按钮")

            container = SiDenseHContainer(self)

            self.demo_toggle_button_text = SiToggleButtonRefactor(self)
            self.demo_toggle_button_text.setText("自动保存")
            self.demo_toggle_button_text.adjustSize()

            self.demo_toggle_button_text_icon = SiToggleButtonRefactor(self)
            self.demo_toggle_button_text_icon.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_save_filled"))
            self.demo_toggle_button_text_icon.setText("自动保存")
            self.demo_toggle_button_text_icon.adjustSize()

            self.demo_toggle_button_icon = SiToggleButtonRefactor(self)
            self.demo_toggle_button_icon.resize(32, 32)
            self.demo_toggle_button_icon.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_save_filled"))
            self.demo_toggle_button_icon.setToolTip("自动保存")

            container.addWidget(self.demo_toggle_button_text)
            container.addWidget(self.demo_toggle_button_text_icon)
            container.addWidget(self.demo_toggle_button_icon)

            self.toggle_buttons.body().addWidget(container)
            self.toggle_buttons.body().addPlaceholder(12)
            self.toggle_buttons.adjustSize()

            # 开关
            self.switches = OptionCardPlaneForWidgetDemos(self)
            self.switches.setTitle("开关")

            self.demo_switch = SiSwitchRefactor(self)

            self.switches.body().addWidget(self.demo_switch)
            self.switches.body().addPlaceholder(12)
            self.switches.adjustSize()

            group.addWidget(self.push_buttons)
            group.addWidget(self.progress_buttons)
            group.addWidget(self.long_press_buttons)
            group.addWidget(self.flat_buttons)
            group.addWidget(self.toggle_buttons)
            group.addWidget(self.switches)

        # 单选框
        with self.titled_widgets_group as group:
            group.addTitle("单选框")

            self.refactor_radiobuttons = OptionCardPlaneForWidgetDemos(self)
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

            group.addWidget(self.refactor_radiobuttons)
            group.addWidget(self.refactor_radiobuttons_desc)
            group.addWidget(self.refactor_radiobuttons_avatar)

        # 滑动条
        with self.titled_widgets_group as group:
            group.addTitle("滑动条")

            self.sliders_horizontal = OptionCardPlaneForWidgetDemos(self)
            self.sliders_horizontal.setTitle("横向滑动条")

            self.demo_slider_horizontal = SiSlider(self)
            self.demo_slider_horizontal.resize(512, 48)

            self.sliders_horizontal.body().addWidget(self.demo_slider_horizontal)
            self.sliders_horizontal.body().addPlaceholder(12)
            self.sliders_horizontal.adjustSize()

            self.sliders_vertical = OptionCardPlaneForWidgetDemos(self)
            self.sliders_vertical.setTitle("纵向滑动条")

            self.demo_slider_vertical = SiSlider(self)
            self.demo_slider_vertical.resize(48, 140)
            self.demo_slider_vertical.setOrientation(Qt.Orientation.Vertical)

            self.sliders_vertical.body().addWidget(self.demo_slider_vertical)
            self.sliders_vertical.body().addPlaceholder(12)
            self.sliders_vertical.adjustSize()

            self.coordinate_picker_2ds = OptionCardPlaneForWidgetDemos(self)
            self.coordinate_picker_2ds.setTitle("二维坐标选取器")

            self.demo_coordinate_picker_2d = SiCoordinatePicker2D(self)
            self.demo_coordinate_picker_2d.resize(384, 256)
            self.demo_coordinate_picker_2d.slider_x.setValue(72)
            self.demo_coordinate_picker_2d.slider_y.setValue(63)

            self.coordinate_picker_2ds.body().addWidget(self.demo_coordinate_picker_2d)
            self.coordinate_picker_2ds.body().addPlaceholder(6)
            self.coordinate_picker_2ds.adjustSize()

            self.coordinate_picker_3ds = OptionCardPlaneForWidgetDemos(self)
            self.coordinate_picker_3ds.setTitle("三维坐标选取器")

            self.demo_coordinate_picker_3d = SiCoordinatePicker3D(self)
            self.demo_coordinate_picker_3d.resize(384, 256)
            self.demo_coordinate_picker_3d.slider_x.setValue(72)
            self.demo_coordinate_picker_3d.slider_y.setValue(63)
            self.demo_coordinate_picker_3d.slider_z.setMaximum(6)
            self.demo_coordinate_picker_3d.slider_z.setValue(6)

            self.coordinate_picker_3ds.body().addWidget(self.demo_coordinate_picker_3d)
            self.coordinate_picker_3ds.body().addPlaceholder(6)
            self.coordinate_picker_3ds.adjustSize()

            group.addWidget(self.sliders_horizontal)
            group.addWidget(self.sliders_vertical)
            group.addWidget(self.coordinate_picker_2ds)
            group.addWidget(self.coordinate_picker_3ds)

        with self.titled_widgets_group as group:
            group.addTitle("统计图表")

            self.charts = OptionCardPlaneForWidgetDemos(self)
            self.charts.setTitle("趋势折线图")

            self.trend_chart = SiTrendChart(self)
            self.trend_chart.resize(900, 340)
            self.trend_chart.setPointList([QPointF(i, (i/50)**2 * 0 + random.random() * (5 + 25 * ((i + 5) % 20 == 0))) for i in range(-50, 51)])
            self.trend_chart.setToolTipFunc(lambda x, y: f"起始点：{x}\n振幅：{y}")
            self.trend_chart.setQuality(1)
            self.trend_chart.adjustViewRect()

            self.charts.body().setAdjustWidgetsSize(True)
            self.charts.body().addWidget(self.trend_chart)
            self.charts.body().addPlaceholder(12)
            self.charts.adjustSize()

            group.addWidget(self.charts)

        # 添加页脚的空白以增加美观性
        self.titled_widgets_group.addPlaceholder(64)

        # 设置控件组为页面对象
        self.setAttachment(self.titled_widgets_group)
