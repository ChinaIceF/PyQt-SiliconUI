from PyQt5.Qt import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.Qt import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit
import numpy
import time
import os

import silicon
import silicon.SiGlobal as SiGlobal
from silicon import *
from silicon.SiSticker import SiSticker

class WidgetsExampleDisplayer(QLabel):
    def __init__(self, parent):
        super().__init__(parent)

        widgets_sticker_width = 580
        status_sticker_width = 320

        self.layout = SiLayoutH(self)

        self.sticker_widgets = WidgetSticker(self)
        self.sticker_widgets.setFixedWidth(widgets_sticker_width)

        self.sticker_status = SiSticker(self)
        self.sticker_status.setFixedWidth(status_sticker_width)
        self.sticker_status.setTitle('信号表')
        self.sticker_status.setInterval(0)
        self.sticker_status.setMinimumSize(status_sticker_width, 64)
        self.sticker_status.setVisible(False)

        self.layout.addItem(self.sticker_widgets)
        self.layout.addItem(self.sticker_status)

    def setCodeURL(self, url):
        self.sticker_widgets.button_github.clicked.connect(
            lambda : os.system('start {}'.format(url)))

    def setTitle(self, title):
        self.sticker_widgets.setTitle(title)

    def addItem(self, item):
        self.sticker_widgets.addItem(item)
        self.layout.adjustSize()
        self.adjustSize()

    def addValueStatus(self, name, signals :list, note = '', width = 128):
        self.sticker_status.setVisible(True)
        new_type = SiLabel(self)
        new_type.resize(6, 18)
        new_type.setStyleSheet('background-color: #664976; border-radius: 3px')
        new_type.setHint('具参信号')

        new_status = SiLabel(self)
        new_status.setHint(note)
        new_status.setStyleSheet('''
            padding-left: 4px; padding-right: 4px; padding-top: 2px; padding-bottom: 2px;
            color: #ffffff;
            border-radius: 4px ''')
        new_status.setText(name)

        new_value = SiLabelHasUpdateAnimation(self)
        new_value.setFixedWidth(width)
        new_value.setFixedHeight(24)
        new_value.setStyleSheet('''
            padding-left: 4px; padding-right: 4px; padding-top: 2px; padding-bottom: 2px;
            color: #e0e0e0;
            text-align: right;
            border-radius: 4px ''')
        new_value.setAlignment(Qt.AlignRight)
        new_value.setAutoAdjustSize(False)

        for signal in signals:
            signal.connect(new_value.setText)
            signal.connect(new_value.activate)

        layout = SiLayoutH(self)
        layout.setInterval(4)
        layout.setFixedWidth(self.sticker_status.width() - 48)
        layout.setCenter(True)
        layout.addItem(new_type)
        layout.addItem(new_status)
        layout.addItem(new_value, 'right')

        self.sticker_status.addItem(layout)
        self.layout.adjustSize()
        self.adjustSize()

    def addSignalStatus(self, name, signals :list, note = ''):
        self.sticker_status.setVisible(True)
        new_type = SiLabel(self)
        new_type.resize(6, 18)
        new_type.setStyleSheet('background-color: #3D6D76; border-radius: 3px')
        new_type.setHint('信号')

        new_status = SiLabelHasUpdateAnimation(self)
        new_status.setHint(note)
        new_status.setStyleSheet('''
            padding-left: 4px;
            padding-right: 4px;
            padding-top: 2px;
            padding-bottom: 2px;
            color: #ffffff;
            border-radius: 4px ''')
        new_status.setText(name)
        for signal in signals:
            signal.connect(new_status.activate)

        layout = SiLayoutH(self)
        layout.setCenter(True)
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


class WidgetSticker(silicon.SiSticker.SiSticker):
    def __init__(self, parent):
        super().__init__(parent)

        self.button_github = SiButtonFlat(self)
        self.button_github.resize(32, 32)
        self.button_github.load(SiGlobal.icons.get('fi-rr-link'))
        self.button_github.setHint('查看源代码')

        self.button_report_bug = SiButtonFlat(self)
        self.button_report_bug.resize(32, 32)
        self.button_report_bug.load(SiGlobal.icons.get('fi-rr-bug'))
        self.button_report_bug.setHint('报告问题')
        self.button_report_bug.clicked.connect(
            lambda : os.system('start https://github.com/ChinaIceF/PyQt-SiliconUI/issues/new'))

        self.head.addItem(self.button_github, side = 'right')
        self.head.addItem(self.button_report_bug, side = 'right')


class WidgetsExample(silicon.SiFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet('')
        self.max_width_policy = False  # 取消过长中置

        widgets_width = 580

        ## ================ Stack 开始 ===================

        self.stack_labels = silicon.SiStack(self)
        self.stack_labels.setTitle('标签')

        self.sticker_label = WidgetsExampleDisplayer(self.stack_labels)
        self.sticker_label.setTitle('文字标签')
        self.sticker_label.setCodeURL(
            'https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/silicon/SiLabel.py')

        self.label_with_no_hint = silicon.SiLabel(self)
        self.label_with_no_hint.setText('测试标签')

        self.label_with_hint = silicon.SiLabel(self)
        self.label_with_hint.setText('测试标签（具有提示信息）')
        self.label_with_hint.setHint('你好，我是提示信息')

        # 添加到 Sticker
        self.sticker_label.addItem(self.label_with_no_hint)
        self.sticker_label.addItem(self.label_with_hint)


        self.sticker_pixlabel_with_hint = WidgetsExampleDisplayer(self.stack_labels)
        self.sticker_pixlabel_with_hint.setTitle('图片标签')
        self.sticker_pixlabel_with_hint.setCodeURL(
            'https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/silicon/SiLabel.py')

        self.layout_pixlabel = SiLayoutH(self)

        self.pixlabel_with_hint = silicon.SiPixLabel(self)
        self.pixlabel_with_hint.resize(80, 80)
        self.pixlabel_with_hint.setRadius(40)
        self.pixlabel_with_hint.load('./img/headpic.png')
        self.pixlabel_with_hint.setHint('关注霏泠谢谢喵')

        self.pixlabel_with_hint_roundrect = silicon.SiPixLabel(self)
        self.pixlabel_with_hint_roundrect.resize(80, 80)
        self.pixlabel_with_hint_roundrect.setRadius(32)
        self.pixlabel_with_hint_roundrect.load('./img/headpic.png')
        self.pixlabel_with_hint_roundrect.setHint('尺寸 80*80，圆角半径 20')

        self.layout_pixlabel.addItem(self.pixlabel_with_hint)
        self.layout_pixlabel.addItem(self.pixlabel_with_hint_roundrect)
        self.layout_pixlabel.setFixedHeight(80)

        # 添加到 Sticker
        self.sticker_pixlabel_with_hint.addItem(self.layout_pixlabel)

        # 添加
        self.stack_labels.addItem(self.sticker_label)
        self.stack_labels.addItem(self.sticker_pixlabel_with_hint)



        ## ================ Stack 开始 ===================

        self.stack_buttons = silicon.SiStack(self)
        self.stack_buttons.setTitle('按钮')

        self.sticker_button_normal = WidgetsExampleDisplayer(self.stack_labels)
        self.sticker_button_normal.setTitle('标准按钮')
        self.sticker_button_normal.setCodeURL(
            'https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/silicon/SiButton.py')

        self.layout_button_normal = SiLayoutH(self)

        self.button_normal_A = SiButton(self)
        self.button_normal_A.setStrong(False)
        self.button_normal_A.setText('普通按钮')
        self.button_normal_A.resize(128, 32)

        self.button_normal_B = SiButton(self)
        self.button_normal_B.setStrong(True)
        self.button_normal_B.setText('高亮按钮')
        self.button_normal_B.resize(128, 32)

        self.button_normal_C = SiButtonHoldtoConfirm(self)
        self.button_normal_C.setText('长按按钮')
        self.button_normal_C.resize(128, 32)

        self.layout_button_normal.addItem(self.button_normal_A, 'left')
        self.layout_button_normal.addItem(self.button_normal_B, 'left')
        self.layout_button_normal.addItem(self.button_normal_C, 'left')

        # 添加到 sticker
        self.sticker_button_normal.addItem(self.layout_button_normal)
        self.sticker_button_normal.addSignalStatus('clicked',
            [self.button_normal_A.clicked,
             self.button_normal_B.clicked,
             self.button_normal_C.clicked,], '被点击时触发')
        self.sticker_button_normal.addValueStatus('holdStateChanged',
            [self.button_normal_A.holdStateChanged,
             self.button_normal_B.holdStateChanged,
             self.button_normal_C.holdStateChanged,], '当按钮被按下 / 松开时触发')

        self.sticker_button_icon = WidgetsExampleDisplayer(self.stack_labels)
        self.sticker_button_icon.setTitle('图标按钮')
        self.sticker_button_icon.setCodeURL(
            'https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/silicon/SiButton.py')

        self.button_icon = SiButtonFlat(self)
        self.button_icon.setHint('我是按钮示例')
        self.button_icon.load(SiGlobal.icons.get('fi-rr-disk'))
        self.button_icon.resize(32, 32)

        # 添加到 sticker
        self.sticker_button_icon.addItem(self.button_icon)



        self.sticker_button_label = WidgetsExampleDisplayer(self.stack_labels)
        self.sticker_button_label.setTitle('标签按钮')
        self.sticker_button_label.setCodeURL(
            'https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/silicon/SiButton.py')

        self.button_label = ClickableLabel(self)
        self.button_label.setStyleSheet('color: #ffffff; padding: 8px')
        self.button_label.setFont(font_L1_bold)
        self.button_label.setFixedHeight(32)
        self.button_label.setText('标签按钮测试')
        self.button_label.adjustSize()

        self.button_label_flow = ClickableLabel(self)   # TODO: 这部分以后整合到预设
        self.button_label_flow.radius = 14
        self.button_label_flow.setStyleSheet('''
            background-color: #20ffffff;
            color: #ffffff;
            padding: 4px;
            padding-left: 12px;
            padding-right: 12px;
            border-radius: 14px;
            ''')
        self.button_label_flow.setFont(font_L1_bold)
        self.button_label_flow.setFixedHeight(28)
        self.button_label_flow.setText('流式标签')
        self.button_label_flow.adjustSize()

        # 添加到 sticker
        self.sticker_button_label.addItem(self.button_label)
        self.sticker_button_label.addItem(self.button_label_flow)



        self.sticker_button_icon_label = WidgetsExampleDisplayer(self.stack_labels)
        self.sticker_button_icon_label.setTitle('图标标签按钮')
        self.sticker_button_icon_label.setCodeURL(
            'https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/silicon/SiButton.py')

        self.button_icon_label = SiButtonFlatWithLabel(self)
        self.button_icon_label.setFixedHeight(32)
        self.button_icon_label.setText('鸡你太美')
        self.button_icon_label.label.setFont(font_L1_bold)
        self.button_icon_label.load(SiGlobal.icons.get('fi-rr-basketball'))

        # 添加到 sticker
        self.sticker_button_icon_label.addItem(self.button_icon_label)

        # 添加
        self.stack_buttons.addItem(self.sticker_button_normal)
        self.stack_buttons.addItem(self.sticker_button_icon)
        self.stack_buttons.addItem(self.sticker_button_label)
        self.stack_buttons.addItem(self.sticker_button_icon_label)


        ## ================ Stack 开始 ===================

        self.stack_menus = silicon.SiStack(self)
        self.stack_menus.setTitle('菜单')

        self.sticker_combobox = WidgetsExampleDisplayer(self.stack_menus)
        self.sticker_combobox.setTitle('下拉菜单')
        self.sticker_combobox.setCodeURL(
            'https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/silicon/SiComboBox.py')

        self.combobox = SiComboBox(self)
        self.combobox.resize(160, 32)
        self.combobox.addOption('练习两年半', 2.5)
        self.combobox.addOption('鸡你太美', 114514)
        self.combobox.addOption('你干嘛嗨嗨呦', 1919)
        self.combobox.addOption('你好烦', 810)
        self.combobox.setOption('练习两年半')

        # 添加到 Sticker
        self.sticker_combobox.addItem(self.combobox)
        self.sticker_combobox.addSignalStatus('clicked',
            [self.combobox.clicked], '被点击时触发')
        self.sticker_combobox.addValueStatus('holdStateChanged',
            [self.combobox.holdStateChanged], '被按下 / 松开时触发')
        self.sticker_combobox.addValueStatus('valueChanged',
            [self.combobox.valueChanged], '变更选项时触发，值为选项设定值')
        self.sticker_combobox.addValueStatus('textChanged',
            [self.combobox.textChanged], '变更选项时触发，值为选项设定文字')


        # 添加到 Stack
        self.stack_menus.addItem(self.sticker_combobox)


        ## ================ Stack 开始 ===================

        self.stack_switchs = silicon.SiStack(self)
        self.stack_switchs.setTitle('开关')

        self.sticker_switch = WidgetsExampleDisplayer(self.stack_switchs)
        self.sticker_switch.setTitle('开关')
        self.sticker_switch.setCodeURL(
            'https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/silicon/SiSwitch.py')

        self.switch = SiSwitch(self)
        self.switch.resize(150, 32)

        # 添加到 Sticker
        self.sticker_switch.addItem(self.switch)
        self.sticker_switch.addSignalStatus('clicked',
            [self.switch.clicked], '被点击时触发')
        self.sticker_switch.addValueStatus('stateChanged',
            [self.switch.stateChanged], '被点击时触发，值为开关状态')

        # 添加到 Stack
        self.stack_switchs.addItem(self.sticker_switch)


        ## ================ Stack 开始 ===================

        self.stack_sliderbar = silicon.SiStack(self)
        self.stack_sliderbar.setTitle('滑动条')

        self.sticker_sliderbar_free = WidgetsExampleDisplayer(self.stack_sliderbar)
        self.sticker_sliderbar_free.setTitle('连续滑动条')
        self.sticker_sliderbar_free.setCodeURL(
            'https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/silicon/SiSliderBar.py')

        self.sliderbar_free = SiSliderBar(self)
        self.sliderbar_free.resize(500, 32)

        # 添加到 Sticker
        self.sticker_sliderbar_free.addItem(self.sliderbar_free)
        self.sticker_sliderbar_free.addValueStatus('valueChanged',
            [self.sliderbar_free.valueChanged], '值改变时触发，值为滑动条当前值')



        self.sticker_sliderbar_levelized = WidgetsExampleDisplayer(self.stack_sliderbar)
        self.sticker_sliderbar_levelized.setTitle('分档滑动条')
        self.sticker_sliderbar_levelized.setCodeURL(
            'https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/silicon/SiSliderBar.py')

        self.sliderbar_levelized = SiSliderBar(self)
        self.sliderbar_levelized.resize(500, 32)
        self.sliderbar_levelized.setDispersed(range(0, 7))

        # 添加到 Sticker
        self.sticker_sliderbar_levelized.addItem(self.sliderbar_levelized)
        self.sticker_sliderbar_levelized.addValueStatus('valueChanged',
            [self.sliderbar_levelized.valueChanged], '值改变时触发，值为滑动条当前值')

        # 添加到 Stack
        self.stack_sliderbar.addItem(self.sticker_sliderbar_free)
        self.stack_sliderbar.addItem(self.sticker_sliderbar_levelized)


        ## ================ Stack 开始 ===================

        self.stack_inputboxes = silicon.SiStack(self)
        self.stack_inputboxes.setTitle('输入框')

        self.sticker_inputboxes = WidgetsExampleDisplayer(self.stack_inputboxes)
        self.sticker_inputboxes.setTitle('输入框')
        self.sticker_inputboxes.setCodeURL(
            'https://github.com/ChinaIceF/PyQt-SiliconUI/blob/main/silicon/SiInputBox.py')

        self.inputbox = SiInputBox(self)
        self.inputbox.resize(300, 32)

        # 添加到 Sticker
        self.sticker_inputboxes.addItem(self.inputbox)
        self.sticker_inputboxes.addSignalStatus('editingFinished',
            [self.inputbox.editingFinished], '编辑已完成时触发')
        self.sticker_inputboxes.addSignalStatus('selectionChanged',
            [self.inputbox.selectionChanged], '选区改变时触发')
        self.sticker_inputboxes.addValueStatus('cursorPositionChanged',
            [self.inputbox.cursorPositionChanged], '光标移动时触发，值为光标位置', width = 96)
        self.sticker_inputboxes.addValueStatus('textEdited',
            [self.inputbox.textEdited], '文本被编辑时触发')

        # 添加到 Stack
        self.stack_inputboxes.addItem(self.sticker_inputboxes)


        self.addItem(self.stack_labels)
        self.addItem(self.stack_buttons)
        self.addItem(self.stack_menus)
        self.addItem(self.stack_switchs)
        self.addItem(self.stack_sliderbar)
        self.addItem(self.stack_inputboxes)
