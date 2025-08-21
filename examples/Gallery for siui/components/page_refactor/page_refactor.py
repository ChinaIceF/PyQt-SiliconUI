import random
from contextlib import contextmanager

from PyQt5.QtCore import QPoint, QPointF, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QBoxLayout, QButtonGroup, QLabel, QSizePolicy, QWidget

from siui.components import SiDenseHContainer, SiDenseVContainer, SiTitledWidgetGroup
from siui.components.button import (
    SiCapsuleButton,
    SiCheckBox,
    SiCheckBoxRefactor,
    SiFlatButton,
    SiFlatButtonWithIndicator,
    SiLongPressButtonRefactor,
    SiOptionButton,
    SiProgressPushButton,
    SiPushButtonRefactor,
    SiRadioButton,
    SiRadioButtonR,
    SiRadioButtonWithAvatar,
    SiRadioButtonWithDescription,
    SiSwitchRefactor,
    SiToggleButtonRefactor,
)
from siui.components.chart import SiTrendChart
from siui.components.combobox_ import SiCapsuleComboBox
from siui.components.container import SiDenseContainer, SiTriSectionPanelCard, SiTriSectionRowCard
from siui.components.editbox import SiCapsuleLineEdit, SiDoubleSpinBox, SiLabeledLineEdit, SiSpinBox
from siui.components.label import SiLabelRefactor, SiLinearIndicator, SiLinearPartitionIndicator
from siui.components.page import SiPage
from siui.components.progress_bar_ import SiProgressBarRefactor
from siui.components.slider_ import SiCoordinatePicker2D, SiCoordinatePicker3D, SiSlider
from siui.core import SiGlobal
from siui.gui import SiFont

from ..option_card import OptionCardPlaneForWidgetDemos
from .example_menu import exampleSiRoundedMenu
from .example_popover import exampleCalenderPickerPopover, exampleDatePickerPopover


@contextmanager
def createPanelCard(parent: QWidget, title: str) -> SiTriSectionPanelCard:
    card = SiTriSectionPanelCard(parent)
    card.setTitle(title)
    try:
        yield card
    finally:
        card.adjustSize()
        parent.addWidget(card)

@contextmanager
def createDenseContainer(parent: SiDenseContainer,
                         direction: QBoxLayout.Direction,
                         side: Qt.Edges = Qt.LeftEdge | Qt.TopEdge) -> SiDenseContainer:
    container = SiDenseContainer(parent)
    container.layout().setDirection(direction)
    container.layout().setSpacing(12)
    container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    try:
        yield container
    finally:
        parent.addWidget(container, side)


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

        with self.titled_widgets_group as group:
            group.addTitle("菜单及弹出框")

            with createPanelCard(group, "菜单演示") as card:
                with createDenseContainer(card.body(), QBoxLayout.LeftToRight) as container:

                    button_menu = SiPushButtonRefactor(self)
                    button_menu.setText("显示菜单")

                    self.example_menu = exampleSiRoundedMenu(button_menu)
                    button_menu.clicked.connect(
                        lambda: self.example_menu.popup(button_menu.mapToGlobal(QPoint(0, button_menu.height())))
                    )

                    container.addWidget(button_menu)

            with createPanelCard(group, "日期选择器") as card:
                with createDenseContainer(card.body(), QBoxLayout.LeftToRight) as container:
                    button_date_picker = exampleDatePickerPopover(container)

                    container.addWidget(button_date_picker)

            with createPanelCard(group, "日历选择器") as card:
                with createDenseContainer(card.body(), QBoxLayout.LeftToRight) as container:
                    button_date_picker = exampleCalenderPickerPopover(container)

                    container.addWidget(button_date_picker)


        with self.titled_widgets_group as group:
            group.addTitle("组合框")

            with createPanelCard(group, "胶囊下拉组合框") as card:
                with createDenseContainer(card.body(), QBoxLayout.LeftToRight) as container:
                    combo_editable = SiCapsuleComboBox(self)
                    combo_editable.setTitle("可编辑组合框")
                    combo_editable.setMinimumHeight(36)
                    combo_editable.setEditable(True)
                    combo_editable.addItems(["Python", "C++", "JavaScript"])

                    combo_not_editable = SiCapsuleComboBox(self)
                    combo_not_editable.setTitle("只读组合框")
                    combo_not_editable.setMinimumHeight(36)
                    combo_not_editable.setEditable(False)
                    combo_not_editable.addItems(["Python", "C++", "JavaScript"])

                    container.addWidget(combo_editable)
                    container.addWidget(combo_not_editable)

        with self.titled_widgets_group as group:
            group.addTitle("进度条")

            with createPanelCard(group, "条形进度条") as card:
                progress_bar = SiProgressBarRefactor(self)
                progress_bar.setMaximum(1000)
                card.body().addWidget(progress_bar)

                with createDenseContainer(card.body(), QBoxLayout.LeftToRight) as container:
                    button_random_value = SiPushButtonRefactor.withText("随机赋值")
                    button_random_value.clicked.connect(
                        lambda: progress_bar.setValue(int(random.random() * 1001)))

                    button_random_add = SiPushButtonRefactor.withText("随机增加")
                    button_random_add.clicked.connect(
                        lambda: progress_bar.setValue(progress_bar.value() + int(random.random() * 50 + 2)))

                    button_loading = SiPushButtonRefactor.withText("加载")
                    button_loading.clicked.connect(
                        lambda: progress_bar.setState(progress_bar.State.Loading))

                    button_processing = SiPushButtonRefactor.withText("处理")
                    button_processing.clicked.connect(
                        lambda: progress_bar.setState(progress_bar.State.Processing))

                    button_paused = SiPushButtonRefactor.withText("暂停")
                    button_paused.clicked.connect(
                        lambda: progress_bar.setState(progress_bar.State.Paused))

                    button_error = SiPushButtonRefactor.withText("错误")
                    button_error.clicked.connect(
                        lambda: progress_bar.setState(progress_bar.State.Error))

                    label_flashing = QLabel(self)
                    label_flashing.setFont(SiFont.getFont(size=14))
                    label_flashing.setText("自动闪烁")
                    label_flashing.setStyleSheet("color: #D1CBD4")

                    button_toggle_flashing = SiSwitchRefactor(self)
                    button_toggle_flashing.toggled.connect(progress_bar.setFlashing)

                    container.addWidget(button_random_value)
                    container.addWidget(button_random_add)
                    container.addWidget(button_error, Qt.RightEdge)
                    container.addWidget(button_paused, Qt.RightEdge)
                    container.addWidget(button_processing, Qt.RightEdge)
                    container.addWidget(button_loading, Qt.RightEdge)
                    container.addWidget(button_toggle_flashing, Qt.RightEdge)
                    container.addWidget(label_flashing, Qt.RightEdge)

        with self.titled_widgets_group as group:
            group.addTitle("按钮")

            with createPanelCard(group, "普通的按钮") as card:
                with createDenseContainer(card.body(), QBoxLayout.LeftToRight) as container:

                    demo_push_button_text = SiPushButtonRefactor(self)
                    demo_push_button_text.setText("按压按钮")
                    demo_push_button_text.adjustSize()

                    demo_push_button_text_icon = SiPushButtonRefactor(self)
                    demo_push_button_text_icon.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_location_filled"))
                    demo_push_button_text_icon.setText("获取定位")
                    demo_push_button_text_icon.setToolTip("包括经纬度、朝向信息")
                    demo_push_button_text_icon.adjustSize()

                    demo_push_button_icon = SiPushButtonRefactor(self)
                    demo_push_button_icon.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_location_filled"))
                    demo_push_button_icon.setToolTip("获取定位")
                    demo_push_button_icon.adjustSize()

                    container.addWidget(demo_push_button_text)
                    container.addWidget(demo_push_button_text_icon)
                    container.addWidget(demo_push_button_icon)

            with createPanelCard(group, "进度按钮") as card:
                with createDenseContainer(card.body(), QBoxLayout.LeftToRight) as container:

                    demo_progress_button_text = SiProgressPushButton(self)
                    demo_progress_button_text.setText("进度按钮")
                    demo_progress_button_text.setToolTip("点击以设置随机进度")
                    demo_progress_button_text.clicked.connect(lambda: demo_progress_button_text.setProgress(random.random() * 1.3))
                    demo_progress_button_text.clicked.connect(lambda: demo_progress_button_text_icon.setProgress(random.random() * 1.3))
                    demo_progress_button_text.clicked.connect(lambda: demo_progress_button_icon.setProgress(random.random() * 1.3))
                    demo_progress_button_text.adjustSize()

                    demo_progress_button_text_icon = SiProgressPushButton(self)
                    demo_progress_button_text_icon.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_arrow_download_filled"))
                    demo_progress_button_text_icon.setText("下载中")
                    demo_progress_button_text_icon.adjustSize()

                    demo_progress_button_icon = SiProgressPushButton(self)
                    demo_progress_button_icon.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_arrow_download_filled"))
                    demo_progress_button_icon.setToolTip("下载中")
                    demo_progress_button_icon.adjustSize()

                    container.addWidget(demo_progress_button_text)
                    container.addWidget(demo_progress_button_text_icon)
                    container.addWidget(demo_progress_button_icon)

            with createPanelCard(group, "长按确定按钮") as card:
                with createDenseContainer(card.body(), QBoxLayout.LeftToRight) as container:

                    demo_long_press_button_text = SiLongPressButtonRefactor(self)
                    demo_long_press_button_text.setText("格式化磁盘")
                    demo_long_press_button_text.setToolTip("长按以确认")
                    demo_long_press_button_text.adjustSize()

                    demo_long_press_button_text_icon = SiLongPressButtonRefactor(self)
                    demo_long_press_button_text_icon.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_delete_filled"))
                    demo_long_press_button_text_icon.setText("删除备份")
                    demo_long_press_button_text_icon.setToolTip("长按以确认")
                    demo_long_press_button_text_icon.adjustSize()

                    demo_long_press_button_icon = SiLongPressButtonRefactor(self)
                    demo_long_press_button_icon.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_delete_filled"))
                    demo_long_press_button_icon.setToolTip("长按以删除备份<br><strong>警告: 此操作将无法撤销</strong>")
                    demo_long_press_button_icon.adjustSize()

                    container.addWidget(demo_long_press_button_text)
                    container.addWidget(demo_long_press_button_text_icon)
                    container.addWidget(demo_long_press_button_icon)

            with createPanelCard(group, "扁平按钮") as card:
                with createDenseContainer(card.body(), QBoxLayout.LeftToRight) as container:

                    demo_flat_button_text = SiFlatButton(self)
                    demo_flat_button_text.setText("扁平按钮")
                    demo_flat_button_text.adjustSize()

                    demo_flat_button_text_icon = SiFlatButton(self)
                    demo_flat_button_text_icon.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_zoom_in_filled"))
                    demo_flat_button_text_icon.setText("放大")
                    demo_flat_button_text_icon.adjustSize()

                    demo_flat_button_icon = SiFlatButton(self)
                    demo_flat_button_icon.resize(32, 32)
                    demo_flat_button_icon.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_zoom_in_filled"))
                    demo_flat_button_icon.setToolTip("放大")

                    container.addWidget(demo_flat_button_text)
                    container.addWidget(demo_flat_button_text_icon)
                    container.addWidget(demo_flat_button_icon)

            with createPanelCard(group, "状态切换按钮") as card:
                with createDenseContainer(card.body(), QBoxLayout.LeftToRight) as container:

                    demo_toggle_button_text = SiToggleButtonRefactor(self)
                    demo_toggle_button_text.setText("自动保存")
                    demo_toggle_button_text.adjustSize()

                    demo_toggle_button_text_icon = SiToggleButtonRefactor(self)
                    demo_toggle_button_text_icon.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_save_filled"))
                    demo_toggle_button_text_icon.setText("自动保存")
                    demo_toggle_button_text_icon.adjustSize()

                    demo_toggle_button_icon = SiToggleButtonRefactor(self)
                    demo_toggle_button_icon.resize(32, 32)
                    demo_toggle_button_icon.setSvgIcon(SiGlobal.siui.iconpack.get("ic_fluent_save_filled"))
                    demo_toggle_button_icon.setToolTip("自动保存")

                    container.addWidget(demo_toggle_button_text)
                    container.addWidget(demo_toggle_button_text_icon)
                    container.addWidget(demo_toggle_button_icon)

            with createPanelCard(group, "胶囊按钮") as card:
                with createDenseContainer(card.body(), QBoxLayout.LeftToRight) as container:

                    capsule_button_1 = SiCapsuleButton(self)
                    capsule_button_1.setText("Likes")
                    capsule_button_1.setValue(114514)
                    capsule_button_1.setToolTip("你好世界")

                    capsule_button_2 = SiCapsuleButton(self)
                    capsule_button_2.setText("Comments")
                    capsule_button_2.setValue(1919)
                    capsule_button_2.setThemeColor(SiCapsuleButton.Theme.Yellow)

                    capsule_button_3 = SiCapsuleButton(self)
                    capsule_button_3.setText("Shares")
                    capsule_button_3.setValue(810)
                    capsule_button_3.setThemeColor(SiCapsuleButton.Theme.Red)

                    container.addWidget(capsule_button_1)
                    container.addWidget(capsule_button_2)
                    container.addWidget(capsule_button_3)

            with createPanelCard(group, "单选/复选按钮") as card:
                with createDenseContainer(card.body(), QBoxLayout.LeftToRight) as h_container:
                    with createDenseContainer(h_container, QBoxLayout.TopToBottom) as container:

                        checkbox1 = SiCheckBoxRefactor(self)
                        checkbox1.setText("多选选项 1")
                        checkbox1.setDescription("唱，跳，Rap，篮球")
                        checkbox1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

                        checkbox2 = SiCheckBoxRefactor(self)
                        checkbox2.setText("多选选项 2")
                        checkbox2.setDescription("Music~")
                        checkbox2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

                        container.layout().setSpacing(0)
                        container.addWidget(checkbox1)
                        container.addWidget(checkbox2)

                    with createDenseContainer(h_container, QBoxLayout.TopToBottom) as container:

                        checkbox1 = SiCheckBoxRefactor(self)
                        checkbox1.setText("单选选项 1")
                        checkbox1.setDescription("唱，跳，Rap，篮球")
                        checkbox1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
                        checkbox1.setAutoExclusive(True)
                        checkbox1.setChecked(True)

                        checkbox2 = SiCheckBoxRefactor(self)
                        checkbox2.setText("单选选项 2")
                        checkbox2.setDescription("Music~")
                        checkbox2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
                        checkbox2.setAutoExclusive(True)

                        container.layout().setSpacing(0)
                        container.addWidget(checkbox1)
                        container.addWidget(checkbox2)

            with createPanelCard(group, "多选框") as card:
                with createDenseContainer(card.body(), QBoxLayout.TopToBottom) as container:
                    checkbox_1 = SiCheckBox(self)
                    checkbox_1.setText("在时间不足时提醒我")

                    checkbox_2 = SiCheckBox(self)
                    checkbox_2.setText("重复创建任务")

                    container.layout().setSpacing(16)
                    container.addWidget(checkbox_1)
                    container.addWidget(checkbox_2)

            with createPanelCard(group, "单选框") as card:
                with createDenseContainer(card.body(), QBoxLayout.TopToBottom) as container:
                    radio_button_1 = SiRadioButton(self)
                    radio_button_1.setChecked(True)
                    radio_button_1.setText("Load data when posible")

                    radio_button_2 = SiRadioButton(self)
                    radio_button_2.setText("Never load data")

                    container.layout().setSpacing(16)
                    container.addWidget(radio_button_1)
                    container.addWidget(radio_button_2)

            with createPanelCard(group, "带指示器的按钮") as card:
                with createDenseContainer(card.body(), QBoxLayout.LeftToRight) as container:

                    indicator_button1 = SiFlatButtonWithIndicator(self)
                    indicator_button1.setText("日期设置")
                    indicator_button1.setFixedHeight(40)
                    indicator_button1.setChecked(True)

                    indicator_button2 = SiFlatButtonWithIndicator(self)
                    indicator_button2.setText("时间设置")
                    indicator_button2.setFixedHeight(40)

                    indicator_button3 = SiFlatButtonWithIndicator(self)
                    indicator_button3.setText("首选项")
                    indicator_button3.setFixedHeight(40)

                    container.addWidget(indicator_button1)
                    container.addWidget(indicator_button2)
                    container.addWidget(indicator_button3)

                    button_group = QButtonGroup(self)
                    button_group.addButton(indicator_button1)
                    button_group.addButton(indicator_button2)
                    button_group.addButton(indicator_button3)
                    button_group.setExclusive(True)

            with createPanelCard(group, "开关") as card:
                with createDenseContainer(card.body(), QBoxLayout.LeftToRight) as container:

                    switch = SiSwitchRefactor(self)

                    container.addWidget(switch)

        with self.titled_widgets_group as group:
            group.addTitle("单选框")

            self.refactor_radiobuttons = OptionCardPlaneForWidgetDemos(self)
            self.refactor_radiobuttons.setTitle("单行单选框")

            radio_button_container = SiDenseVContainer(self)
            radio_button_container.setSpacing(6)

            self.refactor_radio_button = SiRadioButtonR(self)
            self.refactor_radio_button.setText("只因你太美")
            self.refactor_radio_button.adjustSize()
            self.refactor_radio_button.setChecked(True)

            self.refactor_radio_button2 = SiRadioButtonR(self)
            self.refactor_radio_button2.setText("你干嘛嗨嗨呦")
            self.refactor_radio_button2.adjustSize()

            self.refactor_radio_button3 = SiRadioButtonR(self)
            self.refactor_radio_button3.setText("唱跳 Rap 篮球")
            self.refactor_radio_button3.adjustSize()

            radio_button_container.addWidget(self.refactor_radio_button)
            radio_button_container.addWidget(self.refactor_radio_button2)
            radio_button_container.addWidget(self.refactor_radio_button3)
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
            group.addTitle("编辑框")

            self.editbox = OptionCardPlaneForWidgetDemos(self)
            self.editbox.setTitle("单行文本编辑框")

            self.linear_edit_box = SiCapsuleLineEdit(self)
            self.linear_edit_box.resize(560, 36)
            self.linear_edit_box.setTitleWidthMode(SiCapsuleLineEdit.TitleWidthMode.Ratio)
            self.linear_edit_box.setTitle("Repository Name")
            self.linear_edit_box.setText("PyQt-SiliconUI")

            self.linear_edit_box2 = SiCapsuleLineEdit(self)
            self.linear_edit_box2.resize(560, 36)
            self.linear_edit_box2.setTitleWidthMode(SiCapsuleLineEdit.TitleWidthMode.Ratio)
            self.linear_edit_box2.setTitle("Owner")
            self.linear_edit_box2.setText("ChinaIceF")

            self.linear_edit_box3 = SiCapsuleLineEdit(self)
            self.linear_edit_box3.resize(560, 36)
            self.linear_edit_box3.setTitleWidthMode(SiCapsuleLineEdit.TitleWidthMode.Ratio)
            self.linear_edit_box3.setTitle("Description")
            self.linear_edit_box3.setText("A powerful and artistic UI library based on PyQt5")

            self.check_button = SiFlatButton(self)
            self.check_button.setText("确定")
            self.linear_edit_box3.addWidgetToRight(self.check_button)

            self.editbox.body().setSpacing(11)
            self.editbox.body().addWidget(self.linear_edit_box)
            self.editbox.body().addWidget(self.linear_edit_box2)
            self.editbox.body().addWidget(self.linear_edit_box3)
            # self.editbox.body().addWidget(self.check_button)
            self.editbox.body().addPlaceholder(12)
            self.editbox.adjustSize()

            self.capsule_editbox = OptionCardPlaneForWidgetDemos(self)
            self.capsule_editbox.setTitle("小型文本编辑框")

            self.capsule_edit = SiLabeledLineEdit(self)
            self.capsule_edit.setTitle("用户名")
            self.capsule_edit.setPlaceholderText("您的用户名...")
            self.capsule_edit.resize(170, 58)

            self.spinbox = SiSpinBox(self)
            self.spinbox.setTitle("运行次数")
            self.spinbox.resize(170, 58)

            self.spinbox_double = SiDoubleSpinBox(self)
            self.spinbox_double.setTitle("参数")
            self.spinbox_double.setSingleStep(0.1)
            self.spinbox_double.resize(170, 58)

            self.capsule_editbox.body().setSpacing(11)
            self.capsule_editbox.body().addWidget(self.capsule_edit)
            self.capsule_editbox.body().addWidget(self.spinbox)
            self.capsule_editbox.body().addWidget(self.spinbox_double)
            self.capsule_editbox.body().addPlaceholder(12)
            self.capsule_editbox.adjustSize()

            group.addWidget(self.editbox)
            group.addWidget(self.capsule_editbox)

        with self.titled_widgets_group as group:
            group.addTitle("卡片容器")

            bar_test = SiTriSectionRowCard(self, SiGlobal.siui.iconpack.toPixmap("ic_fluent_slide_text_cursor_filled"))
            bar_test.actionsContainer().addWidget(SiSwitchRefactor(self))
            bar_test.adjustSize()
            group.addWidget(bar_test)

            with createPanelCard(group, "区间指示器") as card:

                indicator = SiLinearPartitionIndicator(self)
                indicator.activate()
                indicator.setFixedSize(200, 4)
                indicator.setNodeAmount(7)
                indicator.setVisualWidth(200)
                indicator.setVisualHeight(4)

                indicator.setEndIndex(1)

                def test_func_1():
                    indicator.setStartIndex((indicator.startIndex() + 1) if indicator.startIndex() < indicator.nodeAmount() - 1 else 0)
                def test_func_2():
                    indicator.setEndIndex((indicator.endIndex() + 1) if indicator.endIndex() < indicator.nodeAmount() - 1 else 0)

                btn_container = SiDenseContainer(self, QBoxLayout.LeftToRight)

                button1 = SiPushButtonRefactor.withText("开始增加", self)
                button2 = SiPushButtonRefactor.withText("结束增加", self)
                button3 = SiPushButtonRefactor.withText("平移", self)
                button4 = SiPushButtonRefactor.withText("激活", self)
                button5 = SiPushButtonRefactor.withText("去激活", self)
                button6 = SiPushButtonRefactor.withText("错误", self)

                button1.clicked.connect(test_func_1)
                button2.clicked.connect(test_func_2)

                button3.clicked.connect(test_func_1)
                button3.clicked.connect(test_func_2)

                button4.clicked.connect(lambda: indicator.activate())
                button5.clicked.connect(indicator.deactivate)
                button6.clicked.connect(indicator.warn)

                btn_container.addWidget(button1)
                btn_container.addWidget(button2)
                btn_container.addWidget(button3)
                btn_container.addWidget(button4)
                btn_container.addWidget(button5)
                btn_container.addWidget(button6)

                card.body().addWidget(indicator)
                card.body().addWidget(btn_container)

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
