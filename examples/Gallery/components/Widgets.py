from SiliconUI import *
from SiliconUI.SiGlobal import *
from SiliconUI.SiSticker import SiSticker

from .web_url import GithubUrl, browse


class WidgetsExampleDisplayer(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        widgets_sticker_width = 580
        status_sticker_width = 320

        self.layout = SiLayoutH(self)

        self.sticker_widgets = WidgetSticker(self)
        self.sticker_widgets.setFixedWidth(widgets_sticker_width)

        self.sticker_status = SiSticker(self)
        self.sticker_status.setFixedWidth(status_sticker_width)
        self.sticker_status.setTitle("信号表")
        self.sticker_status.setInterval(0)
        self.sticker_status.setMinimumSize(status_sticker_width, 64)
        self.sticker_status.setVisible(False)

        self.layout.addItem(self.sticker_widgets)
        self.layout.addItem(self.sticker_status)

    def setWidth(self, widgets_sticker_width, status_sticker_width):
        self.sticker_widgets.setFixedWidth(widgets_sticker_width)
        self.sticker_status.setFixedWidth(status_sticker_width)

    def setCodeURL(self, url):
        self.sticker_widgets.button_github.clicked.connect(lambda: os.system(f"start {url}"))

    def setTitle(self, title):
        self.sticker_widgets.setTitle(title)

    def addItem(self, item):
        self.sticker_widgets.addItem(item)
        self.layout.adjustSize()
        self.adjustSize()

    def addValueStatus(self, name, signals: list, note="", width=128):
        self.sticker_status.setVisible(True)
        new_type = SiLabel(self)
        new_type.resize(6, 18)
        new_type.setStyleSheet("background-color: #664976; border-radius: 3px")
        new_type.setHint("具参信号")

        new_status = SiLabel(self)
        new_status.setHint(note)
        new_status.setStyleSheet(
            f"""
            padding-left: 4px; padding-right: 4px; padding-top: 2px; padding-bottom: 2px;
            color: {colorset.TEXT_GRAD_HEX[0]};
            border-radius: 4px """
        )
        new_status.setText(name)

        new_value = SiLabelHasUpdateAnimation(self)
        new_value.setFixedWidth(width)
        new_value.setFixedHeight(24)
        new_value.setStyleSheet(
            f"""
            padding-left: 4px; padding-right: 4px; padding-top: 2px; padding-bottom: 2px;
            color: {colorset.TEXT_GRAD_HEX[1]};
            text-align: right;
            border-radius: 4px """
        )
        new_value.setAlignment(Qt.AlignRight)
        new_value.setAutoAdjustSize(False)

        for signal in signals:
            signal.connect(new_value.setText)
            signal.connect(new_value.activate)

        layout = SiLayoutH(self)
        layout.setInterval(4)
        layout.setFixedWidth(self.sticker_status.width() - 48)
        layout.setAlignCenter(True)
        layout.addItem(new_type)
        layout.addItem(new_status)
        layout.addItem(new_value, "right")

        self.sticker_status.addItem(layout)
        self.layout.adjustSize()
        self.adjustSize()

    def addSignalStatus(self, name, signals: list, note=""):
        self.sticker_status.setVisible(True)
        new_type = SiLabel(self)
        new_type.resize(6, 18)
        new_type.setStyleSheet("background-color: #3D6D76; border-radius: 3px")
        new_type.setHint("信号")

        new_status = SiLabelHasUpdateAnimation(self)
        new_status.setHint(note)
        new_status.setStyleSheet(
            f"""
            padding-left: 4px;
            padding-right: 4px;
            padding-top: 2px;
            padding-bottom: 2px;
            color: {colorset.TEXT_GRAD_HEX[0]};
            border-radius: 4px """
        )
        new_status.setText(name)
        for signal in signals:
            signal.connect(new_status.activate)

        layout = SiLayoutH(self)
        layout.setAlignCenter(True)
        layout.setInterval(4)
        layout.addItem(new_type)
        layout.addItem(new_status)

        self.sticker_status.addItem(layout)
        self.layout.adjustSize()
        self.adjustSize()

    def resizeEvent(self, event):
        size = event.size()
        w, h = size.width(), size.height()

        self.layout.resize(w, h)

    def adjustSize(self):
        h = max(self.sticker_widgets.height(), self.sticker_status.height())
        self.resize(self.width(), h)
        self.sticker_widgets.resize(self.sticker_widgets.width(), h)
        self.sticker_status.resize(self.sticker_status.width(), h)


class WidgetSticker(SiliconUI.SiSticker):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.button_github = SiButtonFlat(self)
        self.button_github.resize(32, 32)
        self.button_github.load(SiGlobal.icons.get("fi-rr-link"))
        self.button_github.setHint("查看源代码")

        self.button_report_bug = SiButtonFlat(self)
        self.button_report_bug.resize(32, 32)
        self.button_report_bug.load(SiGlobal.icons.get("fi-rr-bug"))
        self.button_report_bug.setHint("报告问题")
        self.button_report_bug.clicked.connect(lambda: browse(GithubUrl.Issues_New))

        self.head.addItem(self.button_github, side="right")
        self.head.addItem(self.button_report_bug, side="right")


class WidgetsExample(SiliconUI.SiScrollFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.setStyleSheet("")
        self.max_width_policy = False  # 取消过长中置

        widgets_width = 580

        ## ================ Stack 开始 ===================

        self.stack_labels = SiliconUI.SiCategory(self)
        self.stack_labels.setTitle("标签")

        self.sticker_label = WidgetsExampleDisplayer(self.stack_labels)
        self.sticker_label.setTitle("文字标签")
        self.sticker_label.setCodeURL(GithubUrl.SiLabel)

        self.label_with_no_hint = SiliconUI.SiLabel(self)
        self.label_with_no_hint.setText("测试标签")

        self.label_with_hint = SiliconUI.SiLabel(self)
        self.label_with_hint.setText("测试标签（具有提示信息）")
        self.label_with_hint.setHint("你好，我是提示信息")

        # 添加到 Sticker
        self.sticker_label.addItem(self.label_with_no_hint)
        self.sticker_label.addItem(self.label_with_hint)

        self.sticker_pixlabel_with_hint = WidgetsExampleDisplayer(self.stack_labels)
        self.sticker_pixlabel_with_hint.setTitle("图片标签")
        self.sticker_pixlabel_with_hint.setCodeURL(GithubUrl.SiLabel)

        self.layout_pixlabel = SiLayoutH(self)

        self.pixlabel_with_hint = SiliconUI.SiPixLabel(self)
        self.pixlabel_with_hint.resize(80, 80)
        self.pixlabel_with_hint.setRadius(40)
        self.pixlabel_with_hint.load("./img/headpic.png")
        self.pixlabel_with_hint.setHint("关注霏泠谢谢喵")

        self.pixlabel_with_hint_roundrect = SiliconUI.SiPixLabel(self)
        self.pixlabel_with_hint_roundrect.resize(80, 80)
        self.pixlabel_with_hint_roundrect.setRadius(32)
        self.pixlabel_with_hint_roundrect.load("./img/headpic.png")
        self.pixlabel_with_hint_roundrect.setHint("尺寸 80*80，圆角半径 20")

        self.layout_pixlabel.addItem(self.pixlabel_with_hint)
        self.layout_pixlabel.addItem(self.pixlabel_with_hint_roundrect)
        self.layout_pixlabel.setFixedHeight(80)

        # 添加到 Sticker
        self.sticker_pixlabel_with_hint.addItem(self.layout_pixlabel)

        self.sticker_movable_label = WidgetsExampleDisplayer(self.stack_labels)
        self.sticker_movable_label.setTitle("动画标签")
        self.sticker_movable_label.setCodeURL(GithubUrl.SiLabel)

        self.layout_movable_label = SiliconUI.SiLayoutH(self)
        self.layout_movable_label.setFixedWidth(580)
        self.layout_movable_label.setFixedHeight(80)

        self.movable_label = SiliconUI.SiLabel(self)
        self.movable_label.resize(128, 32)
        self.movable_label.setHint("我是动画标签，支持 moveTo, resizeTo 方法")
        self.movable_label.setMoveLimits(0, 0, 532, 80)
        self.movable_label.setStyleSheet(
            f"""
            border-radius: 4px;
            background-color: {colorset.BG_GRAD_HEX[4]};
        """
        )

        self.layout_movable_label.addItem(self.movable_label)

        self.layout_button = SiliconUI.SiLayoutH(self)

        self.button_random_x = SiliconUI.SiButton(self)
        self.button_random_x.setText("随机移动")
        self.button_random_x.resize(128, 32)
        self.button_random_x.clicked.connect(
            lambda: self.movable_label.moveTo(int(random.random() * 532), int(random.random() * 80))
        )

        self.button_random_size = SiliconUI.SiButton(self)
        self.button_random_size.setText("随机大小")
        self.button_random_size.resize(128, 32)
        self.button_random_size.clicked.connect(
            lambda: self.movable_label.resizeTo(int(random.random() * 256 + 8), int(random.random() * 64 + 8))
        )

        self.button_reset = SiliconUI.SiButton(self)
        self.button_reset.setText("还原初始状态")
        self.button_reset.resize(128, 32)
        self.button_reset.clicked.connect(lambda: self.movable_label.moveTo(0, 0))
        self.button_reset.clicked.connect(lambda: self.movable_label.resizeTo(128, 32))

        self.layout_button.addItem(self.button_random_x)
        self.layout_button.addItem(self.button_random_size)
        self.layout_button.addItem(self.button_reset)

        self.sticker_movable_label.addItem(self.layout_movable_label)
        self.sticker_movable_label.addItem(self.layout_button)

        self.sticker_draggable_label = WidgetsExampleDisplayer(self.stack_labels)
        self.sticker_draggable_label.setTitle("可拖动标签")
        self.sticker_draggable_label.setCodeURL(GithubUrl.SiLabel)

        self.layout_draggable_label = SiliconUI.SiLayoutH(self)
        self.layout_draggable_label.setFixedWidth(526)
        self.layout_draggable_label.setFixedHeight(80)

        self.draggable_label = SiliconUI.SiDraggableLabel(self)
        self.draggable_label.resize(128, 32)
        self.draggable_label.setHint("任意拖动，支持过渡动画")
        self.draggable_label.setMoveLimits(0, 0, 526, 80)
        self.draggable_label.animation_move.setFactor(1 / 6)  # 放慢动画
        self.draggable_label.setStyleSheet(
            f"""
            border-radius: 4px;
            background-color: {colorset.BG_GRAD_HEX[4]};
        """
        )

        self.layout_draggable_label.addItem(self.draggable_label)

        self.sticker_draggable_label.addItem(self.layout_draggable_label)

        # 添加
        self.stack_labels.addItem(self.sticker_label)
        self.stack_labels.addItem(self.sticker_pixlabel_with_hint)
        self.stack_labels.addItem(self.sticker_movable_label)
        self.stack_labels.addItem(self.sticker_draggable_label)

        ## ================ Stack 开始 ===================

        self.stack_buttons = SiliconUI.SiCategory(self)
        self.stack_buttons.setTitle("按钮")

        self.sticker_button_normal = WidgetsExampleDisplayer(self.stack_labels)
        self.sticker_button_normal.setTitle("标准按钮")
        self.sticker_button_normal.setCodeURL(GithubUrl.SiButton)

        self.layout_button_normal = SiLayoutH(self)

        self.button_normal_A = SiButton(self)
        self.button_normal_A.setStrong(False)
        self.button_normal_A.setText("普通按钮")
        self.button_normal_A.resize(128, 32)

        self.button_normal_B = SiButton(self)
        self.button_normal_B.setStrong(True)
        self.button_normal_B.setText("高亮按钮")
        self.button_normal_B.resize(128, 32)

        self.button_normal_C = SiButtonHoldtoConfirm(self)
        self.button_normal_C.setText("长按按钮")
        self.button_normal_C.resize(128, 32)

        self.layout_button_normal.addItem(self.button_normal_A, "left")
        self.layout_button_normal.addItem(self.button_normal_B, "left")
        self.layout_button_normal.addItem(self.button_normal_C, "left")

        # 添加到 sticker
        self.sticker_button_normal.addItem(self.layout_button_normal)
        self.sticker_button_normal.addSignalStatus(
            "clicked",
            [
                self.button_normal_A.clicked,
                self.button_normal_B.clicked,
                self.button_normal_C.clicked,
            ],
            "被点击时触发",
        )
        self.sticker_button_normal.addValueStatus(
            "holdStateChanged",
            [
                self.button_normal_A.holdStateChanged,
                self.button_normal_B.holdStateChanged,
                self.button_normal_C.holdStateChanged,
            ],
            "当按钮被按下 / 松开时触发",
        )

        self.sticker_button_icon = WidgetsExampleDisplayer(self.stack_labels)
        self.sticker_button_icon.setTitle("图标按钮")
        self.sticker_button_icon.setCodeURL(GithubUrl.SiButton)

        self.button_icon = SiButtonFlat(self)
        self.button_icon.setHint("我是按钮示例")
        self.button_icon.load(SiGlobal.icons.get("fi-rr-disk"))
        self.button_icon.resize(32, 32)

        # 添加到 sticker
        self.sticker_button_icon.addItem(self.button_icon)

        self.sticker_button_label = WidgetsExampleDisplayer(self.stack_labels)
        self.sticker_button_label.setTitle("标签按钮")
        self.sticker_button_label.setCodeURL(GithubUrl.SiButton)

        self.button_label = ClickableLabel(self)
        self.button_label.setStyleSheet("color: #ffffff; padding: 8px")
        self.button_label.setFont(font_L1_bold)
        self.button_label.setFixedHeight(32)
        self.button_label.setText("标签按钮测试")
        self.button_label.adjustSize()

        self.button_label_flow = ClickableLabel(self)  # TODO: 这部分以后整合到预设
        self.button_label_flow.radius = 14
        self.button_label_flow.setStyleSheet("""
            background-color: #20ffffff;
            color: #ffffff;
            padding: 4px;
            padding-left: 12px;
            padding-right: 12px;
            border-radius: 14px;
            """)
        self.button_label_flow.setFont(font_L1_bold)
        self.button_label_flow.setFixedHeight(28)
        self.button_label_flow.setText("流式标签")
        self.button_label_flow.adjustSize()

        # 添加到 sticker
        self.sticker_button_label.addItem(self.button_label)
        self.sticker_button_label.addItem(self.button_label_flow)

        self.sticker_button_icon_label = WidgetsExampleDisplayer(self.stack_labels)
        self.sticker_button_icon_label.setTitle("图标标签按钮")
        self.sticker_button_icon_label.setCodeURL(GithubUrl.SiButton)

        self.button_icon_label = SiButtonFlatWithLabel(self)
        self.button_icon_label.setFixedHeight(32)
        self.button_icon_label.setText("鸡你太美")
        self.button_icon_label.label.setFont(font_L1_bold)
        self.button_icon_label.load(SiGlobal.icons.get("fi-rr-basketball"))

        # 添加到 sticker
        self.sticker_button_icon_label.addItem(self.button_icon_label)

        self.sticker_radio_button = WidgetsExampleDisplayer(self.stack_labels)
        self.sticker_radio_button.setTitle("单选框")
        self.sticker_radio_button.setCodeURL(GithubUrl.SiButton)

        self.layout_radio_button = SiLayoutH(self)
        self.layout_radio_button.setInterval(16)

        self.radio_button = SiRadioButton(self)
        self.radio_button.setText("炫我嘴里")
        self.radio_button.setFixedWidth(96)

        self.radio_button2 = SiRadioButton(self)
        self.radio_button2.setText("睡大觉")
        self.radio_button2.setFixedWidth(96)

        self.radio_button3 = SiRadioButton(self)
        self.radio_button3.setText("买买买")
        self.radio_button3.setFixedWidth(96)

        self.radio_button4 = SiRadioButton(self)
        self.radio_button4.setText("来场旅行")
        self.radio_button4.setFixedWidth(96)

        self.layout_radio_button.addItem(self.radio_button)
        self.layout_radio_button.addItem(self.radio_button2)
        self.layout_radio_button.addItem(self.radio_button3)
        self.layout_radio_button.addItem(self.radio_button4)

        self.radio_button_group = SiRadioButtonGroup()
        self.radio_button_group.addItem(self.radio_button)
        self.radio_button_group.addItem(self.radio_button2)
        self.radio_button_group.addItem(self.radio_button3)
        self.radio_button_group.addItem(self.radio_button4)

        # 添加到 sticker
        self.sticker_radio_button.addItem(self.layout_radio_button)

        # 添加
        self.stack_buttons.addItem(self.sticker_button_normal)
        self.stack_buttons.addItem(self.sticker_button_icon)
        self.stack_buttons.addItem(self.sticker_button_label)
        self.stack_buttons.addItem(self.sticker_button_icon_label)
        self.stack_buttons.addItem(self.sticker_radio_button)

        ## ================ Stack 开始 ===================

        self.stack_menus = SiliconUI.SiCategory(self)
        self.stack_menus.setTitle("菜单")

        self.sticker_combobox = WidgetsExampleDisplayer(self.stack_menus)
        self.sticker_combobox.setTitle("下拉菜单")
        self.sticker_combobox.setCodeURL(GithubUrl.SiComboBox)

        self.combobox = SiComboBox(self)
        self.combobox.resize(160, 32)
        self.combobox.addOption("练习两年半", 2.5)
        self.combobox.addOption("鸡你太美", 114514)
        self.combobox.addOption("你干嘛嗨嗨呦", 1919)
        self.combobox.addOption("你好烦", 810)
        self.combobox.setOption("练习两年半")

        # 添加到 Sticker
        self.sticker_combobox.addItem(self.combobox)
        self.sticker_combobox.addSignalStatus("clicked", [self.combobox.clicked], "被点击时触发")
        self.sticker_combobox.addValueStatus(
            "holdStateChanged", [self.combobox.holdStateChanged], "被按下 / 松开时触发"
        )
        self.sticker_combobox.addValueStatus(
            "valueChanged", [self.combobox.valueChanged], "变更选项时触发，值为选项设定值"
        )
        self.sticker_combobox.addValueStatus(
            "textChanged", [self.combobox.textChanged], "变更选项时触发，值为选项设定文字"
        )

        # 添加到 Stack
        self.stack_menus.addItem(self.sticker_combobox)

        ## ================ Stack 开始 ===================

        self.stack_switchs = SiliconUI.SiCategory(self)
        self.stack_switchs.setTitle("开关")

        self.sticker_switch = WidgetsExampleDisplayer(self.stack_switchs)
        self.sticker_switch.setTitle("开关")
        self.sticker_switch.setCodeURL(GithubUrl.SiSwitch)

        self.switch = SiSwitch(self)
        self.switch.resize(150, 32)

        # 添加到 Sticker
        self.sticker_switch.addItem(self.switch)
        self.sticker_switch.addSignalStatus("clicked", [self.switch.clicked], "被点击时触发")
        self.sticker_switch.addValueStatus("stateChanged", [self.switch.stateChanged], "被点击时触发，值为开关状态")

        # 添加到 Stack
        self.stack_switchs.addItem(self.sticker_switch)

        ## ================ Stack 开始 ===================

        self.stack_sliderbar = SiliconUI.SiCategory(self)
        self.stack_sliderbar.setTitle("滑动条")

        self.sticker_sliderbar_free = WidgetsExampleDisplayer(self.stack_sliderbar)
        self.sticker_sliderbar_free.setTitle("连续滑动条")
        self.sticker_sliderbar_free.setCodeURL(GithubUrl.SiSliderBar)

        self.sliderbar_free = SiSliderBar(self)
        self.sliderbar_free.resize(500, 32)

        # 添加到 Sticker
        self.sticker_sliderbar_free.addItem(self.sliderbar_free)
        self.sticker_sliderbar_free.addValueStatus(
            "valueChanged", [self.sliderbar_free.valueChanged], "值改变时触发，值为滑动条当前值"
        )

        self.sticker_sliderbar_levelized = WidgetsExampleDisplayer(self.stack_sliderbar)
        self.sticker_sliderbar_levelized.setTitle("分档滑动条")
        self.sticker_sliderbar_levelized.setCodeURL(GithubUrl.SiSliderBar)

        self.sliderbar_levelized = SiSliderBar(self)
        self.sliderbar_levelized.resize(500, 32)
        self.sliderbar_levelized.setDispersed(range(0, 7))

        # 添加到 Sticker
        self.sticker_sliderbar_levelized.addItem(self.sliderbar_levelized)
        self.sticker_sliderbar_levelized.addValueStatus(
            "valueChanged", [self.sliderbar_levelized.valueChanged], "值改变时触发，值为滑动条当前值"
        )

        # 添加到 Stack
        self.stack_sliderbar.addItem(self.sticker_sliderbar_free)
        self.stack_sliderbar.addItem(self.sticker_sliderbar_levelized)

        ## ================ Stack 开始 ===================

        self.stack_inputboxes = SiliconUI.SiCategory(self)
        self.stack_inputboxes.setTitle("输入框")

        self.sticker_inputboxes = WidgetsExampleDisplayer(self.stack_inputboxes)
        self.sticker_inputboxes.setTitle("输入框")
        self.sticker_inputboxes.setCodeURL(GithubUrl.SiInputBox)

        self.inputbox = SiInputBox(self)
        self.inputbox.resize(300, 32)

        # 添加到 Sticker
        self.sticker_inputboxes.addItem(self.inputbox)
        self.sticker_inputboxes.addSignalStatus("editingFinished", [self.inputbox.editingFinished], "编辑已完成时触发")
        self.sticker_inputboxes.addSignalStatus("selectionChanged", [self.inputbox.selectionChanged], "选区改变时触发")
        self.sticker_inputboxes.addValueStatus(
            "cursorPositionChanged", [self.inputbox.cursorPositionChanged], "光标移动时触发，值为光标位置", width=96
        )
        self.sticker_inputboxes.addValueStatus("textEdited", [self.inputbox.textEdited], "文本被编辑时触发")

        # 添加到 Stack
        self.stack_inputboxes.addItem(self.sticker_inputboxes)

        ## ================ Stack 开始 ===================

        self.stack_progressbar = SiliconUI.SiCategory(self)
        self.stack_progressbar.setTitle("进度条")

        self.sticker_progressbar = WidgetsExampleDisplayer(self.stack_progressbar)
        self.sticker_progressbar.setTitle("进度条")
        self.sticker_progressbar.setWidth(800, 320)

        self.layout_progress_bar = SiliconUI.SiLayoutV(self)

        self.progress_bar = SiliconUI.SiProgressBar(self)
        self.progress_bar.setBorderRadius(3)
        self.progress_bar.resize(480, 6)

        self.layout_progress_bar_buttons = SiliconUI.SiLayoutH(self)

        self.random_progress = SiliconUI.SiButton(self)
        self.random_progress.setText("随机进度")
        self.random_progress.resize(128, 32)
        self.random_progress.clicked.connect(lambda: self.progress_bar.setProgress(random.random()))

        self.shift_status = SiliconUI.SiButton(self)
        self.shift_status.setText("随机切换状态")
        self.shift_status.resize(128, 32)
        self.shift_status.clicked.connect(lambda: self.progress_bar.setStatus(int(random.random() * 3)))

        self.random_color = SiliconUI.SiButton(self)
        self.random_color.setText("随机颜色")
        self.random_color.resize(128, 32)
        self.random_color.clicked.connect(lambda: self.progress_bar.setBarColor(Color.random()))

        self.stepping = SiliconUI.SiButton(self)
        self.stepping.setText("随机步进")
        self.stepping.resize(128, 32)
        self.stepping.clicked.connect(lambda: self.progress_bar.stepping(random.random() / 10))

        self.layout_progress_bar_buttons.addItem(self.random_progress)
        self.layout_progress_bar_buttons.addItem(self.shift_status)
        self.layout_progress_bar_buttons.addItem(self.random_color)
        self.layout_progress_bar_buttons.addItem(self.stepping)

        self.layout_progress_bar.addItem(self.progress_bar)
        self.layout_progress_bar.addItem(self.layout_progress_bar_buttons)

        self.sticker_progressbar.addItem(self.layout_progress_bar)

        self.stack_progressbar.addItem(self.sticker_progressbar)

        ## ================ Stack 开始 ===================

        self.stack_tableview = SiliconUI.SiCategory(self)
        self.stack_tableview.setTitle("表格")

        self.sticker_tableview = WidgetsExampleDisplayer(self.stack_tableview)
        self.sticker_tableview.setTitle("表格")
        self.sticker_tableview.setWidth(800, 320)

        self.table = SiliconUI.SiTable(self)
        self.table.setClasses(
            ["排名", "用户名", "分数", "准确率", "评级", "PP"],
            [
                64,
                196,
                128,
                96,
                64,
                64,
            ],
        )
        self.table.addData(["#1", "BeautifulChicken", "1,000,000", "100.00%", "SS", "120"])
        self.table.addData(["#2", "SummerainCN", "998,692", "98.87%", "S", "97"])
        self.table.addData(["#3", "ChinaIceF", "462,534", "92.14%", "A", "67"])
        self.table.addData(["#4", "SomeoneElse", "384,591", "91.25%", "A", "87"])
        self.table.addData(["#5", "Rick_fake", "273,479", "89.73%", "B", "76"])
        self.table.addData(["#6", "ImRealikun", "114,514", "91.98%", "A", "34"])
        self.table.addData(["#7", "PlayerA", "-", "-", "-", "-"])
        self.table.addData(["#8", "PlayerB", "-", "-", "-", "-"])
        self.table.addData(["#9", "PlayerC", "-", "-", "-", "-"])
        self.table.addData(["#10", "PlayerD", "-", "-", "-", "-"])
        self.table.resize(664, 200)

        self.sticker_tableview.addItem(self.table)

        self.stack_tableview.addItem(self.sticker_tableview)

        self.addItem(self.stack_labels)
        self.addItem(self.stack_buttons)
        self.addItem(self.stack_menus)
        self.addItem(self.stack_switchs)
        self.addItem(self.stack_sliderbar)
        self.addItem(self.stack_inputboxes)
        self.addItem(self.stack_progressbar)
        self.addItem(self.stack_tableview)
